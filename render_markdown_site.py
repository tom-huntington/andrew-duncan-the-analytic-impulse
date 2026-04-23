from __future__ import annotations

import argparse
import html
import json
import re
import shutil
import subprocess
from pathlib import Path


READING_WIDTH_CH = 72
KATEX_ASSET_DIR = "katex"
IMAGE_ASSET_DIR = "images"
DEFAULT_IMAGE_SOURCE_DIR = Path("output/the-analytic-impulse_images")
FIGURE_CAPTION_RE = re.compile(r"^Fig\.\s+\d+\.\s+")
IMAGE_RE = re.compile(r"^!\[(?P<alt>[^\]]*)\]\((?P<src>[^)]+)\)\s*$")
INLINE_MATH_RE = re.compile(r"(?<!\\)\$(?P<tex>[^$\n]+?)(?<!\\)\$")
DISPLAY_MATH_RE = re.compile(r"^\$\$(?P<tex>.*)\$\$\s*$")
DISPLAY_MATH_DELIMITER = "$$"
HTML_HEAD_TEMPLATE = """\
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
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
span.formula > .katex {{
  font-size: 1em;
}}
</style>
</head>
<body>
<div class="page">
"""


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Render docs/index.html from docs/paper.md as the source of truth."
    )
    parser.add_argument(
        "--input",
        default="docs/paper.md",
        help="Markdown source file. Defaults to docs/paper.md.",
    )
    parser.add_argument(
        "--output-dir",
        default="docs",
        help="Directory to write the site into. Defaults to docs.",
    )
    parser.add_argument(
        "--html-output",
        default="index.html",
        help="HTML filename to write inside the output directory.",
    )
    parser.add_argument(
        "--title",
        default="The Analytic Impulse",
        help="HTML document title.",
    )
    parser.add_argument(
        "--image-source-dir",
        default=str(DEFAULT_IMAGE_SOURCE_DIR),
        help=(
            "Directory containing source images to copy into the site. "
            "Defaults to output/the-analytic-impulse_images."
        ),
    )
    return parser.parse_args()


def normalize_tex(tex: str) -> str:
    # Docling's Markdown escapes underscores inside math for Markdown safety.
    return tex.replace(r"\_", "_").strip()


def render_katex(tex: str, display_mode: bool) -> str:
    script = """
const katex = require("katex");
const input = JSON.parse(process.argv[1]);
process.stdout.write(katex.renderToString(input.tex, {
  displayMode: input.displayMode,
  throwOnError: false
}));
"""
    payload = json.dumps({"tex": normalize_tex(tex), "displayMode": display_mode})
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


def render_inline(text: str) -> str:
    escaped = html.escape(text)

    def replace_math(match: re.Match[str]) -> str:
        return (
            '<span class="formula">'
            f"{render_katex(html.unescape(match.group('tex')), display_mode=False)}"
            "</span>"
        )

    return INLINE_MATH_RE.sub(replace_math, escaped)


def render_display_math(tex: str) -> str:
    return f'<div class="formula">{render_katex(tex, display_mode=True)}</div>'


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


def prepare_output_dir(output_dir: Path) -> None:
    if output_dir.exists() and not output_dir.is_dir():
        raise NotADirectoryError(f"Output path is not a directory: {output_dir}")
    output_dir.mkdir(parents=True, exist_ok=True)


def copy_image_assets(image_source_dir: Path, output_dir: Path) -> None:
    if not image_source_dir.exists() or not image_source_dir.is_dir():
        raise FileNotFoundError(f"Image source directory not found: {image_source_dir}")

    shutil.copytree(image_source_dir, output_dir / IMAGE_ASSET_DIR, dirs_exist_ok=True)


def copy_markdown_source(markdown_path: Path, output_dir: Path) -> Path:
    copied_path = output_dir / markdown_path.name
    if markdown_path.resolve() == copied_path.resolve():
        return copied_path
    shutil.copy2(markdown_path, copied_path)
    return copied_path


def normalize_image_src(src: str) -> str:
    for source_dir_name in (
        DEFAULT_IMAGE_SOURCE_DIR.name,
        "The Analytic Impulse_images",
    ):
        prefix = f"{source_dir_name}/"
        if src.startswith(prefix):
            return f"{IMAGE_ASSET_DIR}/{src.removeprefix(prefix)}"
    return src


def paragraph_from_lines(lines: list[str]) -> str:
    text = " ".join(line.strip() for line in lines)
    return f"<p>{render_inline(text)}</p>"


def image_alt_from_caption(caption: str, fallback: str) -> str:
    if not FIGURE_CAPTION_RE.match(caption):
        return fallback

    alt = FIGURE_CAPTION_RE.sub("", caption).rstrip(".")
    alt = re.sub(r"\s+with different attack times$", "", alt)
    alt = alt.replace("$", "").replace(r"\_", "_")
    return alt or fallback


