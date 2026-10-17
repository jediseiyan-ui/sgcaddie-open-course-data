#!/usr/bin/env python3
"""Export plot_holes rows for courses outside Japan (country != 'JP') to CSV. Run manually.

    SUPABASE_URL=... SUPABASE_ANON_KEY=... python scripts/export_overseas_plot_holes.py [--out data/plot_holes_overseas.csv]

Uses the anon key only: the public read policy returns published courses only, so unpublished
work never leaks into the open data. Japanese courses are excluded by the query itself
(country=neq.JP) and checked again before writing.
"""
from __future__ import annotations

import argparse
import csv
import json
import os
import sys
import urllib.parse
import urllib.request
from pathlib import Path

COLUMNS = [
    "country", "region", "course_id", "course_name", "hole_number", "nine_name", "hole_in_nine",
    "green_type", "tee_lat", "tee_lng", "front_lat", "front_lng", "center_lat", "center_lng",
    "back_lat", "back_lng", "dl_lat", "dl_lng", "dl2_lat", "dl2_lng", "plotted_at",
]
PAGE = 1000
IN_CHUNK = 50


def get(base: str, key: str, path: str) -> list[dict]:
    """Page through a PostgREST endpoint. The key is sent as a header and never printed."""
    rows: list[dict] = []
    offset = 0
    while True:
        req = urllib.request.Request(
            f"{base.rstrip('/')}/rest/v1/{path}",
            headers={"apikey": key, "Authorization": f"Bearer {key}", "Range-Unit": "items",
                     "Range": f"{offset}-{offset + PAGE - 1}", "Accept": "application/json"},
        )
        with urllib.request.urlopen(req, timeout=60) as res:
            page = json.loads(res.read().decode("utf-8"))
        rows.extend(page)
        if len(page) < PAGE:
            return rows
        offset += PAGE


def export_rows(courses: list[dict], holes: list[dict]) -> list[dict]:
    """Join plot_holes to their (non-Japanese) course and order rows stably. Pure function."""
    by_id = {c["id"]: c for c in courses if str(c.get("country") or "JP").upper() != "JP"}
    out = []
    for h in holes:
        c = by_id.get(h.get("course_id"))
        if c is None:
            continue
        row = {k: h.get(k) for k in COLUMNS if k in h}
        row.update(country=str(c["country"]).upper(), region=c.get("region"),
                   course_id=c["id"], course_name=c.get("name"))
        out.append(row)
    out.sort(key=lambda r: (r["country"], str(r["course_name"]), int(r.get("hole_number") or 0),
                            str(r.get("green_type"))))
    return out


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--out", type=Path, default=Path(__file__).resolve().parent.parent / "data" / "plot_holes_overseas.csv")
    args = parser.parse_args()
    base = os.environ.get("SUPABASE_URL", "")
    key = os.environ.get("SUPABASE_ANON_KEY", "")
    if not base or not key:
        print("SUPABASE_URL and SUPABASE_ANON_KEY are required", file=sys.stderr)
        return 2
    courses = get(base, key, "courses?select=id,name,country,region&country=neq.JP&order=id.asc")
    holes: list[dict] = []
    ids = [c["id"] for c in courses]
    for i in range(0, len(ids), IN_CHUNK):
        chunk = ",".join(ids[i:i + IN_CHUNK])
        holes += get(base, key, "plot_holes?select=*&course_id=in.(" + urllib.parse.quote(chunk, safe=",") +
                     ")&order=course_id.asc,hole_number.asc,green_type.asc")
    rows = export_rows(courses, holes)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    with args.out.open("w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=COLUMNS, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)
    print(f"{len(rows)} rows from {len(courses)} courses -> {args.out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
