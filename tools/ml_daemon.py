"""
tools/ml_daemon.py — Layer 0.5b ML inference daemon
=====================================================
Serves the two local models consumed by the §5c verifier pipeline:

    POST /embed   sentence-transformers/all-MiniLM-L6-v2   (~80 MB)
    POST /nli     cross-encoder/nli-deberta-v3-base         (~440 MB)
    GET  /        health check + CUDA presence

Hardware target: RTX 3070 8 GB VRAM.  Both models fit simultaneously
without quantization.

HARD CONSTRAINT (ratified-decision-7):
    This file MUST NOT be imported from .venv/ (Flask env).
    torch is not installed there by design; any cross-import raises
    ModuleNotFoundError immediately — which is the intended behaviour.

PI TUNING SURFACE — intentionally left as stubs:
    EMBED_BATCH_SIZE     controls encode() batch_size
    NLI_MAX_LENGTH       tokenizer max_length (DeBERTa supports ≤ 512)
    fp16 / 8-bit quant   see comments in lifespan()
    normalize_embeddings True  → cosine ≡ dot-product; False → raw
    _NLI_LABELS order    verify against model config label2id before
                         promoting any downstream consumer to Layer 1b

Run via start-ml.bat, not directly.
"""

from __future__ import annotations

import logging
from contextlib import asynccontextmanager
from typing import Any

import torch
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from sentence_transformers import CrossEncoder, SentenceTransformer

# ---------------------------------------------------------------------------
# PI TUNING SURFACE
# ---------------------------------------------------------------------------
EMBED_MODEL_ID: str = "sentence-transformers/all-MiniLM-L6-v2"
NLI_MODEL_ID: str = "cross-encoder/nli-deberta-v3-base"

EMBED_BATCH_SIZE: int = 64       # PI: raise toward 256 on 8 GB VRAM
NLI_MAX_LENGTH: int = 512        # PI: reduce to 256 for throughput on short passages

# Label order for cross-encoder/nli-deberta-v3-base logits.
# Typical:  contradiction=0, entailment=1, neutral=2
# Verify:   .venv-ml\Scripts\python -c
#               "from transformers import AutoConfig; \
#                c = AutoConfig.from_pretrained('cross-encoder/nli-deberta-v3-base'); \
#                print(c.label2id)"
# smoke_ml.py emits a WARN if the contradiction pair mislabels.
_NLI_LABELS: list[str] = ["contradiction", "entailment", "neutral"]
# ---------------------------------------------------------------------------

logging.basicConfig(level=logging.INFO, format="%(levelname)s  %(message)s")
log = logging.getLogger("ml_daemon")

_embed_model: SentenceTransformer | None = None
_nli_model: CrossEncoder | None = None
_device: str = "cpu"


# ---------------------------------------------------------------------------
# Pydantic schemas — request/response bodies ONLY
# No entity-level schemas here; those belong to Layer 1b.
# ---------------------------------------------------------------------------

class EmbedRequest(BaseModel):
    texts: list[str] = Field(..., min_length=1)

class EmbedResponse(BaseModel):
    embeddings: list[list[float]]
    dim: int
    model: str

class NLIRequest(BaseModel):
    claim: str   = Field(..., description="Hypothesis / atomic fact to verify")
    source: str  = Field(..., description="Premise / retrieved source passage")

class NLIResponse(BaseModel):
    label: str
    score: float
    all_scores: dict[str, float]
    model: str

class HealthResponse(BaseModel):
    status: str
    cuda: bool
    device: str
    models_loaded: bool


# ---------------------------------------------------------------------------
# Lifespan — warm-up on startup
# ---------------------------------------------------------------------------

@asynccontextmanager
async def lifespan(app: FastAPI):  # noqa: ARG001
    global _embed_model, _nli_model, _device

    _device = "cuda" if torch.cuda.is_available() else "cpu"
    log.info("Device: %s", _device)

    log.info("Loading embed model: %s", EMBED_MODEL_ID)
    _embed_model = SentenceTransformer(
        EMBED_MODEL_ID,
        device=_device,
        # PI: add model_kwargs={"torch_dtype": torch.float16} for fp16
    )

    log.info("Loading NLI model: %s", NLI_MODEL_ID)
    _nli_model = CrossEncoder(
        NLI_MODEL_ID,
        max_length=NLI_MAX_LENGTH,
        device=_device,   # "cuda" or "cpu" — sentence-transformers 3.x requires string, not -1
        # PI: add automodel_args={"load_in_8bit": True} for 8-bit quant
        #     (requires bitsandbytes; saves ~220 MB VRAM for DeBERTa)
    )

    log.info("Warm-up pass…")
    _embed_model.encode(["warm-up"], batch_size=1)
    _nli_model.predict([("warm-up premise", "warm-up hypothesis")])
    log.info("ML daemon ready — device=%s", _device)

    yield

    log.info("ML daemon shutting down")


# ---------------------------------------------------------------------------
# App
# ---------------------------------------------------------------------------

app = FastAPI(
    title="ML Daemon",
    version="0.5b",
    description="Embed + NLI inference for the §5c verifier pipeline",
    lifespan=lifespan,
)


def _require_models() -> None:
    if _embed_model is None or _nli_model is None:
        raise HTTPException(status_code=503, detail="Models not yet loaded")


@app.get("/", response_model=HealthResponse, tags=["meta"])
def health() -> Any:
    return HealthResponse(
        status="ok",
        cuda=torch.cuda.is_available(),
        device=_device,
        models_loaded=(_embed_model is not None and _nli_model is not None),
    )


@app.post("/embed", response_model=EmbedResponse, tags=["inference"])
def embed(req: EmbedRequest) -> Any:
    """
    Returns L2-normalised sentence embeddings.
    MiniLM-L6-v2 → 384-dim.

    PI: toggle normalize_embeddings=False for raw embeddings if your
        downstream similarity metric is not cosine.
    PI: raise EMBED_BATCH_SIZE toward 256 for higher GPU utilisation.
    """
    _require_models()
    vecs = _embed_model.encode(  # type: ignore[union-attr]
        req.texts,
        batch_size=EMBED_BATCH_SIZE,
        convert_to_numpy=True,
        normalize_embeddings=True,   # PI: toggle
        show_progress_bar=False,
    )
    return EmbedResponse(
        embeddings=vecs.tolist(),
        dim=int(vecs.shape[1]),
        model=EMBED_MODEL_ID,
    )


@app.post("/nli", response_model=NLIResponse, tags=["inference"])
def nli(req: NLIRequest) -> Any:
    """
    Scores (source, claim) pair as entailment / neutral / contradiction.

    source → premise; claim → hypothesis.
    Logit order: see _NLI_LABELS constant above.

    PI: for batch NLI (multiple claims against one source passage),
        extend the schema in Layer 1b and call predict() with a list
        of pairs — CrossEncoder handles batches natively.
    PI: apply_softmax=False to get raw logits if you need them for
        calibration work.
    """
    _require_models()
    scores: list[float] = _nli_model.predict(  # type: ignore[union-attr]
        [(req.source, req.claim)],
        apply_softmax=True,
        convert_to_numpy=True,
    )[0].tolist()

    all_scores = {lbl: round(float(s), 6) for lbl, s in zip(_NLI_LABELS, scores)}
    top_idx = int(max(range(len(scores)), key=lambda i: scores[i]))

    return NLIResponse(
        label=_NLI_LABELS[top_idx],
        score=round(scores[top_idx], 6),
        all_scores=all_scores,
        model=NLI_MODEL_ID,
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("tools.ml_daemon:app", host="127.0.0.1", port=5001, reload=False)
