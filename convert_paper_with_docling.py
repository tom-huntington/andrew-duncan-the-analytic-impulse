from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

from docling.datamodel.base_models import InputFormat
from docling.datamodel.pipeline_options import PdfPipelineOptions
from docling.document_converter import DocumentConverter, ImageFormatOption
from docling_core.types.doc import ImageRefMode


IMG_SRC_RE = re.compile(r'<img\b[^>]*\bsrc="([^"]+\.(?:jpe?g|png|tiff?|bmp|webp))"', re.IGNORECASE)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Convert an HTML file containing page images into cached Docling JSON."
    )
    parser.add_argument(
        "--html",
        default="The Analytic Impulse.html",
        help="Path to the source HTML file containing page images.",
    )
    parser.add_argument(
        "--cache-dir",
        default="cache/docling",
        help="Directory to write cached Docling JSON and manifest files.",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Rebuild cached JSON even if it already exists.",
    )
    return parser.parse_args()


def image_paths_from_html(html_path: Path) -> list[Path]:
    raw_html = html_path.read_text(encoding="utf-8")
    matches = IMG_SRC_RE.findall(raw_html)
    if not matches:
        raise ValueError(f"No image references found in {html_path}")

    image_paths: list[Path] = []
    for src in matches:
        normalized = src.replace("/", "\\")
        if normalized.startswith(".\\"):
            normalized = normalized[2:]
        image_path = (html_path.parent / normalized).resolve()
        if not image_path.exists():
            raise FileNotFoundError(f"Referenced image does not exist: {image_path}")
        image_paths.append(image_path)

    return image_paths


def make_converter() -> DocumentConverter:
    pipeline_options = PdfPipelineOptions()
    pipeline_options.do_ocr = True
    pipeline_options.do_table_structure = True
    pipeline_options.do_code_enrichment = False
    pipeline_options.do_formula_enrichment = False

    return DocumentConverter(
        allowed_formats=[InputFormat.IMAGE],
        format_options={
            InputFormat.IMAGE: ImageFormatOption(pipeline_options=pipeline_options),
        },
    )


def build_manifest(html_path: Path, cache_dir: Path, image_paths: list[Path]) -> dict:
    pages = []
    for index, image_path in enumerate(image_paths, start=1):
        json_name = f"page_{index:02d}.json"
        pages.append(
            {
                "index": index,
                "image_path": str(image_path),
                "json_path": str((cache_dir / json_name).resolve()),
            }
        )

    return {
        "title": html_path.stem,
        "source_html": str(html_path),
        "cache_dir": str(cache_dir),
        "pages": pages,
    }


def main() -> None:
    args = parse_args()
    html_path = Path(args.html).resolve()
    cache_dir = Path(args.cache_dir).resolve()
    cache_dir.mkdir(parents=True, exist_ok=True)

    image_paths = image_paths_from_html(html_path)
    converter = make_converter()
    manifest = build_manifest(html_path, cache_dir, image_paths)

    for page in manifest["pages"]:
        image_path = Path(page["image_path"])
        json_path = Path(page["json_path"])

        if json_path.exists() and not args.force:
            print(f"Skipping page {page['index']}: cache exists at {json_path.name}")
            continue

        result = converter.convert(image_path)
        result.document.save_as_json(
            json_path,
            image_mode=ImageRefMode.PLACEHOLDER,
        )
        print(f"Cached page {page['index']}: {image_path.name} -> {json_path.name}")

    manifest_path = cache_dir / "manifest.json"
    manifest_path.write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    print(f"Wrote manifest: {manifest_path}")


if __name__ == "__main__":
    main()
