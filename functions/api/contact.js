/**
 * Contact-form handler for Cloudflare Pages.
 *
 * Receives POST submissions from /contact/, validates the Cloudflare
 * Turnstile bot-check token, sanity-checks the fields, sends an email
 * to the site owner via Resend, and redirects the visitor to the
 * thank-you page. On failure, redirects back to /contact/?error=<code>.
 *
 * Required environment variables (configure in the Pages project's
 * Settings → Environment variables):
 *
 *   TURNSTILE_SECRET_KEY   — secret half of the Turnstile site key pair.
 *   RESEND_API_KEY         — Resend account API key (free tier is enough).
 *   CONTACT_TO             — destination email (luke@lukesimmonsnz.kiwi).
 *   CONTACT_FROM           — verified sender, e.g. form@lukesimmonsnz.kiwi.
 *
 * The matching public TURNSTILE_SITE_KEY is embedded in the frozen HTML
 * by the Flask template — it's public and not sensitive.
 */

const VALID_TOPICS = new Set([
  "david-simmons", "research", "projects", "blog", "correction", "other",
]);

const MAX_NAME = 200;
const MAX_EMAIL = 320;   // RFC upper bound
const MAX_MESSAGE = 10_000;

function redirect(url, status = 303) {
  return new Response(null, { status, headers: { Location: url } });
}

function badRequest(origin, code) {
  return redirect(`${origin}/contact/?error=${encodeURIComponent(code)}`);
}

async function verifyTurnstile(token, ip, secret) {
  const body = new URLSearchParams();
  body.set("secret", secret);
  body.set("response", token);
  if (ip) body.set("remoteip", ip);
  const res = await fetch("https://challenges.cloudflare.com/turnstile/v0/siteverify", {
    method: "POST",
    body,
  });
  if (!res.ok) return false;
  const data = await res.json();
  return Boolean(data?.success);
}

function sanitize(s) {
  if (typeof s !== "string") return "";
  return s.replace(/\r\n?/g, "\n").trim();
}

async function sendViaResend({ apiKey, from, to, replyTo, subject, text }) {
  const res = await fetch("https://api.resend.com/emails", {
    method: "POST",
    headers: {
      Authorization: `Bearer ${apiKey}`,
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      from,
      to: [to],
      reply_to: replyTo,
      subject,
      text,
    }),
  });
  return res.ok;
}

export async function onRequestPost({ request, env }) {
  const url = new URL(request.url);
  const origin = `${url.protocol}//${url.host}`;

  let form;
  try {
    form = await request.formData();
  } catch {
    return badRequest(origin, "bad-request");
  }

  const name    = sanitize(form.get("name"));
  const email   = sanitize(form.get("email"));
  const topic   = sanitize(form.get("topic"));
  const message = sanitize(form.get("message"));
  const token   = sanitize(form.get("cf-turnstile-response"));

  if (!name || name.length > MAX_NAME)            return badRequest(origin, "name");
  if (!email || email.length > MAX_EMAIL)         return badRequest(origin, "email");
  if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email))  return badRequest(origin, "email-format");
  if (!topic || !VALID_TOPICS.has(topic))         return badRequest(origin, "topic");
  if (!message || message.length > MAX_MESSAGE)   return badRequest(origin, "message");
  if (!token)                                     return badRequest(origin, "turnstile-missing");

  // IP is used only for the Turnstile siteverify call (their anti-bot
  // heuristics want it) and is NOT propagated into the email body.
  const ip = request.headers.get("CF-Connecting-IP") || "";
  const ok = await verifyTurnstile(token, ip, env.TURNSTILE_SECRET_KEY);
  if (!ok) return badRequest(origin, "turnstile-failed");

  const subject = `[lukesimmonsnz.kiwi · ${topic}] ${name}`;
  const text =
    `New message from the contact form.\n\n` +
    `Name:    ${name}\n` +
    `Email:   ${email}\n` +
    `Topic:   ${topic}\n\n` +
    `---\n${message}\n---\n`;

  const sent = await sendViaResend({
    apiKey: env.RESEND_API_KEY,
    from:   env.CONTACT_FROM || "form@lukesimmonsnz.kiwi",
    to:     env.CONTACT_TO   || "luke@lukesimmonsnz.kiwi",
    replyTo: email,
    subject,
    text,
  });

  if (!sent) return badRequest(origin, "send-failed");

  return redirect(`${origin}/contact/thanks/`);
}

export async function onRequestGet({ request }) {
  // GETs on /api/contact just bounce to the form.
  const url = new URL(request.url);
  return redirect(`${url.protocol}//${url.host}/contact/`);
}
