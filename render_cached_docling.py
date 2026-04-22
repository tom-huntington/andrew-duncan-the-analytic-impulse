from __future__ import annotations

import argparse
import html as html_lib
import json
import re
import shutil
import subprocess
from pathlib import Path

from docling_core.types.doc import DoclingDocument, ImageRef, ImageRefMode
from docling_core.types.doc.base import Size
from PIL import Image


DOCUMENT_PATH = Path("cache/docling-formula/document.json")
MATHML_FORMULA_RE = re.compile(
    r"(?P<wrapper><div>)?"
    r"(?P<math><math\b[^>]*\bdisplay=\"(?P<display>inline|block)\"[^>]*>.*?"
    r"<annotation\b[^>]*\bencoding=\"TeX\"[^>]*>(?P<tex>.*?)</annotation>.*?</math>)"
    r"(?(wrapper)</div>)",
    re.DOTALL,
)
INLINE_DOLLAR_FORMULA_RE = re.compile(
    r"(?<!\\)\$(?P<tex>[^$\n]+?)(?<!\\)\$"
)
HTML_TAG_RE = re.compile(r"(<[^>]+>)")
READING_WIDTH_CH = 72
KATEX_ASSET_DIR = "katex"
HTML_HEAD_TEMPLATE = """\
{katex_stylesheet}
<style>
body {{
  max-width: {reading_width}ch;
  margin: 2rem auto;
  padding: 0 1rem;
  line-height: 1.55;
}}
figure {{
  margin: 1.5rem auto;
  text-align: center;
}}
figure img {{
  display: block;
  max-width: min(100%, 720px);
  height: auto;
  margin: 0 auto 0.5rem;
}}
figcaption {{
  font-size: 0.95rem;
}}
.formula {{
  overflow-x: auto;
}}
</style>"""


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Render Markdown and HTML from the formula-enriched Docling cache."
    )
    parser.add_argument(
        "--output-dir",
        default="output",
        help="Directory to write the Markdown and HTML outputs.",
    )
    parser.add_argument(
        "--output-stem",
        help="Filename stem for the rendered outputs. Defaults to the Docling document name.",
    )
    parser.add_argument(
        "--html-formulas",
        choices=["katex", "mathml"],
        default="katex",
        help="Formula renderer to use in the HTML output.",
    )
    parser.add_argument(
        "--source-image-dir",
        default="The Analytic Impulse_files",
        help="Directory containing source page JPEGs to crop Docling pictures from.",
    )
    parser.add_argument(
        "--picture-padding",
        type=int,
        default=8,
        help="Pixels of padding to add around cropped pictures.",
    )
    return parser.parse_args()


def safe_output_stem(value: str) -> str:
    stem = "".join(ch if ch.isalnum() or ch in " ._-" else "_" for ch in value).strip()
    return stem or "document"


def render_katex(tex: str, display_mode: bool) -> str:
    script = """
const katex = require("katex");
const input = JSON.parse(process.argv[1]);
process.stdout.write(katex.renderToString(input.tex, {
  displayMode: input.displayMode,
  throwOnError: false
}));
"""
    payload = json.dumps({"tex": tex, "displayMode": display_mode})
    try:
        result = subprocess.run(
            ["node", "-e", script, payload],
            check=True,
            capture_output=True,
            encoding="utf-8",
            text=True,
        )
    except FileNotFoundError as exc:
        raise RuntimeError(
            "Build-time KaTeX rendering requires Node.js to be available on PATH."
        ) from exc
    except subprocess.CalledProcessError as exc:
        stderr = exc.stderr.strip()
        if "Cannot find module 'katex'" in stderr:
            raise RuntimeError(
                "Build-time KaTeX rendering requires the Node package 'katex'. "
                "Install it with: npm install"
            ) from exc
        raise RuntimeError(f"KaTeX build-time render failed: {stderr}") from exc

    return result.stdout


def mathml_to_katex(html: str) -> str:
    def replace_formula(match: re.Match[str]) -> str:
        tex = html_lib.unescape(match.group("tex"))
        display = match.group("display")
        rendered = render_katex(tex, display_mode=display == "block")
        if display == "inline":
            return f'<span class="formula">{rendered}</span>'

        return f'<div class="formula">{rendered}</div>'

    return MATHML_FORMULA_RE.sub(replace_formula, html)


def inline_dollar_math_to_katex(html: str) -> str:
    """Render inline $...$ formulas in text nodes without touching HTML tags."""

    def replace_formula(match: re.Match[str]) -> str:
        tex = html_lib.unescape(match.group("tex"))
        return f'<span class="formula">{render_katex(tex, display_mode=False)}</span>'

    parts = HTML_TAG_RE.split(html)
    rendered_parts: list[str] = []
    skip_text = False
    for part in parts:
        if not part:
            continue

        if part.startswith("<") and part.endswith(">"):
            tag = part.lower()
            if tag.startswith("<script") or tag.startswith("<style"):
                skip_text = True
            elif tag.startswith("</script") or tag.startswith("</style"):
                skip_text = False
            rendered_parts.append(part)
            continue

        rendered_parts.append(
            part if skip_text else INLINE_DOLLAR_FORMULA_RE.sub(replace_formula, part)
        )

    return "".join(rendered_parts)


