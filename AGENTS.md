# AGENTS.md — 咖啡手沖科學 LLM Wiki 員工手冊

> 本手冊依「先討論、後生成」原則建立，逐條對應使用者確認的 8 項需求摘要。全檔嚴格控制在 12,000 字元以內，只維護此單一規格檔（不重複建立 GEMINI.md；若使用 Claude Code，於 CLAUDE.md 撰寫 `@AGENTS.md` 共用）。

## 1. 專案目標與讀者定位
- **主題**：咖啡手沖科學（Pour-Over Coffee Science）。
- **目標讀者**：完全沒接觸過手沖咖啡的新手，不假設讀者預先知道 TDS、萃取率（Extraction Yield）、鹼度緩衝等專有名詞。
- **語言規範**：以繁體中文撰寫，專有名詞首次出現時附英文對照（如：萃取率 Extraction Yield、悶蒸 Blooming）。

## 2. 知識庫架構與單向事實防線
- `raw/`：**唯讀事實來源區**，存放 S1–S6 原始公開文章的擷取摘要與原文 URL。嚴禁 AI 修改 `raw/` 內的原始數據或結論。
- `wiki/sources/`：單篇來源筆記（一篇一檔，忠實整理該來源的論點與數據）。
- `wiki/concepts/`：核心原理與操作變因詞條（跨來源統整，標註每條事實出處）。
- `wiki/syntheses/`：新手實戰整合頁（黃金起始配方、風味除錯指南）。
- `wiki/index.md`：全站目錄與知識關聯索引。
- `wiki/log.md`：每次 ingest、lint 與衝突修正的歷史紀錄。

## 3. 出處標註與衝突處理規則
- **出處粒度**：每一項科學數值、建議範圍與實驗結論皆須標註來源編號（如 `[S1]`）與原文連結；產出簡報時，每一頁底部皆須列出對應的 Wiki 頁面路徑與來源編號。
- **跨來源矛盾處理**：禁止私自忽略、覆蓋或憑空猜測。遇來源間數值或術語衝突（例如 S2 將濾沖 TDS 與萃取率數值混淆，或 S1 與 S6 的鈣硬度範圍差異），必須於對應詞條以 `> ⚠️ 跨來源衝突註記` 區塊並列雙方說法，並對照 SCA 標準說明差異。

## 4. Ingest 與版控作業流程
- 採**單篇依序 ingest**（一次一篇）：讀取 `raw/Sx-*.md` → 建立 `wiki/sources/Sx-*.md` → 同步更新受影響的 `wiki/concepts/`、`wiki/syntheses/`、`wiki/index.md` 與 `wiki/log.md` → 執行 `git commit`。
- 嚴禁引入未收錄於 `raw/` 的外部數據或憑空補充實驗數字。

## 5. 品質檢查（Lint）與驗收標準
- 「做完了」不是 AI 說了算，是腳本說了算。
- 每次 ingest 完成後必須執行 `python3 scripts/lint_wiki.py`，確認通過：
  1. 零孤島頁面（所有 `wiki/` 子頁皆於 `wiki/index.md` 被連結）。
  2. 零斷鏈（所有相對 Markdown 連結目標皆存在）。
  3. 出處完整性（每個詞條頁皆含 `[S1]`–`[S6]` 來源標記與原文 URL）。
  4. 衝突標記存在（跨來源矛盾點已於詞條中明示）。

## 6. 下游產出與 Graph Workflow
- 下游產出為教學型 HTML 簡報（`topic-pourover-science/deck.html`），頁數控制在 **8–15 頁**。
- 完整流程定義於 `.agents/workflows/topic-slides.md`，並透過 `python3 scripts/check_deck.py` 進行自動化驗收（頁數、每頁出處、Wiki 頁面存在性、單頁字數上限防溢出）。
- **停止條件（煞車）**：單一節點修正最多 3 輪；若檢索到的相關 Wiki 頁面少於 3 頁，立即停下回報資料不足，嚴禁以模型既有知識硬湊。
