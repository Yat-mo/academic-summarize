# 學術論文智能摘要工具 🤖📄

## 專案簡介

呢個係一個用 AI 嚟整嘅學術論文自動摘要工具，幫研究者、學生同學術工作者快啲明白複雜學術論文嘅核心內容。用咗 OpenAI GPT 模型，呢個工具可以智能噉分析同總結 PDF 文檔。

## 🌟 主要特性

- **智能分段總結**：將啲長文檔分成好多段，逐段深入分析
- **綜合性摘要**：生成包含研究目的、方法、主要發現嘅全面總結
- **Markdown 輸出**：用結構清晰嘅 Markdown 格式保存總結
- **靈活配置**：可以用配置文件自定義處理參數
- **多語言支持**：支持中文學術論文總結

## 🛠 技術架構

- Python 3.8+
- OpenAI API (GPT-4o Mini)
- PyPDF2 (PDF 文本提取)
- python-dotenv (環境變量管理)
- PyYAML (配置文件解析)

## 📦 安裝步驟

1. 克隆倉庫
```bash
git clone https://github.com/Yat-mo/academic-summarize.git
cd academic-summarize
```

2. 整個虛擬環境
```bash
python3 -m venv venv
source venv/bin/activate
```

3. 安裝依賴
```bash
pip install -r requirements.txt
```

4. 配置 OpenAI API 密鑰
- 開個 `.env` 文件
- 加入 `OPENAI_API_KEY=your_openai_api_key`

## 🚀 使用方法

### 基本使用
```bash
python summarize_papers.py
```

### 配置文件
喺 `config.yaml` 入面可以自定義：
- 輸入/輸出目錄
- 最大字數
- 日誌級別
- OpenAI 模型參數

## 📂 目錄結構
```
academic-summarize/
│
├── 論文輸入區/         # 放要總結嘅 PDF 文件
├── 論文總結區/         # 生成嘅論文總結 Markdown 文件
│
├── summarize_papers.py # 主程式
├── config.yaml         # 配置文件
├── requirements.txt    # 依賴列表
└── .env               # API 密鑰配置
```

## 🔍 工作原理

1. 提取 PDF 文字
2. 將文字分割成多個段落
3. 逐段用 GPT 模型生成總結
4. 合併生成綜合性摘要
5. 保存做 Markdown 文件

## ⚠️ 注意事項

- 要有效嘅 OpenAI API 密鑰
- 大型 PDF 文件可能要較長處理時間
- API 調用會有費用

## 🤝 貢獻指南

1. Fork 倉庫
2. 開個功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交改動 (`git commit -m '加咗個好正嘅功能'`)
4. 推送去分支 (`git push origin feature/AmazingFeature`)
5. 提交 Pull Request

## 📄 許可證

用 MIT 許可證開源。詳情睇 `LICENSE` 文件。

## 🌈 未來計劃

- [ ] 支持更多語言
- [ ] 加入互動式 CLI
- [ ] 優化 API 調用效能
- [ ] 加多啲輸出格式選項

---

**免責聲明**：呢個工具淨係用嚟幫手睇學術論文，唔可以完全代替人手閱讀。