def render_markdown(markdown: str) -> str:
    lines = markdown.splitlines()
    output: list[str] = []
    paragraph: list[str] = []
    list_items: list[str] = []
    i = 0

    def flush_paragraph() -> None:
        nonlocal paragraph
        if paragraph:
            output.append(paragraph_from_lines(paragraph))
            paragraph = []

    def flush_list() -> None:
        nonlocal list_items
        if list_items:
            output.append("<ul>")
            output.extend(f"<li>{render_inline(item)}</li>" for item in list_items)
            output.append("</ul>")
            list_items = []

    while i < len(lines):
        line = lines[i]
        stripped = line.strip()

        if not stripped:
            flush_paragraph()
            flush_list()
            i += 1
            continue

        if stripped.startswith("<") and stripped.endswith(">"):
            flush_paragraph()
            flush_list()
            output.append(stripped)
            i += 1
            continue

        math_match = DISPLAY_MATH_RE.match(stripped)
        if math_match:
            flush_paragraph()
            flush_list()
            output.append(render_display_math(math_match.group("tex")))
            i += 1
            continue

        if stripped == DISPLAY_MATH_DELIMITER:
            flush_paragraph()
            flush_list()
            math_lines: list[str] = []
            i += 1
            while i < len(lines) and lines[i].strip() != DISPLAY_MATH_DELIMITER:
                math_lines.append(lines[i])
                i += 1
            if i >= len(lines):
                raise ValueError("Unclosed display math block")
            output.append(render_display_math("\n".join(math_lines)))
            i += 1
            continue

        if stripped.startswith("## "):
            flush_paragraph()
            flush_list()
            output.append(f"<h2>{render_inline(stripped[3:].strip())}</h2>")
            i += 1
            continue

        if stripped.startswith("- "):
            flush_paragraph()
            list_items.append(stripped[2:].strip())
            i += 1
            continue

        image_match = IMAGE_RE.match(stripped)
        if image_match:
            flush_paragraph()
            flush_list()
            alt = image_match.group("alt")
            src = normalize_image_src(image_match.group("src"))
            output.append(
                '<figure>'
                f'<img src="{html.escape(src, quote=True)}" '
                f'alt="{html.escape(alt, quote=True)}">'
                "</figure>"
            )
            i += 1
            continue

        next_caption_image = (
            FIGURE_CAPTION_RE.match(stripped)
            and i + 2 < len(lines)
            and not lines[i + 1].strip()
            and IMAGE_RE.match(lines[i + 2].strip())
        )
        if next_caption_image:
            flush_paragraph()
            flush_list()
            image_match = IMAGE_RE.match(lines[i + 2].strip())
            assert image_match is not None
            src = normalize_image_src(image_match.group("src"))
            alt = image_alt_from_caption(stripped, image_match.group("alt"))
            output.append(
                "<figure>"
                f'<img src="{html.escape(src, quote=True)}" '
                f'alt="{html.escape(alt, quote=True)}">'
                f"<figcaption>{render_inline(stripped)}</figcaption>"
                "</figure>"
            )
            i += 3
            continue

        paragraph.append(line)
        i += 1

    flush_paragraph()
    flush_list()
    return "\n".join(output)


def render_site(
    markdown_path: Path,
    output_dir: Path,
    html_filename: str,
    title: str,
    image_source_dir: Path,
) -> Path:
    if not markdown_path.exists():
        raise FileNotFoundError(f"Markdown source not found: {markdown_path}")

    prepare_output_dir(output_dir)
    copy_markdown_source(markdown_path, output_dir)
    copy_image_assets(image_source_dir, output_dir)
    katex_stylesheet = (
        '<link rel="stylesheet" '
        f'href="{copy_katex_assets(output_dir)}">'
    )
    body = render_markdown(markdown_path.read_text(encoding="utf-8"))
    html_output = (
        HTML_HEAD_TEMPLATE.format(
            title=html.escape(title),
            katex_stylesheet=katex_stylesheet,
            reading_width=READING_WIDTH_CH,
        )
        + body
        + "\n</div>\n</body>\n</html>\n"
    )

    html_path = output_dir / Path(html_filename).name
    html_path.write_text(html_output, encoding="utf-8")
    return html_path


def main() -> None:
    args = parse_args()
    html_path = render_site(
        markdown_path=Path(args.input).resolve(),
        output_dir=Path(args.output_dir).resolve(),
        html_filename=args.html_output,
        title=args.title,
        image_source_dir=Path(args.image_source_dir).resolve(),
    )
    print(f"Read Markdown: {Path(args.input).resolve()}")
    print(f"Copied Markdown: {Path(args.input).resolve()} -> {Path(args.output_dir).resolve() / Path(args.input).name}")
    print(f"Copied images: {Path(args.image_source_dir).resolve()} -> {Path(args.output_dir).resolve() / IMAGE_ASSET_DIR}")
    print(f"Wrote HTML: {html_path}")


if __name__ == "__main__":
    main()
