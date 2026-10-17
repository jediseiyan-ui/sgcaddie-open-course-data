# sgcaddie-open-course-data

Golf course hole coordinates (tee / front / center / back of green, dogleg points) for courses
**outside Japan**, collected for the SGCaddie app and published as open data.

ゴルフアプリ SGCaddie のために作った、**日本国外**のゴルフコースのホール座標（ティー・グリーン手前／中央／奥・
ドッグレッグ点）を、オープンデータとして公開します。

## License / ライセンス

The data in `data/` is licensed under the
[Creative Commons Attribution 4.0 International License (CC BY 4.0)](https://creativecommons.org/licenses/by/4.0/).

`data/` のデータは [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/deed.ja) で提供します。
利用時は次のように出典を表示してください。

> SGCaddie open course data (https://github.com/jediseiyan-ui/sgcaddie-open-course-data), CC BY 4.0

The export script (`scripts/`) is provided under the same terms.

## Sources / 出典

Coordinates were plotted by hand on aerial imagery. The imagery used for each course is recorded
per course in the SGCaddie ledger (`imagery_source`).

座標は航空写真の上で手作業でプロットしたものです。コースごとに使った写真は台帳（`imagery_source`）に記録しています。

- New South Wales, Australia: NSW aerial imagery —
  © State Government of NSW and Spatial Services (DCS), licensed under
  [CC BY 3.0 AU](https://creativecommons.org/licenses/by/3.0/au/).
- Other countries: Esri World Imagery —
  Esri, Maxar, Earthstar Geographics, and the GIS User Community.

No Google or Apple imagery was used.
Google・Apple の写真は使っていません。

## What is NOT included / 含まないもの

- **Courses in Japan are not included.** This repository only contains rows whose course
  `country` is not `JP`.
  **日本のコースは含みません。** コースの `country` が `JP` 以外の行だけを出力します。
- Yardages (scorecard distances) are not included.

## Files / ファイル

| path | content |
|---|---|
| `data/plot_holes_overseas.csv` | one row per hole × green (`green_type` = single / main / sub) |
| `scripts/export_overseas_plot_holes.py` | the export script (run manually) |

Columns: `country, region, course_id, course_name, hole_number, nine_name, hole_in_nine, green_type,
tee_lat, tee_lng, front_lat, front_lng, center_lat, center_lng, back_lat, back_lng,
dl_lat, dl_lng, dl2_lat, dl2_lng, plotted_at`. Coordinates are WGS84 decimal degrees.

## Updating / 更新

The export is run manually (it is not scheduled):

```
SUPABASE_URL=... SUPABASE_ANON_KEY=... python scripts/export_overseas_plot_holes.py
```

It reads only published courses (the public read policy) and rewrites `data/plot_holes_overseas.csv`.

## Last updated / 更新日

2026-10-17 — initial release (no overseas courses yet; the CSV contains the header only).
初版。海外コースはまだ無く、CSV は見出し行だけです。
