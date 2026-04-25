from flask import Blueprint, render_template

research_bp = Blueprint("research", __name__)


@research_bp.route("/")
def index():
    return render_template("research/index.html")


@research_bp.route("/computer-science/")
def cs_index():
    return render_template("research/computer_science/index.html")


@research_bp.route("/computer-science/python/")
def cs_python():
    return render_template("research/computer_science/python.html")


@research_bp.route("/computer-science/rust/")
def cs_rust():
    return render_template("research/computer_science/rust.html")


@research_bp.route("/computer-science/ai-it-ecosystem/")
def cs_ai_it():
    return render_template("research/computer_science/ai_it_ecosystem.html")


@research_bp.route("/computer-science/references/")
def cs_references():
    return render_template("research/computer_science/references.html")


@research_bp.route("/computer-science/readme/")
def cs_readme():
    return render_template("research/computer_science/readme.html")


# ---- Climate Science & AI ---------------------------------------------------

@research_bp.route("/climate-science-and-ai/")
def climate_index():
    return render_template("research/climate_science/index.html")


@research_bp.route("/climate-science-and-ai/intro/")
def climate_intro():
    return render_template("research/climate_science/intro.html")


@research_bp.route("/climate-science-and-ai/history/")
def climate_history():
    return render_template("research/climate_science/history.html")


@research_bp.route("/climate-science-and-ai/methods/")
def climate_methods():
    return render_template("research/climate_science/methods.html")


@research_bp.route("/climate-science-and-ai/applications/")
def climate_applications():
    return render_template("research/climate_science/applications.html")


@research_bp.route("/climate-science-and-ai/challenges/")
def climate_challenges():
    return render_template("research/climate_science/challenges.html")


@research_bp.route("/climate-science-and-ai/future/")
def climate_future():
    return render_template("research/climate_science/future.html")


@research_bp.route("/climate-science-and-ai/references/")
def climate_references():
    return render_template("research/climate_science/references.html")


# ---- Medical Science --------------------------------------------------------

@research_bp.route("/medical-science/")
def medsci_index():
    return render_template("research/medical_science/index.html")


@research_bp.route("/medical-science/neuroscience-ai/")
def medsci_neuroscience():
    return render_template("research/medical_science/neuroscience_ai.html")


@research_bp.route("/medical-science/bioinformatics/")
def medsci_bioinformatics():
    return render_template("research/medical_science/bioinformatics.html")


@research_bp.route("/medical-science/medical-imaging/")
def medsci_imaging():
    return render_template("research/medical_science/medical_imaging.html")


@research_bp.route("/medical-science/clinical-ai/")
def medsci_clinical():
    return render_template("research/medical_science/clinical_ai.html")


@research_bp.route("/medical-science/drug-discovery/")
def medsci_drugs():
    return render_template("research/medical_science/drug_discovery.html")


@research_bp.route("/medical-science/references/")
def medsci_references():
    return render_template("research/medical_science/references.html")
