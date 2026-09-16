from __future__ import annotations

import argparse
import base64
import html
import io
import json
import hashlib
import shutil
import subprocess
import sys
from pathlib import Path
from urllib.parse import quote

import qrcode


SKILL_DIR = Path(__file__).resolve().parents[1]
TEMPLATE_PATH = SKILL_DIR / "assets" / "template.html"


def esc(value: object) -> str:
    return html.escape(str(value or ""), quote=True)


def svg_uri(svg: str) -> str:
    return "data:image/svg+xml," + quote(svg)


def hero_fallback_uri(accent: str) -> str:
    return svg_uri(
        '<svg xmlns="http://www.w3.org/2000/svg" width="1600" height="900" viewBox="0 0 1600 900">'
        '<defs><radialGradient id="g" cx="78%" cy="45%" r="55%">'
        '<stop stop-color="#263442"/><stop offset="1" stop-color="#070909"/></radialGradient></defs>'
        '<rect width="1600" height="900" fill="url(#g)"/>'
        f'<g fill="none" stroke="{esc(accent)}" stroke-width="3" opacity=".55">'
        '<path d="M930 170C1120 40 1430 90 1530 280S1460 670 1250 730 900 620 870 430 780 280 930 170Z"/>'
        '<path d="M1030 270L1270 180 1460 350 1370 610 1080 650 930 440Z"/>'
        '</g><g fill="#fff" opacity=".72">'
        '<circle cx="1030" cy="270" r="10"/><circle cx="1270" cy="180" r="10"/>'
        '<circle cx="1460" cy="350" r="10"/><circle cx="1370" cy="610" r="10"/>'
        '<circle cx="1080" cy="650" r="10"/><circle cx="930" cy="440" r="10"/>'
        '</g></svg>'
    )


def speaker_avatar_uri(name: str, accent: str) -> str:
    digest = hashlib.sha256(name.encode("utf-8")).digest()
    palettes = [
        ("#16202a", "#8fa8bd"),
        ("#282035", "#b19ac5"),
        ("#17302c", "#89b5a8"),
        ("#35251d", "#c4a18d"),
    ]
    background, person = palettes[digest[0] % len(palettes)]
    return svg_uri(
        '<svg xmlns="http://www.w3.org/2000/svg" width="320" height="320" viewBox="0 0 320 320">'
        f'<rect width="320" height="320" fill="{background}"/>'
        f'<circle cx="160" cy="112" r="62" fill="{person}"/>'
        f'<path d="M45 320c7-91 51-137 115-137s108 46 115 137Z" fill="{person}"/>'
        f'<circle cx="258" cy="62" r="42" fill="{esc(accent)}" opacity=".82"/>'
        '<path d="M81 249c25-29 51-44 79-44s54 15 79 44" fill="none" stroke="#fff" '
        'stroke-width="8" stroke-linecap="round" opacity=".22"/></svg>'
    )


def image_uri(path_value: str, base_dir: Path, fallback_uri: str) -> str:
    if not path_value:
        return fallback_uri
    path = Path(path_value)
    if not path.is_absolute():
        path = base_dir / path
    if not path.is_file():
        raise FileNotFoundError(f"Image not found: {path}")
    suffix = path.suffix.lower()
    mime = {
        ".jpg": "image/jpeg",
        ".jpeg": "image/jpeg",
        ".png": "image/png",
        ".webp": "image/webp",
        ".svg": "image/svg+xml",
    }.get(suffix)
    if not mime:
        raise ValueError(f"Unsupported image format: {suffix}")
    return f"data:{mime};base64,{base64.b64encode(path.read_bytes()).decode('ascii')}"


def qr_uri(url: str) -> str:
    if not url:
        raise ValueError("cta.url is required to generate the QR code")
    qr = qrcode.QRCode(version=None, box_size=12, border=4)
    qr.add_data(url)
    qr.make(fit=True)
    image = qr.make_image(fill_color="black", back_color="white")
    stream = io.BytesIO()
    image.save(stream, format="PNG")
    return f"data:image/png;base64,{base64.b64encode(stream.getvalue()).decode('ascii')}"


def require(data: dict, key: str) -> object:
    value = data.get(key)
    if value in (None, "", []):
        raise ValueError(f"Missing required field: {key}")
    return value


