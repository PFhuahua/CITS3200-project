#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os, csv, time, json, argparse, pathlib, hashlib, base64, re
from typing import Optional, List, Dict, Literal
from pydantic import BaseModel, ValidationError
import json

DEFAULT_TOP_K = 3
YEAR_MIN, YEAR_MAX = 1900, 2035 #TODO adjust as needed

#TODO: will update metadata model as needed
class DocMeta(BaseModel):
    title: str
    year: int
    country_iso: str                 
    state_province: Optional[str] = ""
    publisher: Optional[str] = ""
    doc_type: Literal["report","handbook","tables","abstract"] = "report"
    access: Literal["green","yellow","red"] = "yellow"  # green = open download; yellow = remote request; red = limited
    source_url: str
    confidence: Optional[float] = None

# Small utilities
def _slug(s: str) -> str:
    s = re.sub(r"[^\w\s-]", "", s, flags=re.UNICODE).strip().lower()
    s = re.sub(r"[\s-]+", "_", s)
    return s or "doc"

def _stable_id(s: str) -> str:
    h = hashlib.blake2s(s.encode("utf-8"), digest_size=8).digest()
    return base64.urlsafe_b64encode(h).decode().rstrip("=")

def color_to_priority(c: str) -> int:
    return {"green":1, "yellow":2, "red":3}.get(c, 3)

def color_to_method(c: str) -> str:
    return {"green":"download", "yellow":"remote_request", "red":"physical"}.get(c, "physical")

def _now_iso() -> str:
    return time.strftime("%Y-%m-%dT%H-%M-%SZ", time.gmtime())

# Country name to ISO2 mapping
with open("name_to_iso.json", encoding="utf-8") as f:
    NAME_TO_ISO = json.load(f)

def name_to_iso2(country_name: str) -> str:
    if not country_name:
        return "XX"
    key = country_name.strip().lower()
    if key in NAME_TO_ISO:
        return NAME_TO_ISO[key]
    key2 = key.replace("’","'").replace("é","e").replace("á","a")
    return NAME_TO_ISO.get(key2, "XX")

# Candidate generator (mockdata)
# TODO replace with API calls
def build_candidates(country_iso: str, year: int, top_k: int, state_province: str = "") -> List[DocMeta]:
    base_title = f"{country_iso} Census {year}"
    publisher_by_iso = {
        "IN":"Office of the Registrar General & Census Commissioner",
        "CN":"National Bureau of Statistics",
        "PH":"Philippine Statistics Authority",
        "ID":"Statistics Indonesia (BPS)",
    }
    publisher = publisher_by_iso.get(country_iso, "National Statistics Office")

    types = ["report", "handbook", "tables", "abstract"]
    items: List[DocMeta] = []

    for i in range(min(top_k, len(types))):
        dtype = types[i]
        title = base_title if dtype == "report" else f"{base_title} {dtype.title()}"
        url = f"local://{country_iso}/{year}/{_slug(title)}.pdf"

        items.append(DocMeta(
            title=title,
            year=year,
            country_iso=country_iso,
            state_province=state_province,
            publisher=publisher,
            doc_type=dtype,        
            access="yellow",          
            source_url=url,
            confidence=None            
        ))
    return items

# Validation helpers
def parse_year(y_raw: str) -> Optional[int]:
    if not y_raw or not y_raw.isdigit():
        return None
    y = int(y_raw)
    return y if YEAR_MIN <= y <= YEAR_MAX else None

def ensure_iso(country_iso: Optional[str], country_name: Optional[str]) -> Optional[str]:
    if country_iso:
        return country_iso.strip().upper()
    if country_name:
        iso = name_to_iso2(country_name)
        return iso if iso != "XX" else None
    return None

