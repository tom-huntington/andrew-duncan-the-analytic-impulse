from __future__ import annotations

import argparse
import html as html_lib
import json
import re
import subprocess
from pathlib import Path

from docling_core.types.doc import DoclingDocument, ImageRefMode


DOCUMENT_PATH = Path("cache/docling-formula/document.json")
MATHML_FORMULA_RE = re.compile(
    r"(?P<wrapper><div>)?"
    r"(?P<math><math\b[^>]*\bdisplay=\"(?P<display>inline|block)\"[^>]*>.*?"
    r"<annotation\b[^>]*\bencoding=\"TeX\"[^>]*>(?P<tex>.*?)</annotation>.*?</math>)"
    r"(?(wrapper)</div>)",
    re.DOTALL,
)
KATEX_HEAD = """\
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex@0.16.45/dist/katex.min.css">"""


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

    markdown = doc.export_to_markdown(
        image_mode=ImageRefMode.PLACEHOLDER,
        page_break_placeholder=None,
    )
    html_head = KATEX_HEAD if args.html_formulas == "katex" else "null"
    html = doc.export_to_html(
        image_mode=ImageRefMode.PLACEHOLDER,
        split_page_view=False,
        formula_to_mathml=True,
        html_head=html_head,
    )
    if args.html_formulas == "katex":
        html = mathml_to_katex(html)

    markdown_path.write_text(markdown.rstrip() + "\n", encoding="utf-8")
    html_path.write_text(html, encoding="utf-8")

    print(f"Read Docling cache: {document_path}")
    print(f"Wrote Markdown: {markdown_path}")
    print(f"Wrote HTML: {html_path}")


if __name__ == "__main__":
    main()