def sorted_source_images(source_image_dir: Path) -> list[Path]:
    def sort_key(path: Path) -> tuple[str, int | str]:
        match = re.search(r"(\d+)$", path.stem)
        if match:
            return (path.stem[: match.start()], int(match.group(1)))
        return (path.stem, path.stem)

    image_paths = [
        *source_image_dir.glob("*.jpg"),
        *source_image_dir.glob("*.jpeg"),
        *source_image_dir.glob("*.png"),
    ]
    return sorted(image_paths, key=sort_key)


def crop_picture_images(
    *,
    document_json: dict,
    source_image_dir: Path,
    output_image_dir: Path,
    html_path: Path,
    padding: int,
) -> list[tuple[int, str, int, int]]:
    source_images = sorted_source_images(source_image_dir)
    if not source_images:
        return []

    output_image_dir.mkdir(parents=True, exist_ok=True)
    image_refs: list[tuple[int, str, int, int]] = []
    pictures = document_json.get("pictures", [])
    for picture_index, picture in enumerate(pictures):
        prov = picture.get("prov") or []
        if not prov:
            continue

        page_no = prov[0].get("page_no")
        if not isinstance(page_no, int) or page_no < 1 or page_no > len(source_images):
            continue

        bbox = prov[0].get("bbox") or {}
        source_path = source_images[page_no - 1]
        with Image.open(source_path) as page_image:
            width, height = page_image.size
            left = max(0, int(bbox.get("l", 0)) - padding)
            right = min(width, int(bbox.get("r", width)) + padding)
            top = max(0, int(height - bbox.get("t", height)) - padding)
            bottom = min(height, int(height - bbox.get("b", 0)) + padding)
            if left >= right or top >= bottom:
                continue

            output_path = output_image_dir / f"picture_{picture_index + 1:02d}.jpeg"
            crop = page_image.crop((left, top, right, bottom)).convert("RGB")
            crop.save(
                output_path,
                "JPEG",
                quality=92,
                optimize=True,
            )
            crop_width, crop_height = crop.size

        image_refs.append(
            (
                picture_index,
                output_path.relative_to(html_path.parent).as_posix(),
                crop_width,
                crop_height,
            )
        )

    return image_refs


def add_picture_image_refs(
    doc: DoclingDocument, image_refs: list[tuple[int, str, int, int]]
) -> None:
    for picture_index, image_src, width, height in image_refs:
        doc.pictures[picture_index].image = ImageRef(
            mimetype="image/jpeg",
            dpi=72,
            size=Size(width=width, height=height),
            uri=Path(image_src),
        )


def copy_katex_assets(output_dir: Path) -> str:
    katex_dist = Path("node_modules/katex/dist")
    stylesheet = katex_dist / "katex.min.css"
    fonts = katex_dist / "fonts"
    if not stylesheet.exists() or not fonts.exists():
        raise RuntimeError(
            "Local KaTeX assets were not found. Install dependencies with: npm install"
        )

    asset_dir = output_dir / KATEX_ASSET_DIR
    asset_dir.mkdir(parents=True, exist_ok=True)
    shutil.copy2(stylesheet, asset_dir / stylesheet.name)
    shutil.copytree(fonts, asset_dir / "fonts", dirs_exist_ok=True)
    return f"{KATEX_ASSET_DIR}/{stylesheet.name}"


def main() -> None:
    args = parse_args()
    document_path = DOCUMENT_PATH.resolve()
    if not document_path.exists():
        raise FileNotFoundError(f"Formula-enriched Docling cache not found: {document_path}")

    output_dir = Path(args.output_dir).resolve()
    output_dir.mkdir(parents=True, exist_ok=True)

    doc = DoclingDocument.load_from_json(document_path)
    doc.validate_document()

    output_stem = safe_output_stem(args.output_stem or doc.name)
    markdown_path = output_dir / f"{output_stem}.md"
    html_path = output_dir / f"{output_stem}.html"
    image_dir = output_dir / f"{output_stem}_images"
    document_json = json.loads(document_path.read_text(encoding="utf-8"))
    image_refs = crop_picture_images(
        document_json=document_json,
        source_image_dir=Path(args.source_image_dir).resolve(),
        output_image_dir=image_dir,
        html_path=html_path,
        padding=args.picture_padding,
    )
    add_picture_image_refs(doc, image_refs)

    markdown = doc.export_to_markdown(
        image_mode=ImageRefMode.REFERENCED if image_refs else ImageRefMode.PLACEHOLDER,
        page_break_placeholder=None,
    )
    katex_stylesheet = ""
    if args.html_formulas == "katex":
        katex_stylesheet = (
            '<link rel="stylesheet" '
            f'href="{copy_katex_assets(output_dir)}">'
        )

    html_head = HTML_HEAD_TEMPLATE.format(
        katex_stylesheet=katex_stylesheet,
        reading_width=READING_WIDTH_CH,
    )
    html = doc.export_to_html(
        image_mode=ImageRefMode.REFERENCED if image_refs else ImageRefMode.PLACEHOLDER,
        split_page_view=False,
        formula_to_mathml=True,
        html_head=html_head,
    )
    html = html.replace("%5C", "/")
    if args.html_formulas == "katex":
        html = mathml_to_katex(html)
        html = inline_dollar_math_to_katex(html)

    markdown_path.write_text(markdown.rstrip() + "\n", encoding="utf-8")
    html_path.write_text(html, encoding="utf-8")

    print(f"Read Docling cache: {document_path}")
    print(f"Wrote Markdown: {markdown_path}")
    print(f"Wrote HTML: {html_path}")
    print(f"Wrote picture JPEGs: {len(image_refs)}")


if __name__ == "__main__":
    main()