# Main batch
def run_batch(csv_in: str, csv_out: str, err_log: str, top_k: int = DEFAULT_TOP_K):
    pathlib.Path(os.path.dirname(csv_out) or ".").mkdir(parents=True, exist_ok=True)
    pathlib.Path(os.path.dirname(err_log) or ".").mkdir(parents=True, exist_ok=True)

    with open(csv_in, newline="", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        if reader.fieldnames:
            reader.fieldnames = [h.lstrip("\ufeff").strip() for h in reader.fieldnames]
        rows = list(reader)

    total = len(rows)
    print(f"[INFO] total={total}")
    if total == 0:
        print("[WARN] no rows; CSV must have headers like: year,country_name[,state_province][,query]")
        return

    ok_rows: List[Dict] = []
    errs: List[Dict] = []
    run_id = _now_iso()
    now_ts = _now_iso()

    for i, row in enumerate(rows, start=1):
        q = (row.get("query") or "").strip()  # optional field, used only for logging/debugging
        y = parse_year((row.get("year") or "").strip())
        iso = ensure_iso((row.get("country_iso") or "").strip() or None,
                         (row.get("country_name") or "").strip() or None)
        sp = (row.get("state_province") or "").strip()

        if y is None:
            errs.append({"query": q or "(auto)", "error": "invalid_year", "detail": "Year required and must be within range"})
            print(f"[SKIP] row {i}: invalid/missing year")
            continue
        if not iso:
            errs.append({"query": q or "(auto)", "error": "missing_country", "detail": "country_name or country_iso is required (full name in dropdown)"})
            print(f"[SKIP] row {i}: missing country")
            continue

        display = q or f"census {iso} {y}"
        print(f"[{i}/{total}] {display} (country={iso}, year={y})")

        try:
            cands = build_candidates(iso, y, top_k=top_k, state_province=sp)
            # flatten for CSV
            qid = _stable_id(display)[:6]
            for rank, m in enumerate(cands, start=1):
                d = m.model_dump()
                access = d["access"]
                ok_rows.append({
                    "run_id": run_id,
                    "query_id": qid,
                    "query": display,
                    "rank": rank,
                    "id": _stable_id(d["source_url"]),
                    "title": d["title"],
                    "year": d["year"],
                    "country_iso": d["country_iso"],
                    "state_province": d.get("state_province") or "",
                    "publisher": d.get("publisher") or "",
                    "doc_type": d.get("doc_type") or "",
                    "access": access,
                    "access_method": color_to_method(access),
                    "access_priority": color_to_priority(access),
                    "source_url": d["source_url"],
                    "confidence": d.get("confidence", ""),
                    "created_at": now_ts,
                })
        except ValidationError as ve:
            errs.append({"query": display, "error": "validation_error", "detail": ve.errors()})
        except Exception as e:
            errs.append({"query": display, "error": "build_candidates_error", "detail": str(e)})

    # write CSV
    if ok_rows:
        fieldnames = [
            "run_id","query_id","query","rank","id","title","year",
            "country_iso","state_province","publisher","doc_type",
            "access","access_method","access_priority",
            "source_url","confidence","created_at",
        ]
        with open(csv_out, "w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=fieldnames)
            w.writeheader()
            w.writerows(ok_rows)
        print(f"[OK] written {len(ok_rows)} rows -> {csv_out}")

        # write nested JSON grouped by query_id
        grouped: Dict[str, List[Dict]] = {}
        for r in ok_rows:
            grouped.setdefault(r["query_id"], []).append(r)

        nested = []
        for qid, items in grouped.items():
            items_sorted = sorted(items, key=lambda x: x["rank"])
            nested.append({
                "run_id": run_id,
                "query_id": qid,
                "query": items_sorted[0]["query"],
                "candidates": [
                    {
                        "rank": it["rank"],
                        "id": it["id"],
                        "title": it["title"],
                        "year": it["year"],
                        "country_iso": it["country_iso"],
                        "state_province": it["state_province"],
                        "publisher": it["publisher"],
                        "doc_type": it["doc_type"],
                        "access": it["access"],
                        "access_method": it["access_method"],
                        "access_priority": it["access_priority"],
                        "source_url": it["source_url"],
                        "confidence": it["confidence"] if it["confidence"] != "" else None,
                        "created_at": it["created_at"],
                    } for it in items_sorted
                ]
            })

        json_out = os.path.splitext(csv_out)[0] + ".json"
        with open(json_out, "w", encoding="utf-8") as f:
            json.dump(nested, f, ensure_ascii=False, indent=2)
        print(f"[OK] written {len(nested)} queries -> {json_out}")
    else:
        print("[WARN] no successful rows")

    # write errors
    if errs:
        with open(err_log, "w", encoding="utf-8") as f:
            json.dump(errs, f, ensure_ascii=False, indent=2)
        print(f"[OK] errors logged -> {err_log}")

# CLI
if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", required=True,
                    help="CSV with: year (required) + country_name or country_iso (+ optional state_province, query)")
    ap.add_argument("--out", default="exports/results.csv")
    ap.add_argument("--errors", default="exports/errors.json")
    ap.add_argument("--top_k", type=int, default=DEFAULT_TOP_K, help="candidates per query")
    args = ap.parse_args()
    run_batch(args.input, args.out, args.errors, top_k=args.top_k)
