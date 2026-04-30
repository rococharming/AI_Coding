---
name: query
description: 基于 Obsidian wiki 知识库回答用户关于 AI Coding 的问题。通过 obsidian-cli 读取 wiki/index.md 定位相关页面，深度阅读后综合回答，并使用 [[wikilink]] 标注引用来源。操作 wiki 文件时优先使用 obsidian read / backlinks / search。如果答案有价值，可以归档回 wiki。
---

# Query

基于 AI Coding 知识库回答用户问题。

## 触发时机

- 用户说"/query <问题>"
- 用户提出关于 Claude Code、AI Coding 工具、方法论的问题
- 用户要求"对比 X 和 Y"、"解释 Z 概念"

## 执行流程

### 1. 判断 wiki 规模
统计 wiki/ 目录下 .md 文件数量：
- **< 100 个页面**：走"小规模路径"（直接读取 index.md）
- **≥ 100 个页面**：走"大规模路径"（使用 qmd 搜索）

### 2a. 小规模路径（< 100 页面）

**步骤 1：读取索引**
使用 obsidian-cli 读取 `wiki/index.md`，了解知识库的整体结构和已有页面。

```bash
obsidian read path="wiki/index.md"
```

**步骤 2：定位相关页面**
根据问题关键词判断相关分类：

| 问题类型 | 优先查看分类 |
|----------|-------------|
| "Claude Code 怎么..." / "Cursor 如何..." | `## Tools` |
| "什么是 RAG" / "子代理是什么" | `## Concepts` |
| "怎么配置..." / "最佳实践..." | `## Workflows` |
| "Anthropic 是什么公司" | `## Entities` |
| "某篇文章讲了什么" | `## Sources` |

如需快速搜索，使用 obsidian search：
```bash
obsidian search query="子代理" limit=10
```

**步骤 3：深度阅读**
使用 obsidian-cli 读取判断为相关的 wiki 页面。追踪 `## 关联链接` 中的双向链接。

```bash
obsidian read path="wiki/tools/Claude_Code.md"
```

### 2b. 大规模路径（≥ 100 页面）

**步骤 1：qmd 混合搜索定位**
使用 qmd 的混合查询（BM25 + 向量 + LLM 重排序）获取最相关的页面：

```bash
qmd query "用户问题的核心关键词"
```

返回结果包含：文件路径、相关度分数、匹配片段。取 Top-K（通常 3-5 个）作为核心阅读列表。

**步骤 2：扩展关联**
对 Top-K 结果中的每个页面：
- 使用 `obsidian read path="..."` 读取完整内容
- 使用 `obsidian backlinks path="..."` 获取入站链接，发现更多关联页面
- 追踪页面内 `## 关联链接` 中的双向链接

**步骤 3：补充搜索（如信息不足）**
若核心阅读列表未能充分回答问题，使用 qmd vsearch 进行语义扩展：

```bash
qmd vsearch "问题的另一种表述"
```

### 3. 综合回答

**回答要求**：
- 直接回答用户问题，不绕弯子
- 使用 `[[页面名称]]` 标注信息来源（Obsidian 双链格式）
- 涉及多工具对比时，使用表格呈现
- 如果 wiki 中信息不足，明确告知"知识库中暂无相关信息"

**引用格式示例**：
```
Claude Code 支持三种核心权限模式：default、acceptEdits 和 plan [[Claude_Code]]。
记忆系统分为手动记忆（CLAUDE.md）和自动记忆两种 [[Memory_System]]。
```

### 5. 可选归档（高价值答案）

如果答案具有以下特征，建议归档回 wiki：
- 综合了多个页面的信息
- 发现了新的关联或对比
- 形成了结构化的分析框架
- 用户明确说"保存到 wiki"

归档方式：
- 使用 `obsidian create path="wiki/syntheses/<slug>.md" content="..."` 创建新页面
- 更新 `wiki/index.md`（`obsidian read` + `obsidian create ... overwrite`）
- 追加 `wiki/log.md`（`obsidian append`）

## 回答风格

- **准确**：基于 wiki 内容回答，不编造知识库中不存在的信息
- **简洁**：直接给出核心答案，再展开细节
- **可追溯**：每个关键论断都有 `[[wikilink]]` 来源
- **诚实**：不确定时明确说明，不猜测

## 限制

- 只基于 `wiki/` 目录中的内容回答
- 不基于 raw/ 中的原始素材直接回答（raw/ 是只读的）
- 如果问题超出 AI Coding 范围，告知用户知识库的主题边界
