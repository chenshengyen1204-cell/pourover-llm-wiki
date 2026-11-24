# LLM Wiki 維護與 Ingest 日誌（log.md）

| 步驟 | 動作 | 影響檔案 | 檢查結果 |
| :--- | :--- | :--- | :--- |
| Step 0 | 需求訪談確認（8 項規格）並建立 `AGENTS.md` | `AGENTS.md` | 字元數 < 12,000，逐條符合需求摘要 |
| Ingest 1 | 匯入 S1（SCA 黃金杯標準） | `raw/S1`, `wiki/sources/S1`, `wiki/concepts/extraction-and-tds.md` | 通過 |
| Ingest 2 | 匯入 S2（研磨度與萃取） | `raw/S2`, `wiki/sources/S2`, `wiki/concepts/grind-size-and-uniformity.md` | ⚠️ 偵測衝突：S2 誤將濾沖 TDS 寫成 18–22%，已標註衝突註記並對照 S1 修正 |
| Ingest 3 | 匯入 S3（水溫與烘焙度） | `raw/S3`, `wiki/sources/S3`, `wiki/concepts/water-temperature-and-roast.md` | 通過 |
| Ingest 4 | 匯入 S4（悶蒸與 CO₂ 排氣） | `raw/S4`, `wiki/sources/S4`, `wiki/concepts/blooming-and-co2-degassing.md` | 通過 |
| Ingest 5 | 匯入 S5（濾杯幾何 V60 vs. Kalita） | `raw/S5`, `wiki/sources/S5`, `wiki/concepts/dripper-geometry.md` | 通過 |
| Ingest 6 | 匯入 S6（水質化學） | `raw/S6`, `wiki/sources/S6`, `wiki/concepts/water-chemistry.md` | ⚠️ 偵測差異：S1 與 S6 鈣硬度區間不同，已並列標註交集 50–85 mg/L |
| Synthesis | 跨來源彙整新手黃金配方與風味除錯表 | `wiki/syntheses/*`, `wiki/index.md` | 通過 `scripts/lint_wiki.py` 全項檢驗 |