def build_html(data: dict, base_dir: Path) -> str:
    for key in ("brand", "event_day", "event_date", "title", "subtitle", "agenda", "speakers", "audience", "venue", "cta"):
        require(data, key)

    agenda = data["agenda"]
    speakers = data["speakers"]
    audience = data["audience"]
    if not 3 <= len(agenda) <= 5:
        raise ValueError("agenda must contain 3 to 5 items")
    if not 1 <= len(speakers) <= 3:
        raise ValueError("speakers must contain 1 to 3 items")
    if not 3 <= len(audience) <= 4:
        raise ValueError("audience must contain 3 to 4 items")

    agenda_html = "".join(
        f'<div class="agenda-item"><div class="agenda-time">{esc(item.get("time"))}</div>'
        f'<div><div class="agenda-title">{esc(item.get("title"))}</div>'
        f'<div class="agenda-description">{esc(item.get("description"))}</div></div></div>'
        for item in agenda
    )

    speaker_parts = []
    accent = str(data.get("accent", "#E3FF04"))
    for speaker in speakers:
        image = speaker.get("image", "")
        name = str(speaker.get("name", ""))
        image_html = (
            f'<img src="{image_uri(image, base_dir, speaker_avatar_uri(name, accent))}" '
            f'alt="{esc(name)}">'
        )
        speaker_parts.append(
            f'<article class="speaker">{image_html}<div><div class="speaker-name">{esc(speaker.get("name"))}</div>'
            f'<div class="speaker-role">{esc(speaker.get("role"))}</div></div></article>'
        )

    venue = data["venue"]
    features = venue.get("features", [])[:2]
    cta = data["cta"]
    brand_words = str(data["brand"]).split(" ", 1)
    brand_html = (
        f'<span class="brand-mark">{esc(brand_words[0])}</span>{esc(brand_words[1])}'
        if len(brand_words) == 2
        else f'<span class="brand-mark">{esc(brand_words[0])}</span>'
    )

    replacements = {
        "DOCUMENT_TITLE": esc(f'{data["brand"]} – {data["title"]}'),
        "HERO_IMAGE": image_uri(data.get("hero_image", ""), base_dir, hero_fallback_uri(accent)),
        "ACCENT": esc(accent),
        "BRAND_HTML": brand_html,
        "EVENT_DAY": esc(data["event_day"]),
        "EVENT_DATE": esc(data["event_date"]),
        "EYEBROW": esc(data.get("eyebrow", "THEMENSCHWERPUNKT")),
        "TITLE": esc(data["title"]),
        "SUBTITLE": esc(data["subtitle"]),
        "FACTS": "".join(f'<span class="fact">{esc(value)}</span>' for value in data.get("facts", [])[:3]),
        "AGENDA": agenda_html,
        "SPEAKERS": "".join(speaker_parts),
        "SPEAKER_COLUMNS": str(min(len(speakers), 2)),
        "AUDIENCE_TITLE": esc(data.get("audience_title", "Für wen ist das Event?")),
        "AUDIENCE": "".join(f'<div class="audience-item">{esc(value)}</div>' for value in audience),
        "VENUE_NAME": esc(venue.get("name")),
        "VENUE_STREET": esc(venue.get("street")),
        "VENUE_CITY": esc(venue.get("city")),
        "VENUE_FEATURES": "".join(f'<div class="feature">{esc(value)}</div>' for value in features),
        "QR_IMAGE": qr_uri(str(cta.get("url", ""))),
        "CTA_TITLE": esc(cta.get("title", "Platz sichern")),
        "CTA_TEXT": esc(cta.get("text")),
        "CTA_LABEL": esc(cta.get("label") or cta.get("url")),
        "FOOTER_LEFT": esc(data.get("footer_left", "")),
        "FOOTER_RIGHT": esc(data.get("footer_right", "")),
    }
    output = TEMPLATE_PATH.read_text(encoding="utf-8")
    for key, value in replacements.items():
        output = output.replace("{{" + key + "}}", value)
    unresolved = [part.split("}}", 1)[0] for part in output.split("{{")[1:]]
    if unresolved:
        raise RuntimeError(f"Unresolved template placeholders: {', '.join(unresolved)}")
    return output


def find_browser() -> Path:
    candidates = [
        Path(r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"),
        Path(r"C:\Program Files\Microsoft\Edge\Application\msedge.exe"),
        Path(r"C:\Program Files\Google\Chrome\Application\chrome.exe"),
        Path(r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"),
    ]
    command = shutil.which("msedge") or shutil.which("chrome") or shutil.which("chromium")
    if command:
        candidates.insert(0, Path(command))
    for candidate in candidates:
        if candidate.is_file():
            return candidate
    raise FileNotFoundError("No Chromium browser found for PDF rendering")


def render_pdf(html_path: Path, pdf_path: Path) -> None:
    browser = find_browser()
    command = [
        str(browser),
        "--headless",
        "--disable-gpu",
        "--no-pdf-header-footer",
        f"--print-to-pdf={pdf_path.resolve()}",
        html_path.resolve().as_uri(),
    ]
    result = subprocess.run(command, capture_output=True, text=True, timeout=90)
    if result.returncode != 0 or not pdf_path.is_file():
        detail = result.stderr.strip() or result.stdout.strip()
        raise RuntimeError(f"PDF rendering failed: {detail}")


def main() -> int:
    parser = argparse.ArgumentParser(description="Create a fixed-layout A4 event one-pager")
    parser.add_argument("content", type=Path, help="JSON content file")
    parser.add_argument("output", type=Path, help="Output .pdf or .html path")
    parser.add_argument("--html-only", action="store_true", help="Only generate HTML")
    args = parser.parse_args()

    content_path = args.content.resolve()
    data = json.loads(content_path.read_text(encoding="utf-8"))
    output = args.output.resolve()
    html_path = output if output.suffix.lower() == ".html" else output.with_suffix(".html")
    html_path.parent.mkdir(parents=True, exist_ok=True)
    html_path.write_text(build_html(data, content_path.parent), encoding="utf-8")
    print(f"HTML: {html_path}")

    if not args.html_only and output.suffix.lower() != ".html":
        pdf_path = output if output.suffix.lower() == ".pdf" else output.with_suffix(".pdf")
        render_pdf(html_path, pdf_path)
        print(f"PDF: {pdf_path}")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(f"Error: {exc}", file=sys.stderr)
        raise SystemExit(1)
