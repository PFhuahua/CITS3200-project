#!/usr/bin/env python3
import argparse, json, re, zipfile
from pathlib import Path
from typing import Any, Dict, List, Optional, Union
from xml.etree import ElementTree as ET

NA_RE = re.compile(r'^(?:N/?A|NA|NaN|null|None)$', re.IGNORECASE)
HEADER_KEYS = {
    'name', 'title (in english)', 'original title', 'country', 'province',
    'date', 'year', 'publication', 'author', 'publisher',
    'volume', 'file size', 'pages', 'colonising'
}


def norm(v, keep_na=False): 
    if v is None: return "None" if keep_na else ""
    s = str(v).strip()
    return s if keep_na or not NA_RE.match(s) else ""

def get_pd():
    try: import pandas as pd; return pd
    except ImportError: raise RuntimeError("Need pandas: pip install pandas openpyxl")

def guess_header(df, depth, keep_na):
    best = (-1, -1, -1, 0)
    for i in range(min(depth, len(df))):
        cells = [norm(x, keep_na) for x in df.iloc[i]]
        kw = sum(1 for c in cells if any(k in c.lower() for k in HEADER_KEYS))
        hdr = sum(1 for c in cells if c and not re.match(r'^\d+(\.\d+)?$', c) and len(c) < 80)
        non_empty = sum(1 for c in cells if c)
        score = (kw, hdr, non_empty, -i)
        if score > best: best, best_i = score, i
    return best_i

def apply_header(df_raw, hdr_row, keep_na):
    pd = get_pd()
    headers = [norm(h, True) or f'col_{i}' for i, h in enumerate(df_raw.iloc[hdr_row])]
    data = df_raw.iloc[hdr_row+1:].copy()
    data.columns = headers
    data = data.astype(str).replace({'nan': ''}).map(lambda x: norm(x, keep_na))
    # Drop empty cols/rows
    data = data[[c for c in data.columns if (data[c] != '').any()]]
    return data[(data != '').any(axis=1)]

def read_csv(path, max_rows, keep_na, hdr_row, hdr_depth):
    pd = get_pd()
    df = pd.read_csv(path, header=None, dtype=str, na_filter=False, encoding="latin1")
    if hdr_row is None: hdr_row = guess_header(df, hdr_depth, keep_na)
    data = apply_header(df, hdr_row, keep_na)
    if max_rows: data = data.head(max_rows)
    return [dict(row) for _, row in data.iterrows() if any(row.values)]

def read_excel(path, sheet, max_rows, keep_na, hdr_row, hdr_depth):
    pd = get_pd()
    with pd.ExcelFile(path) as xls:
        if sheet is None:
            sheet = next((s for s in xls.sheet_names if not pd.read_excel(xls, s, nrows=1).empty), xls.sheet_names[0])
        elif sheet.isdigit(): sheet = xls.sheet_names[int(sheet)]
        df = pd.read_excel(xls, sheet, header=None, dtype=str, na_filter=False)
    if hdr_row is None: hdr_row = guess_header(df, hdr_depth, keep_na)
    data = apply_header(df, hdr_row, keep_na)
    if max_rows: data = data.head(max_rows)
    return [dict(row) for _, row in data.iterrows() if any(row.values)]

def read_docx(path, keep_na):
    NS = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
    with zipfile.ZipFile(path) as zf:
        try: doc = ET.parse(zf.open('word/document.xml'))
        except: return []
        
        # Extract tables
        tables = []
        for tbl in doc.findall('.//w:tbl', NS):
            rows = []
            for tr in tbl.findall('w:tr', NS):
                cells = [''.join(t.text or '' for t in tc.findall('.//w:t', NS)).strip() 
                        for tc in tr.findall('w:tc', NS)]
                if cells: rows.append(cells)
            if rows: tables.append(rows)
        
        if tables:
            records = []
            for table in tables:
                if len(table) < 2: continue
                headers = [norm(h, True) or f'col_{i}' for i, h in enumerate(table[0])]
                for row in table[1:]:
                    rec = {h: norm(row[i] if i < len(row) else '', keep_na) for i, h in enumerate(headers)}
                    if any(rec.values()): records.append(rec)
            return records
        
        # Extract paragraphs if no tables
        paras = []
        for p in doc.findall('.//w:p', NS):
            text = ''.join(t.text or '' for t in p.findall('.//w:t', NS)).strip()
            if text: paras.append(norm(text, keep_na))
        return paras

def convert_file(path, sheet=None, max_rows=None, keep_na=False, header_row=None, header_depth=50):
    p = Path(path)
    ext = p.suffix.lower()
    if ext == '.csv': return read_csv(p, max_rows, keep_na, header_row, header_depth)
    elif ext in ('.xlsx', '.xls'): return read_excel(p, sheet, max_rows, keep_na, header_row, header_depth)
    elif ext == '.docx': return read_docx(p, keep_na)
    else: raise ValueError(f"Unsupported: {ext}")

def main():
    p = argparse.ArgumentParser(description="Convert CSV/XLSX/DOCX to Python lists")
    p.add_argument("input", help="Input file")
    p.add_argument("--sheet", help="Excel sheet")
    p.add_argument("--max-rows", type=int, help="Max rows")
    p.add_argument("--keep-na", action="store_true", help="Keep NA values")
    p.add_argument("--as-json", action="store_true", help="JSON output")
    p.add_argument("--quiet", action="store_true", help="Quiet mode")
    p.add_argument("--header-row", type=int, help="Header row (0-based)")
    p.add_argument("--header-depth", type=int, default=50, help="Header scan depth")
    args = p.parse_args()
    
    data = convert_file(args.input, args.sheet, args.max_rows, args.keep_na, args.header_row, args.header_depth)
    
    if not args.quiet:
        print(f"# {Path(args.input).name} | Rows: {len(data)}")
    
    print(json.dumps(data, indent=2) if args.as_json else repr(data))

if __name__ == "__main__": main()