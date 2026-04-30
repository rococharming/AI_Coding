---
name: ingest
description: 将 raw/ 目录下的原始素材读取并提炼，整合到 Obsidian wiki/ 知识库中。当用户要求摄入新素材、处理 raw/ 文件、或添加新知识到 wiki 时调用。必须更新 wiki/index.md 和 wiki/log.md。操作 Obsidian vault 中的文件时，优先使用 obsidian-cli 命令（obsidian create / read / append），让 Obsidian 实时感知变更。遵循分类规则：工具功能→wiki/tools/、操作指南→wiki/workflows/、方法论→wiki/concepts/。
---

# Ingest

将原始素材编译进 AI Coding 知识库 wiki（Obsidian vault）。

## 前置条件

- Obsidian 应用处于打开状态（obsidian-cli 需要与运行中的 Obsidian 实例通信）
- 若 Obsidian 未打开，回退到 Read / Write / Edit 文件系统工具

## 触发时机

- 用户说"/ingest <路径>"
- 用户要求"把 raw/ 下的某文件整理到 wiki"
- 用户要求"处理这个素材"或"添加新知识"
- /Claude Code/ 目录新增有内容的笔记（需先复制到 raw/01-articles/）

## 执行流程

### 1. 读取原始素材
使用 Read 工具读取指定的 raw/ 文件。如果素材是图片，描述其内容。

### 2. 内容分类判断
根据素材主题归入对应目录：

| 素材类型 | 目标目录 | 示例 |
|----------|----------|------|
| AI Coding 工具的功能说明、特性介绍 | `wiki/tools/` | Claude Code、Cursor、Superpowers |
| 操作步骤、配置指南、最佳实践 | `wiki/workflows/` | 第三方模型配置、权限模式切换 |
| 通用方法论、架构概念、设计模式 | `wiki/concepts/` | 记忆系统、子代理、RAG |
| 人物、公司、组织 | `wiki/entities/` | Anthropic、Karpathy |
| 原始素材摘要 | `wiki/sources/` | 所有素材必须创建对应的摘要页 |

### 3. 创建 Source 摘要页
使用 obsidian-cli 在 `wiki/sources/` 创建素材摘要。

```bash
obsidian create path="wiki/sources/摘要-<slug>.md" content="---\ntitle: \"...\"\ntype: source\n...\n---\n\n# ..."
```

摘要页必须包含：
- 素材来源信息（原始文件路径）
- 核心主旨（一句话概括）
- 关键知识点列表（3-7 条）
- `## 关联链接` 区域，链接到相关的 Tools/Concepts/Workflows 页面

若内容较长，先使用 Write 工具写入文件，再执行 `obsidian read path="..."` 验证 Obsidian 已同步。

### 4. 更新或创建目标页面

**如果是新工具/概念/工作流**：
- 使用 `obsidian create path="wiki/<分类>/<页面>.md" content="..."` 创建页面
- 页面需包含 frontmatter、结构化内容、关联链接
- 内容较长时，先用 Write 工具写入，再 `obsidian read` 验证

**如果是已有页面的补充**：
- 使用 `obsidian read path="wiki/<分类>/<页面>.md"` 读取现有内容
- 将新素材的信息整合进去
- 使用 `obsidian create path="..." content="..." overwrite` 覆盖更新
- 在 `## 知识冲突` 区域标注与旧知识的矛盾（如果有）
- 更新 `last_updated` 字段

### 5. 维护双向链接
每个 wiki 页面必须包含 `## 关联链接` 区域，使用 `[[页面名称]]` 链接到相关页面。

**链接策略**：
- Source 页 → 链接到提炼出的 Tools/Concepts/Workflows 页
- Tools/Concepts/Workflows 页 → 链接到相关的 Source 页和其他概念页
- 绝不产生孤岛页面（除 index.md 和 log.md 外）

验证链接时，使用 `obsidian search query="页面名称"` 快速确认目标页面是否存在。

### 6. 更新基石文件

**更新 `wiki/index.md`**：
- 使用 `obsidian read path="wiki/index.md"` 读取现有索引
- 将新页面按分类加入目录
- 使用 `obsidian create path="wiki/index.md" content="..." overwrite` 覆盖更新
- 格式：`[[页面名称]] — 一句话描述`

**追加 `wiki/log.md`**：
```bash
obsidian append path="wiki/log.md" content="## [YYYY-MM-DD] ingest | <操作简述>\n- **变更**: 新增 [[页面]]; 更新 [[页面]]\n- **冲突**: 无 (或: 冲突 [[页面]], 已标注)\n- **归档**: raw/<原始文件> → raw/archive/\n"
```

### 7. 归档源文件

处理完成后，将已摄入的源文件从 `raw/` 移动到 `raw/archive/`，避免重复处理。

```bash
# 创建归档目录（如不存在）
mkdir -p raw/archive

# 移动已处理的源文件
mv raw/01-articles/claude-code-intro.md raw/archive/
```

**归档规则**：
- 单个文件摄入：直接移动到 `raw/archive/`
- 批量摄入（如 `raw/01-articles/` 下的多个文件）：保持子目录结构，移动到 `raw/archive/01-articles/`
- 归档后的文件不再参与后续 ingest 流程
- 若源文件位于 `raw/` 外的其他位置，移动到 `raw/archive/external/`

**注意**：`raw/` 目录整体仍为只读原则——归档操作仅移动文件位置，不修改文件内容。

### 8. 更新搜索索引

wiki 页面变更后，更新 qmd 搜索索引，否则新内容无法被搜索到。

```bash
qmd embed
```

**注意**：
- `qmd embed` 会重新生成所有页面的向量嵌入
- 当 wiki 很大时（数百页面），这可能需要几秒到几十秒
- 如果仅更新少量页面，未来 qmd 可能支持增量 embed（需关注版本更新）

如果 qmd 未安装，跳过此步骤并记录到 log.md。

## 页面规范

### Frontmatter（必须）
```yaml
---
title: "页面标题"
type: tool | concept | entity | source | workflow
tags: [知识标签, 可选工具名]  # 标签不能包含空格，多个单词用连字符连接，如 Agent-Architecture
tools: [关联的工具名]  # 仅当 type 为 concept/workflow/source 时填写
sources: [关联的raw文件相对路径]
last_updated: YYYY-MM-DD
---
```

### 命名规范
- Tools/Entities/Concepts: **TitleCase**（如 `Claude_Code.md`）
- Sources/Workflows: **kebab-case**（如 `摘要-claude-code-intro.md`）

### 内容结构
- 标题（H1）
- 概述/定义段落
- 结构化内容（H2/H3 分节）
- `## 关联链接` 区域（末尾）

## 冲突处理

如果新素材与现有 wiki 内容矛盾：
1. **不要静默覆盖**旧知识
2. 在页面中新建 `## 知识冲突` 区块
3. 将两种说法都保留并做对比说明
4. 在 log.md 中记录冲突
