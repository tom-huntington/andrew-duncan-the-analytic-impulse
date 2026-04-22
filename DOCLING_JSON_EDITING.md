# Editing cached Docling JSON

The cached document lives at `cache/docling-formula/document.json`.

## Delete a text entry

Docling stores OCR text entries in the top-level `texts` array. Each entry has a stable `self_ref`, for example:

```json
{
  "self_ref": "#/texts/34",
  "parent": { "$ref": "#/body" },
  "children": [],
  "label": "text",
  "text": "Smoothed energy-time"
}
```

To delete one entry cleanly:

1. Find the entry by exact `text` or by `self_ref`.
2. Remove that object from the top-level `texts` array.
3. Remove any matching child references, such as `{ "$ref": "#/texts/34" }`, from `children` arrays elsewhere in the JSON.
4. Parse the JSON afterward and check that no `$ref` points to a missing text entry.

## Exact-text deletion script

Run this from the repo root. Change `target_text` to the standalone text entry you want to delete.

```powershell
. .venv\Scripts\Activate.ps1
python -c 'import json; from pathlib import Path; p=Path("cache/docling-formula/document.json"); data=json.loads(p.read_text(encoding="utf-8")); target_text="Smoothed energy-time"; deleted_refs=set(); data["texts"]=[item for item in data.get("texts",[]) if not (item.get("text")==target_text and not deleted_refs.add(item.get("self_ref")))]
def scrub(obj):
    if isinstance(obj,dict):
        for key,value in list(obj.items()):
            if key=="children" and isinstance(value,list):
                obj[key]=[child for child in value if not (isinstance(child,dict) and child.get("$ref") in deleted_refs)]
            else:
                scrub(value)
    elif isinstance(obj,list):
        for value in obj: scrub(value)
scrub(data)
p.write_text(json.dumps(data, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")
print("deleted refs:", sorted(deleted_refs))'
```

## Validation script

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
