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

Coordinates were plotted by hand on aerial imagery. The imagery each row was read from is in the
`source` column: `nsw_imagery` (NSW aerial imagery) or `esri_world_imagery` (Esri World Imagery).

座標は航空写真の上で手作業でプロットしたものです。各行がどの写真から読んだかは `source` 列にあります
（`nsw_imagery`＝NSW 州の航空写真／`esri_world_imagery`＝Esri World Imagery）。

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
dl_lat, dl_lng, dl2_lat, dl2_lng, plotted_at, source`. Coordinates are WGS84 decimal degrees.

## Updating / 更新

The export is run manually (it is not scheduled):

```
SUPABASE_URL=... SUPABASE_SERVICE_ROLE_KEY=... python scripts/export_overseas_plot_holes.py
```

It reads only published shared courses outside Japan (filtered in the query itself) and rewrites
`data/plot_holes_overseas.csv`. The key comes from the maintainer's local environment and is never committed.

## Last updated / 更新日

2026-10-17 — added the `source` column (imagery per row).
`source` 列（行ごとの写真の出典）を追加。

2026-10-17 — first data export: Panya Indra Golf Club (Bangkok, TH), 27 holes. Imagery: Esri World Imagery.
初回の書き出し。Panya Indra Golf Club（タイ・バンコク）27 ホール。写真は Esri World Imagery。

2026-10-17 — initial release (header-only CSV).
