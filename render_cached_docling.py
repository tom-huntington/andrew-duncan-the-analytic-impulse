from __future__ import annotations

import argparse
import html
import json
import os
import re
from pathlib import Path
from typing import Iterable

from docling_core.types.doc import DoclingDocument, ImageRefMode


BODY_RE = re.compile(r"<body[^>]*>(.*)</body>", re.IGNORECASE | re.DOTALL)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Render Markdown and HTML from cached Docling JSON."
    )
    parser.add_argument(
        "--manifest",
        default="cache/docling/manifest.json",
        help="Path to the cache manifest written by convert_paper_with_docling.py.",
    )
    parser.add_argument(
        "--output-dir",
        default="output",
        help="Directory to write the combined Markdown and HTML outputs.",
    )
    return parser.parse_args()


def load_manifest(manifest_path: Path) -> dict:
    return json.loads(manifest_path.read_text(encoding="utf-8"))


def inner_html(fragment: str) -> str:
    match = BODY_RE.search(fragment)
    if match:
        return match.group(1).strip()
    return fragment.strip()


def build_markdown(title: str, page_blocks: Iterable[tuple[int, str]]) -> str:
    parts = [f"# {title}"]
    for page_num, page_md in page_blocks:
        parts.append(f"## Page {page_num}\n\n{page_md.strip()}")
    return "\n\n---\n\n".join(parts).strip() + "\n"


def build_html(
    title: str, source_name: str, html_output_path: Path, page_blocks: Iterable[tuple[int, str, Path]]
) -> str:
    sections: list[str] = []
    for page_num, page_html, image_path in page_blocks:
        relative_image_path = os.path.relpath(image_path, start=html_output_path.parent).replace("\\", "/")
        sections.append(
            f"""
            <section class="page">
              <header class="page-header">
                <h2>Page {page_num}</h2>
                <p>{html.escape(image_path.name)}</p>
              </header>
              <div class="page-grid">
                <figure class="scan">
                  <img src="{html.escape(relative_image_path)}" alt="Source scan for page {page_num}">
                </figure>
                <article class="ocr">
                  {inner_html(page_html)}
                </article>
              </div>
            </section>
            """.strip()
        )

    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{html.escape(title)}</title>
  <style>
    :root {{
      color-scheme: light;
      --bg: #f5f6f8;
      --surface: #ffffff;
      --border: #d6dbe3;
      --text: #1c2430;
      --muted: #5d6776;
      --accent: #0b6bcb;
    }}
    * {{ box-sizing: border-box; }}
    body {{
      margin: 0;
      font-family: Arial, sans-serif;
      color: var(--text);
      background: var(--bg);
      line-height: 1.55;
    }}
    main {{
      max-width: 1280px;
      margin: 0 auto;
      padding: 24px;
    }}
    .hero {{
      padding: 24px 0 12px;
    }}
    h1, h2, h3 {{
      margin: 0 0 12px;
      line-height: 1.2;
    }}
    p {{
      margin: 0 0 12px;
    }}
    .hero p {{
      color: var(--muted);
      max-width: 72ch;
    }}
    .page {{
      border-top: 1px solid var(--border);
      padding: 24px 0;
    }}
    .page-header {{
      margin-bottom: 16px;
    }}
    .page-header p {{
      color: var(--muted);
      font-size: 14px;
    }}
    .page-grid {{
      display: grid;
      grid-template-columns: minmax(280px, 420px) minmax(0, 1fr);
      gap: 20px;
      align-items: start;
    }}
    .scan,
    .ocr {{
      margin: 0;
      background: var(--surface);
      border: 1px solid var(--border);
      border-radius: 8px;
      overflow: hidden;
    }}
    .scan img {{
      display: block;
      width: 100%;
      height: auto;
    }}
    .ocr {{
      padding: 20px;
    }}
    .ocr table {{
      border-collapse: collapse;
      width: 100%;
    }}
    .ocr th,
    .ocr td {{
      border: 1px solid var(--border);
      padding: 6px 8px;
      vertical-align: top;
    }}
    .ocr a {{
      color: var(--accent);
    }}
    @media (max-width: 900px) {{
      main {{
        padding: 16px;
      }}
      .page-grid {{
        grid-template-columns: 1fr;
      }}
    }}
  </style>
</head>
<body>
  <main>
    <section class="hero">
      <h1>{html.escape(title)}</h1>
      <p>Combined OCR extraction from {html.escape(source_name)} using cached Docling JSON. Each section keeps the source page scan alongside the extracted content.</p>
    </section>
    {"".join(sections)}
  </main>
</body>
</html>
"""


def main() -> None:
    args = parse_args()
    manifest_path = Path(args.manifest).resolve()
    output_dir = Path(args.output_dir).resolve()
    output_dir.mkdir(parents=True, exist_ok=True)

    manifest = load_manifest(manifest_path)
    title = manifest["title"]
    source_name = Path(manifest["source_html"]).name

    md_pages: list[tuple[int, str]] = []
    html_pages: list[tuple[int, str, Path]] = []

    for page in manifest["pages"]:
        doc = DoclingDocument.load_from_json(page["json_path"])
        md_pages.append(
            (
                page["index"],
                doc.export_to_markdown(
                    image_mode=ImageRefMode.PLACEHOLDER,
                    page_break_placeholder=None,
                ),
            )
        )
        html_pages.append(
            (
                page["index"],
                doc.export_to_html(image_mode=ImageRefMode.PLACEHOLDER),
                Path(page["image_path"]),
            )
        )

    markdown_path = output_dir / f"{title}.md"
    html_output_path = output_dir / f"{title}.html"

    markdown_path.write_text(build_markdown(title, md_pages), encoding="utf-8")
    html_output_path.write_text(
        build_html(title, source_name, html_output_path, html_pages),
        encoding="utf-8",
    )

    print(f"Wrote Markdown: {markdown_path}")
    print(f"Wrote HTML: {html_output_path}")


if __name__ == "__main__":
    main()
