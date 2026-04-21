from __future__ import annotations

import argparse
from pathlib import Path

from docling_core.types.doc import DoclingDocument, ImageRefMode


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Render Markdown and HTML from a cached Docling document JSON."
    )
    parser.add_argument(
        "--document",
        default="cache/docling/document.json",
        help="Path to the cached single DoclingDocument JSON.",
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
    return parser.parse_args()


def safe_output_stem(value: str) -> str:
    stem = "".join(ch if ch.isalnum() or ch in " ._-" else "_" for ch in value).strip()
    return stem or "document"


def main() -> None:
    args = parse_args()
    document_path = Path(args.document).resolve()
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
    html = doc.export_to_html(
        image_mode=ImageRefMode.PLACEHOLDER,
        split_page_view=False,
    )

    markdown_path.write_text(markdown.rstrip() + "\n", encoding="utf-8")
    html_path.write_text(html, encoding="utf-8")

    print(f"Wrote Markdown: {markdown_path}")
    print(f"Wrote HTML: {html_path}")


if __name__ == "__main__":
    main()
