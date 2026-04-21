from __future__ import annotations

import argparse
import re
from pathlib import Path

from docling.datamodel.base_models import InputFormat
from docling.datamodel.pipeline_options import CodeFormulaVlmOptions, PdfPipelineOptions
from docling.document_converter import DocumentConverter, ImageFormatOption
from docling_core.types.doc import DoclingDocument, ImageRefMode


IMG_SRC_RE = re.compile(r'<img\b[^>]*\bsrc="([^"]+\.(?:jpe?g|png|tiff?|bmp|webp))"', re.IGNORECASE)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Convert an HTML file containing page images into one cached Docling JSON."
    )
    parser.add_argument(
        "--html",
        default="The Analytic Impulse.html",
        help="Path to the source HTML file containing page images.",
    )
    parser.add_argument(
        "--cache-dir",
        default="cache/docling",
        help="Directory to write the cached Docling JSON.",
    )
    parser.add_argument(
        "--document-name",
        default="document.json",
        help="Filename for the merged cached Docling JSON.",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Rebuild cached JSON even if it already exists.",
    )
    parser.add_argument(
        "--no-formula-enrichment",
        action="store_true",
        help="Disable Docling's formula recognition and LaTeX conversion stage.",
    )
    parser.add_argument(
        "--formula-preset",
        choices=["codeformulav2", "granite_docling"],
        default="codeformulav2",
        help="Docling code/formula VLM preset to use when formula enrichment is enabled.",
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


def make_converter(*, formula_enrichment: bool, formula_preset: str) -> DocumentConverter:
    pipeline_options = PdfPipelineOptions()
    pipeline_options.do_ocr = True
    pipeline_options.do_table_structure = True
    pipeline_options.do_code_enrichment = False
    pipeline_options.do_formula_enrichment = formula_enrichment
    if formula_enrichment:
        pipeline_options.code_formula_options = CodeFormulaVlmOptions.from_preset(
            formula_preset
        )
        pipeline_options.code_formula_options.extract_code = False
        pipeline_options.code_formula_options.extract_formulas = True

    return DocumentConverter(
        allowed_formats=[InputFormat.IMAGE],
        format_options={
            InputFormat.IMAGE: ImageFormatOption(pipeline_options=pipeline_options),
        },
    )


def main() -> None:
    args = parse_args()
    html_path = Path(args.html).resolve()
    cache_dir = Path(args.cache_dir).resolve()
    cache_dir.mkdir(parents=True, exist_ok=True)
    document_path = cache_dir / args.document_name

    if document_path.exists() and not args.force:
        print(f"Skipping conversion: cache exists at {document_path}")
        return

    image_paths = image_paths_from_html(html_path)
    converter = make_converter(
        formula_enrichment=not args.no_formula_enrichment,
        formula_preset=args.formula_preset,
    )
    docs = []
    for index, image_path in enumerate(image_paths, start=1):
        result = converter.convert(image_path)
        docs.append(result.document)
        print(f"Converted page image {index}: {image_path.name}")

    document = DoclingDocument.concatenate(docs)
    document.name = html_path.stem
    document.validate_document()
    document.save_as_json(document_path, image_mode=ImageRefMode.PLACEHOLDER)
    print(f"Wrote merged document: {document_path}")


if __name__ == "__main__":
    main()
