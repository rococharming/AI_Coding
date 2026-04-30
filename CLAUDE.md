# 语言设定与核心角色 (Global Rules)
- **语言指令**：无论输入何种语言，你必须始终使用**简体中文**进行思考、回复和知识库的编写。
- **角色定义**：你正在维护一个 **AI Coding 知识库**，聚焦 Claude Code 生态及更广泛的 AI 编程工具、方法论与实践。知识库遵循 Karpathy 的 [LLM Wiki 规范](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f)，你的任务是将碎片化的学习素材编译成结构化、高度相互链接的 Obsidian 知识库。

# 核心目录与权限边界 (Immutability & Architecture)
你必须严格遵守以下文件操作权限，这是不可逾越的底线：

- `/raw/` (不可变层 - Immutable)：
  - **绝对只读**。这里存放我的原始素材，包括文章、书籍、论文等。
  - **禁止修改或删除此目录下的任何文件**。它是事实的唯一真相来源。
- `/assets/` (媒体资产层)：
  - 存放图片、PDF和媒体。引用时使用 Obsidian 标准语法 `![[文件名称.png]]`。
- `/wiki/` (编译输出层 - You Own This)：
  - 这是你的专属工作区。你需要在此处创建、更新、提炼知识并解决矛盾。
- `/Claude Code/` (个人学习草稿区 - 保留不变)：
  - 这是用户的个人学习笔记目录，**禁止修改或删除此目录下的任何文件**。
  - 当此目录下新增或更新有内容的笔记时，应先将其复制到 `raw/01-articles/`（使用 kebab-case 命名），再执行 `/ingest` 流程提炼到 wiki/。
  - 此目录是用户原始思考的保留地，与 `raw/` 的事实来源定位不同。
- `qmd` (本地搜索引擎 - 可选但推荐用于大规模 wiki)：
  - 安装：`npm install -g @tobilu/qmd`
  - 初始化：`qmd collection add ./wiki --name ai-coding-wiki && qmd embed`
  - 当 wiki 页面超过 100 个时，query skill 内部优先使用 qmd 进行搜索定位
  - 每次 ingest 后执行 `qmd embed` 更新索引

# Wiki 核心文件契约 (The Wiki Schema)
当你在 `/wiki/` 中工作时（尤其是执行写入操作后），必须维护以下基石：

1. **`wiki/index.md` (总目录)**：
   每次向 wiki 新增知识页后，必须同步更新此文件，将其按分类加入目录中。
   格式要求： [[页面名称]] — 一句话描述。
    - Tools/Entities/Concepts: 使用 TitleCase 命名。
    - Sources/Workflows: 使用 kebab-case 命名。
    范例：
    ```markdown
    # Wiki Index

    ## Tools
    - [[ToolName]] — 该工具的核心功能、适用场景及关键配置。

    ## Concepts
    - [[ConceptName]] — 该概念或方法论的核心定义与实践要点。

    ## Entities
    - [[EntityName]] — 该实体的身份定义或核心产品。

    ## Sources
    - [[摘要-source-slug]] — 该资料的核心主旨摘要。

    ## Workflows
    - [[workflow-slug]] — 该工作流的操作步骤与最佳实践。
    ```
2. **`wiki/log.md` (操作日志)**：
    只能追加写入（Append-only）。每次操作后记录：`## [YYYY-MM-DD] <动作> | <操作简述>`。
    操作类型： ingest, query, lint, sync
    **边界**：只记录知识库内容层面的操作（素材摄入、查询回答、健康检查），不记录基础设施搭建过程（如安装工具、修改 skill、调整配置等）。
    范例：
    ```markdown
    ## [2026-04-11] ingest | 引入项目 Claude Code 核心概念
    - **变更**: 新增 [[ClaudeCode]], [[摘要-claude-code-docs]]; 更新 [[index.md]]
    - **冲突**: 无 (或: 冲突 [[RAG架构]], 已标注)

    ## [2026-04-11] query | 解析 Karpathy LLM-Wiki 理念
    - **输出**: 已保存至 [[分析-karpathy-wiki-philosophy]]

    ## [2026-04-11] lint | 周度健康检查
    - **结果**: 修复 2 处死链，发现 1 个孤儿页面 [[UnlinkedPage]]
    ```
3. **内容分类**：
   - `/wiki/tools/`：存放 AI Coding 工具的专题页（如 `Claude_Code.md`、`Cursor.md`、`MCP.md`）。每个工具页涵盖其功能、配置、使用场景及与其他工具的对比。
   - `/wiki/concepts/`：存放概念、框架、方法论（如 `Agentic_Coding.md`、`Prompt_Engineering.md`、`RAG.md`）。
   - `/wiki/entities/`：存放人物、公司、组织（如 `Anthropic.md`、`Karpathy.md`）。
   - `/wiki/sources/`：存放从 `raw/` 提炼出的原始素材摘要（如 `摘要-superpowers.md`）。
   - `/wiki/workflows/`：存放操作指南、最佳实践、配置模板（如 `Claude_Code_快速配置.md`、`MCP_服务器搭建.md`）。
4. **强制双向链接**：
   每一个 wiki 页面必须包含 `## 关联连接` 区域，使用 Obsidian 双链 `[[页面名称]]` 链接到其他相关概念。绝不能产生孤岛页面。
5. **矛盾处理原则**：
   如果新摄入的知识与旧知识冲突，不要静默覆盖。在页面中新建 `## 知识冲突` 区块，将两种说法都保留并做对比。

# 工作流指令说明 (Workflows / Skills)
当被要求执行以下操作时，请遵循核心逻辑（未来可能由专用 Agent Skills 接管）：

- `/ingest <路径>`：读取指定的 `raw/` 文件，将其核心价值提炼并整合到 `wiki/` 目录的相关工具/概念/实体/工作流中。必须更新 index 和 log。
  - 当素材是关于某个 AI Coding 工具的功能说明时，归入 `/wiki/tools/`。
  - 当素材是关于操作步骤或配置指南时，归入 `/wiki/workflows/`。
  - 当素材是关于通用方法论或概念时，归入 `/wiki/concepts/`。
  - 若素材涉及工具对比，在相关工具页中建立双向链接，并可创建 `/wiki/syntheses/` 下的对比分析页。
- `/query <问题>`：通过 qmd 搜索定位相关页面（大规模时），或读取 wiki/index.md 寻找相关文件（小规模时）。进行深度阅读后综合回答，并在回答中必须使用 `[[wikilink]]` 标注引用来源。
  - **小规模**（< 100 页面）：读取 `wiki/index.md` → 定位分类 → 读取页面
  - **大规模**（≥ 100 页面）：`qmd query "问题"` → 获取 Top-K 结果 → 读取页面
- `/lint`：全局扫描 `wiki/` 目录，找出孤岛页面（没有双链）、死链（链接不存在的页面）以及存在逻辑冲突的地方，并向我报告。

# 页面 Frontmatter (YAML) 规范
所有生成的 wiki 页面必须包含以下 YAML 头部：
---
title: "页面标题"
type: tool | concept | entity | source | workflow
tags: [知识标签, 可选工具名]  # 标签不能包含空格，多个单词用连字符连接
tools: [关联的工具名，如 Claude Code, Cursor]  # 仅当 type 为 concept/workflow/source 且关联特定工具时填写
sources: [关联的raw文件相对路径]
last_updated: YYYY-MM-DD
---