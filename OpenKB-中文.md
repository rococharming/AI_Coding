---
title: "VectifyAI/OpenKB: OpenKB: 开放式 LLM 知识库"
source: "https://github.com/VectifyAI/OpenKB"
author:
published:
created: 2026-04-30
description: "OpenKB: 开放式 LLM 知识库。通过创建账户为 VectifyAI/OpenKB 做出贡献。"
tags:
  - "clippings"
---

[![OpenKB (by PageIndex)](https://camo.githubusercontent.com/f6545872ff934893226196c979b1db5142b2631081b5a553d46598459eb1efa2/68747470733a2f2f646f63732e70616765696e6465782e61692f696d616765732f6f70656e6b622e706e67)](https://openkb.ai/)

## OpenKB — 开放式 LLM 知识库

*扩展长文档 • 基于推理的检索 • 原生多模态 • 无需向量数据库*

---

## 📑 什么是 OpenKB

**OpenKB（开放式知识库）** 是一个开源的 CLI 系统，它使用 LLM 将原始文档编译成结构化、相互链接的维基风格知识库，并由 [**PageIndex**](https://github.com/VectifyAI/PageIndex) 提供无向量的长文档检索能力。

这一理念基于 Andrej Karpathy 提出的一个[概念](https://x.com/karpathy/status/2039805659525644595)：LLM 生成摘要、概念页面和交叉引用，所有内容都自动维护。知识随时间积累，而不是在每次查询时重新推导。

### 为什么不使用传统 RAG？

传统 RAG 在每次查询时都从头重新发现知识，没有任何积累。OpenKB 将知识一次性编译成持久化的维基，然后保持更新。交叉引用已经存在，矛盾会被标记，综合反映所有已消费的内容。

### 功能特性

- **广泛的格式支持** — 通过 markitdown 支持 PDF、Word、Markdown、PowerPoint、HTML、Excel、文本等格式
- **扩展长文档** — 通过 [PageIndex](https://github.com/VectifyAI/PageIndex) 树形索引处理长而复杂的文档，实现准确的无向量长上下文检索
- **原生多模态** — 检索并理解图表、表格和图像，而不仅仅是文本
- **编译型维基** — LLM 将文档管理和编译成摘要、概念页面和交叉链接，所有内容保持同步
- **查询** — 向维基提问（一次性）。LLM 浏览编译后的知识来回答
- **交互式聊天** — 多轮对话，支持持久化会话，可在多次运行之间恢复
- **检查** — 健康检查发现矛盾、空白、孤立页面和过时内容
- **监视模式** — 将文件拖入 `raw/`，维基自动更新
- **兼容 Obsidian** — 维基是纯 `.md` 文件，使用 `[[维基链接]]`。在 Obsidian 中打开以查看图谱视图和浏览

## 🚀 快速开始

### 安装

```
pip install openkb
```
*其他安装选项*
- **从 GitHub 安装最新版：**
	```
	pip install git+https://github.com/VectifyAI/OpenKB.git
	```
- **从源代码安装**（可编辑，用于开发）：
	```
	git clone https://github.com/VectifyAI/OpenKB.git
	cd OpenKB
	pip install -e .
	```

### 快速入门

```
# 1. 为知识库创建一个目录
mkdir my-kb && cd my-kb

# 2. 初始化知识库
openkb init

# 3. 添加文档
openkb add paper.pdf
openkb add ~/papers/  # 添加整个目录

# 4. 提问
openkb query "主要发现是什么？"

# 5. 或进行交互式聊天
openkb chat
```

### 设置 LLM

OpenKB 通过 [LiteLLM](https://github.com/BerriAI/litellm) 提供[多 LLM 支持](https://docs.litellm.ai/docs/providers)（例如 OpenAI、Claude、Gemini）（固定到[安全版本](https://docs.litellm.ai/blog/security-update-march-2026)）。

在 `openkb init` 期间或 [.openkb/config.yaml](#配置) 中设置模型，使用 `provider/model` LiteLLM 格式（如 `anthropic/claude-sonnet-4-6`）。OpenAI 模型可以省略前缀（如 `gpt-5.4`）。

创建一个包含 LLM API 密钥的 `.env` 文件：

```
LLM_API_KEY=your_llm_api_key
```

## 🧩 OpenKB 的工作原理

### 架构

```
raw/                              你将文件放在这里
 │
 ├─ 短文档 ──→ markitdown ──→ LLM 读取全文
 │                                     │
 ├─ 长 PDF ──→ PageIndex ────→ LLM 读取文档树
 │                                     │
 │                                     ▼
 │                         维基编译（使用 LLM）
 │                                     │
 ▼                                     ▼
wiki/
 ├── index.md            知识库概览
 ├── log.md              操作时间线
 ├── AGENTS.md           维基模式（LLM 指令）
 ├── sources/            全文转换
 ├── summaries/          每篇文档摘要
 ├── concepts/           跨文档综合 ← 精华所在
 ├── explorations/       保存的查询结果
 └── reports/            检查报告
```

### 短文档与长文档处理

|  | 短文档 | 长文档（PDF ≥ 20 页） |
| --- | --- | --- |
| **转换** | markitdown → Markdown | PageIndex → 树形索引 + 摘要 |
| **图像** | 内联提取（pymupdf） | 由 PageIndex 提取 |
| **LLM 读取** | 全文 | 文档树 |
| **结果** | 摘要 + 概念 | 摘要 + 概念 |

短文档由 LLM 完整读取。长 PDF 由 PageIndex 索引为层次树结构并生成摘要。LLM 读取树而非全文，从而实现更好的长文档检索。

### 知识编译

添加文档时，LLM 会：

1. 生成**摘要**页面
2. 读取现有的**概念**页面
3. 创建或更新跨文档综合的概念
4. 更新**索引**和**日志**

单个来源可能涉及 10-15 个维基页面。知识会积累：每个文档都会丰富现有维基，而不是孤立存在。

## ⚙️ 使用方式

### 命令

| 命令 | 描述 |
| --- | --- |
| `openkb init` | 初始化新知识库（交互式） |
| `openkb add <file_or_dir>` | 添加文档并编译到维基 |
| `openkb query "question"` | 向知识库提问（使用 `--save` 将答案保存到 `wiki/explorations/`） |
| `openkb chat` | 启动交互式多轮聊天（使用 `--resume`、`--list`、`--delete` 管理会话） |
| `openkb watch` | 监视 `raw/` 并自动编译新文件 |
| `openkb lint` | 运行结构 + 知识健康检查 |
| `openkb list` | 列出索引的文档和概念 |
| `openkb status` | 显示知识库统计信息 |

### 交互式聊天

`openkb chat` 打开基于维基知识库的交互式聊天会话。与一次性 `openkb query` 不同，每轮对话都携带会话历史，因此你可以深入某个主题而无需重新输入上下文。

```
openkb chat                       # 启动新会话
openkb chat --resume              # 恢复最近会话
openkb chat --resume 20260411     # 按 ID 恢复（唯一前缀即可）
openkb chat --list                # 列出所有会话
openkb chat --delete <id>         # 删除会话
```

在聊天中，输入 `/` 访问斜杠命令（按 Tab 补全）：

- `/help` — 列出可用命令
- `/status` — 显示知识库状态
- `/list` — 列出所有文档
- `/add <path>` — 在聊天中添加文档或目录
- `/save [name]` — 将对话导出到 `wiki/explorations/`
- `/clear` — 开始新会话（当前会话保留在磁盘上）
- `/lint` — 运行知识库检查
- `/exit` — 退出（Ctrl-D 也可）

### 配置

设置由 `openkb init` 初始化，存储在 `.openkb/config.yaml` 中：

```
model: gpt-5.4                   # LLM 模型（任何 LiteLLM 支持的提供商）
language: en                     # 维基输出语言
pageindex_threshold: 20          # PageIndex 的 PDF 页数阈值
```

模型名称使用 `provider/model` LiteLLM [格式](https://docs.litellm.ai/docs/providers)（OpenAI 模型可省略前缀）：

| 提供商 | 模型示例 |
| --- | --- |
| OpenAI | `gpt-5.4` |
| Anthropic | `anthropic/claude-sonnet-4-6` |
| Gemini | `gemini/gemini-3.1-pro-preview` |

### PageIndex 集成

由于上下文限制、上下文衰减和摘要丢失，长文档对 LLM 来说具有挑战性。[PageIndex](https://github.com/VectifyAI/PageIndex) 通过无向量、基于推理的检索解决了这个问题——构建层次树索引，让 LLM 通过推理进行上下文感知检索。

PageIndex 默认使用[开源版本](https://github.com/VectifyAI/PageIndex)在本地运行，无需外部依赖。

#### 可选：云端支持

对于大型或复杂的 PDF，可以使用 [PageIndex Cloud](https://docs.pageindex.ai/) 访问额外功能，包括：

- 扫描 PDF 的 OCR 支持（通过托管 VLM 模型）
- 更快的结构生成
- 大型文档的可扩展索引

在 `.env` 中设置 `PAGEINDEX_API_KEY` 以启用云端功能：

```
PAGEINDEX_API_KEY=your_pageindex_api_key
```

### AGENTS.md

`wiki/AGENTS.md` 文件定义维基结构和约定。它是 LLM 维护维基的操作手册。自定义它以更改维基的组织和呈现方式。

在运行时，LLM 从磁盘读取 `AGENTS.md`，因此你的修改会立即生效。

### 与 Obsidian 一起使用

OpenKB 的维基是一个 Markdown 文件目录，使用 `[[维基链接]]`。Obsidian 原生渲染。

1. 将 `wiki/` 作为 Obsidian 仓库打开
2. 浏览摘要、概念和探索
3. 使用图谱视图查看知识连接
4. 使用 Obsidian Web Clipper 将网络文章添加到 `raw/`

## 🧭 了解更多

### 与 Karpathy 方法的对比

|  | Karpathy 的工作流 | OpenKB |
| --- | --- | --- |
| 短文档 | LLM 直接读取 | markitdown → LLM 读取 |
| 长文档 | 上下文限制、上下文衰减 | PageIndex 树形索引 |
| 支持格式 | Web 剪藏 → .md | PDF、Word、PPT、Excel、HTML、文本、CSV、.md |
| 维基编译 | LLM 代理 | LLM 代理（相同） |
| 问答 | 查询维基 | 维基 + PageIndex 检索 |

### 技术栈

- [PageIndex](https://github.com/VectifyAI/PageIndex) — 无向量、基于推理的文档索引和检索
- [markitdown](https://github.com/microsoft/markitdown) — 通用文件转 Markdown 转换
- [OpenAI Agents SDK](https://github.com/openai/openai-agents-python) — 代理框架（通过 LiteLLM 支持非 OpenAI 模型）
- [LiteLLM](https://github.com/BerriAI/litellm) — 多提供商 LLM 网关
- [Click](https://click.palletsprojects.com/) — CLI 框架
- [watchdog](https://github.com/gorakhargosh/watchdog) — 文件系统监控

### 路线图

- 将长文档处理扩展到非 PDF 格式
- 通过嵌套文件夹支持扩展到大型文档集合
- 大规模知识库的分层概念（主题）索引
- 数据库支持的存储引擎
- 用于浏览和管理维基的 Web UI

### 贡献

欢迎贡献！请提交拉取请求，或打开 [issue](https://github.com/VectifyAI/OpenKB/issues) 报告错误或请求功能。对于较大的更改，建议先打开 issue 讨论方案。
