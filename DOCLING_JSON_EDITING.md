# Editing cached Docling JSON

The cached document lives at `cache/docling-formula/document.json`.

## Important: Docling refs are positional

Docling stores OCR text entries in the top-level `texts` array, and references such as `#/texts/34` are JSON Pointers to array index `34`. Do not remove an object from the middle of `texts`, `pictures`, `tables`, or similar top-level arrays unless you also renumber every later `self_ref`, `parent`, `children`, and other `$ref` in the whole document.

Removing `texts[162]`, for example, shifts the old `texts[163]` object into array slot `162`. Existing references still point to `#/texts/163`, so Docling starts resolving them to the wrong object. This can fail with hierarchy errors like:

```text
Document hierarchy is inconsistent. #/pictures/12 has child #/texts/169 with parent #/pictures/13
```

For one-off cleanup, prefer hiding or detaching a text entry while preserving array indices.

## Hide or detach a text entry

Each text entry has a `self_ref`, for example:

```json
{
  "self_ref": "#/texts/34",
  "parent": { "$ref": "#/body" },
  "children": [],
  "label": "text",
  "text": "Smoothed energy-time"
}
```

To hide one standalone text entry without shifting array indices:

1. Find the entry by exact `text` or by `self_ref`.
2. Keep the object in the top-level `texts` array.
3. Remove any matching child references, such as `{ "$ref": "#/texts/34" }`, from `children` arrays elsewhere in the JSON.
4. Optionally clear the entry's visible `text` and `orig` fields so accidental direct renderers do not display it.
5. Load the file with Docling afterward. A plain JSON ref scan is not enough because it will not catch parent/child mismatches caused by shifted array indices.

## Exact-text detach script

Run this from the repo root. Change `target_text` to the standalone text entry you want to hide.

```powershell
. .venv\Scripts\Activate.ps1
python -c 'import json; from pathlib import Path; p=Path("cache/docling-formula/document.json"); data=json.loads(p.read_text(encoding="utf-8")); target_text="Smoothed energy-time"; detached_refs=set()
for item in data.get("texts",[]):
    if item.get("text")==target_text:
        detached_refs.add(item.get("self_ref"))
        item["text"]=""
        item["orig"]=""
def scrub(obj):
    if isinstance(obj,dict):
        for key,value in list(obj.items()):
            if key=="children" and isinstance(value,list):
                obj[key]=[child for child in value if not (isinstance(child,dict) and child.get("$ref") in detached_refs)]
            else:
                scrub(value)
    elif isinstance(obj,list):
        for value in obj: scrub(value)
scrub(data)
p.write_text(json.dumps(data, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")
print("detached refs:", sorted(detached_refs))'
```

## Validation script

This catches missing text references. It does not prove Docling's hierarchy is valid, so also run the Docling load check below.

```powershell
. .venv\Scripts\Activate.ps1
python -c 'import json; d=json.load(open("cache/docling-formula/document.json",encoding="utf-8")); text_refs={t["self_ref"] for t in d.get("texts",[])}; refs=[]
def walk(o):
    if isinstance(o,dict):
        r=o.get("$ref")
        if isinstance(r,str) and r.startswith("#/texts/"): refs.append(r)
        for v in o.values(): walk(v)
    elif isinstance(o,list):
        for v in o: walk(v)
walk(d)
missing=sorted(set(refs)-text_refs)
print("missing text refs:", missing)'
```

## Docling load check

Run this after editing. This is the check that catches positional-ref and parent/child consistency problems.

```powershell
. .venv\Scripts\Activate.ps1
python -c 'from pathlib import Path; from docling_core.types.doc.document import DoclingDocument; DoclingDocument.load_from_json(Path("cache/docling-formula/document.json")); print("Docling load: ok")'
```

codex session id for joining paragraphs
019db43a-6506-7aa2-a132-fa7e8f948445
