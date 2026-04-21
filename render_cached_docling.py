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
FORMULA_REPLACEMENTS = {
    r"e ^ { j \omega t } = \cos ( \omega t ) \, + \, _ { j } \, \sin ( \omega t ) \, .": (
        r"e ^ { j \omega t } = \cos ( \omega t ) \, + \, j \, \sin ( \omega t ) \, ."
    ),
    r"\cos ( \omega t ) = \frac { e ^ { j \omega t } + e ^ { - j \omega t } } { 2 } & & \frac { a \text { speed} } { 3 } & & \frac { \text {difference} } { 2 } & & \frac { ( 3 ) } { 2 } & & \text {real} & & \text {analy}": (
        r"\cos ( \omega t ) = \frac { e ^ { j \omega t } + e ^ { - j \omega t } } { 2 }"
    ),
    r"f ( t ) & = \frac { \sin ( \pi t ) } { \pi t } + j \, \frac { 1 - \cos ( \pi t ) } { \pi t } \\ & = \left [ \frac { e ^ { j t } - 1 } { \pi t } \right ] ^ { * } \\ & = \sin ( t ) + j \cdot \cos ( t ) = \, \text {as} ( t ) \, . \quad ( 5 a ) \\ \intertext { s u n t i o n s i m e s a l o s d e r h a s } \intertext { i t }": (
        r"\begin{aligned} f ( t ) & = \frac { \sin ( \pi t ) } { \pi t } + j \, \frac { 1 - \cos ( \pi t ) } { \pi t } \\ & = \left [ \frac { e ^ { j t } - 1 } { \pi t } \right ] ^ { * } \\ & = \sin ( t ) + j \cdot \cos ( t ) = \, \text {as} ( t ) \, . \quad ( 5 a ) \end{aligned}"
    ),
    r"\Delta ( t ) & = \delta ( t ) + j \, \frac { 1 } { \pi t } \quad & \text {can reach} \\ & = \delta ( t ) + j \cdot d ( t ) \ . & \text {trans}": (
        r"\begin{aligned} \Delta ( t ) & = \delta ( t ) + j \, \frac { 1 } { \pi t } \\ & = \delta ( t ) + j \cdot d ( t ) \end{aligned}"
    ),
    r"\Delta _ { \alpha } [ \tau ] & = \frac { \sin ( \pi \tau ) } { \pi \tau } + j \, \frac { 1 \, - \, \cos ( \pi \tau ) } { \pi \tau } \\ & = \left [ \frac { e ^ { j \pi \, \pi } - 1 } { \pi \tau } \right ] ^ { * }": (
        r"\begin{aligned} \Delta _ { \alpha } [ \tau ] & = \frac { \sin ( \pi \tau ) } { \pi \tau } + j \, \frac { 1 \, - \, \cos ( \pi \tau ) } { \pi \tau } \\ & = \left [ \frac { e ^ { j \pi \, \pi } - 1 } { \pi \tau } \right ] ^ { * } \end{aligned}"
    ),
    r"\Delta _ { N } [ \tau ] & = \frac { 1 } { N } \left [ 2 e ^ { j 2 \pi / N } \frac { 1 - e ^ { j \pi \tau } } { 1 - e ^ { j 2 \pi / N } } + ( 1 - e ^ { j \pi \tau } ) \right ] \\ & = \begin{cases} 1 , & \tau = 0 \\ j \frac { 2 } { N } \cot \left ( \frac { \pi \tau } { N } \right ) , & \tau \text { odd} \quad [ 5 , p . 3 5 ] \\ 0 , & \tau \text { even } \neq 0 \end{cases}": (
        r"\begin{aligned} \Delta _ { N } [ \tau ] & = \frac { 1 } { N } \left [ 2 e ^ { j 2 \pi / N } \frac { 1 - e ^ { j \pi \tau } } { 1 - e ^ { j 2 \pi / N } } + ( 1 - e ^ { j \pi \tau } ) \right ] \\ & = \begin{cases} 1 , & \tau = 0 \\ j \frac { 2 } { N } \cot \left ( \frac { \pi \tau } { N } \right ) , & \tau \text { odd} \quad [ 5 , p . 3 5 ] \\ 0 , & \tau \text { even } \neq 0 \end{cases} \end{aligned}"
    ),
    r"\text {lled} \quad & \quad \text {the} \quad \text {smoother AIR} ( t ) \, = \, \mathbb { F } ^ { - 1 } \{ \mathcal { F } \left \{ \Delta ( t ) \{ W ( f ) H ( f ) \} \right \} \\ \text {Fig.} \quad & \quad \text {main.} \quad & = \, \mathbb { F } ^ { - 1 } \left \{ [ \mathcal { F } \{ \Delta ( t ) \} \, W ( f ) ] \ H ( f ) \right \} \\ \text {pe-} \quad & \quad \text {mat.} \quad & = \, \mathbb { F } ^ { - 1 } \left \{ \mathcal { F } \{ \widehat { \Delta } ( t ) \} H ( f ) \right \} \\ \text {the} \quad & \quad \text {win-} \quad & = \, \widetilde { \Delta } ( t ) \, * \, h ( t ) \quad & ( 1 0 ) \\ \text {and a} \quad & \quad \text {in} \quad & = \, \mathbb { F } ^ { - 1 } \{ \mathcal { F } ( t ) \, \text {is the window function} \, \text {equiv.} \quad &": (
        r"\begin{aligned} \text {smoother AIR} ( t ) & = \mathbb { F } ^ { - 1 } \left \{ [ \mathcal { F } \{ \Delta ( t ) \} \, W ( f ) ] H ( f ) \right \} \\ & = \mathbb { F } ^ { - 1 } \left \{ \mathcal { F } \{ \widehat { \Delta } ( t ) \} H ( f ) \right \} \\ & = \widetilde { \Delta } ( t ) \ast h ( t ) \quad ( 1 0 ) \end{aligned}"
    ),
    r"F ( f ) & = \int _ { - x } ^ { x } f ( t ) \, e ^ { - j 2 \pi f l } \, d t \, , & f & & & f [ t ] = \int _ { - x } ^ { x } F ( f ) \, e ^ { j 2 \pi f l } \, d f \\ f ( t ) & = \int _ { - x } ^ { x } F ( f ) \, e ^ { j 2 \pi f l } \, d f & & & ( 1 2 )": (
        r"\begin{aligned} F ( f ) & = \int _ { - \infty } ^ { \infty } f ( t ) \, e ^ { - j 2 \pi f t } \, d t \\ f ( t ) & = \int _ { - \infty } ^ { \infty } F ( f ) \, e ^ { j 2 \pi f t } \, d f \quad ( 1 2 ) \end{aligned}"
    ),
}


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


def sanitize_tex(tex: str) -> str:
    tex = FORMULA_REPLACEMENTS.get(tex, tex)
    tex = tex.replace(r"_ { j }", "j")
    tex = re.sub(r"(?:\\ ){2,}", r"\\quad ", tex)
    tex = re.sub(r"(?:\s*\\quad\b\s*)+\\?\s*$", "", tex).strip()

    return tex


def mathml_to_katex(html: str) -> str:
    def replace_formula(match: re.Match[str]) -> str:
        tex = sanitize_tex(html_lib.unescape(match.group("tex")))
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
