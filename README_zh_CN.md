# 学术论文智能总结工具 🤖📄

## 项目简介

这是一个基于 AI 的学术论文自动摘要生成工具，旨在帮助研究者、学生和学术工作者快速理解复杂学术论文的核心内容。通过先进的 OpenAI GPT 模型，本工具能够智能地分析和总结 PDF 文档。

## 🌟 主要特性

- **智能分段总结**：将长文档分割成多个段落，逐段深入分析
- **综合性摘要**：生成包含研究目的、方法、主要发现的全面总结
- **Markdown 输出**：以结构清晰的 Markdown 格式保存总结
- **灵活配置**：支持通过配置文件自定义处理参数
- **多语言支持**：支持中文学术论文总结

## 🛠 技术栈

- Python 3.8+
- OpenAI API (GPT-4o Mini)
- PyPDF2 (PDF 文本提取)
- python-dotenv (环境变量管理)
- PyYAML (配置文件解析)

## 📦 安装步骤

1. 克隆仓库
```bash
git clone https://github.com/yourusername/academic-summarize.git
cd academic-summarize
```

2. 创建虚拟环境
```bash
python3 -m venv venv
source venv/bin/activate
```

3. 安装依赖
```bash
pip install -r requirements.txt
```

4. 配置 OpenAI API 密钥
- 创建 `.env` 文件
- 添加 `OPENAI_API_KEY=your_openai_api_key`

## 🚀 使用方法

### 基本使用
```bash
python summarize_papers.py
```

### 配置文件
在 `config.yaml` 中可以自定义：
- 输入/输出目录
- 最大字符数
- 日志级别
- OpenAI 模型参数

## 📂 目录结构
```
academic-summarize/
│
├── 论文输入区/         # 放置待总结的 PDF 文件
├── 论文总结区/         # 生成的论文总结 Markdown 文件
│
├── summarize_papers.py # 主脚本
├── config.yaml         # 配置文件
├── requirements.txt    # 依赖列表
└── .env               # API 密钥配置
```

## 🔍 工作原理

1. 提取 PDF 文本
2. 将文本分割成多个段落
3. 逐段使用 GPT 模型生成总结
4. 合并生成综合性摘要
5. 保存为 Markdown 文件

## ⚠️ 注意事项

- 需要有效的 OpenAI API 密钥
- 大型 PDF 文件可能需要较长处理时间
- API 调用会产生费用

## 🤝 贡献指南

1. Fork 仓库
2. 创建功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m '添加了某某功能'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 提交 Pull Request

## 📄 许可证

基于 MIT 许可证开源。详见 `LICENSE` 文件。

## 🌈 未来计划

- [ ] 支持更多语言
- [ ] 添加交互式 CLI
- [ ] 优化 API 调用性能
- [ ] 增加更多输出格式选项

---

**免责声明**：本工具仅用于学术研究和辅助理解，不能替代人工全面阅读。
