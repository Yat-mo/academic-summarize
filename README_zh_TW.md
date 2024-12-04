# 學術論文智能摘要工具 🤖📄

## 專案簡介

這是一個基於 AI 的學術論文自動摘要生成工具，旨在幫助研究者、學生和學術工作者快速理解複雜學術論文的核心內容。透過先進的 OpenAI GPT 模型，本工具能夠智慧地分析和總結 PDF 文檔。

## 🌟 主要特性

- **智能分段總結**：將長文檔分割成多個段落，逐段深入分析
- **綜合性摘要**：生成包含研究目的、方法、主要發現的全面總結
- **Markdown 輸出**：以結構清晰的 Markdown 格式保存總結
- **靈活配置**：支持透過配置文件自定義處理參數
- **多語言支持**：支持中文學術論文總結

## 🛠 技術棧

- Python 3.8+
- OpenAI API (GPT-4o Mini)
- PyPDF2 (PDF 文本提取)
- python-dotenv (環境變數管理)
- PyYAML (配置文件解析)

## 📦 安裝步驟

1. 克隆倉庫
```bash
git clone https://github.com/Yat-mo/academic-summarize.git
cd academic-summarize
```

2. 建立虛擬環境
```bash
python3 -m venv venv
source venv/bin/activate
```

3. 安裝依賴
```bash
pip install -r requirements.txt
```

4. 配置 OpenAI API 金鑰
- 建立 `.env` 文件
- 新增 `OPENAI_API_KEY=your_openai_api_key`

## 🚀 使用方法

### 基本使用
```bash
python summarize_papers.py
```

### 配置文件
在 `config.yaml` 中可以自定義：
- 輸入/輸出目錄
- 最大字元數
- 日誌級別
- OpenAI 模型參數

## 📂 目錄結構
```
academic-summarize/
│
├── 論文輸入區/         # 放置待總結的 PDF 文件
├── 論文總結區/         # 生成的論文總結 Markdown 文件
│
├── summarize_papers.py # 主腳本
├── config.yaml         # 配置文件
├── requirements.txt    # 依賴列表
└── .env               # API 金鑰配置
```

## 🔍 工作原理

1. 提取 PDF 文本
2. 將文本分割成多個段落
3. 逐段使用 GPT 模型生成總結
4. 合併生成綜合性摘要
5. 保存為 Markdown 文件

## ⚠️ 注意事項

- 需要有效的 OpenAI API 金鑰
- 大型 PDF 文件可能需要較長處理時間
- API 呼叫會產生費用

## 🤝 貢獻指南

1. Fork 倉庫
2. 建立功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交變更 (`git commit -m '新增了某某功能'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 提交 Pull Request

## 📄 許可證

基於 MIT 許可證開源。詳見 `LICENSE` 文件。

## 🌈 未來計劃

- [ ] 支持更多語言
- [ ] 新增互動式 CLI
- [ ] 優化 API 呼叫效能
- [ ] 增加更多輸出格式選項

---

**免責聲明**：本工具僅用於學術研究和輔助理解，不能替代人工全面閱讀。
