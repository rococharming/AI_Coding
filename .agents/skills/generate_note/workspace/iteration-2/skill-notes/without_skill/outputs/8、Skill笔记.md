# 一、概述

在 `Claude Code` 中，**Skill（技能）** 是一种通过 `SKILL.md` 文件定义的可复用能力单元，用于封装反复使用的操作手册、检查清单或多步骤流程。当你发现自己在多次对话中粘贴相同的指令时，就应该考虑将其封装为一个 Skill。

Skill 与 `CLAUDE.md` 的核心区别在于加载时机：
- `CLAUDE.md` 的内容会在**每次会话启动时自动加载**到上下文中
- Skill 的主体内容**只在被使用时才加载**，长篇参考资料在未被调用前几乎不消耗上下文成本

旧式的 `.claude/commands/*.md` 自定义命令已经并入 Skill 机制，仍然兼容，但新写法推荐使用 `.claude/skills/<skill-name>/SKILL.md`。

`Claude Code` 的 Skill 遵循 [Agent Skills](https://agentskills.io/) 开放标准，该标准可跨多种 AI 工具工作。`Claude Code` 在此基础上扩展了调用控制、子代理执行和动态上下文注入等能力。

> Skill 是 Claude Code 生态中最重要的扩展机制之一，与 Subagent、MCP、Plugin 共同构成四层扩展体系。

---

# 二、Skill 的存放位置与作用域

Skill 存放在哪里，决定了谁能使用它。当不同层级存在同名 Skill 时，按优先级覆盖：

| 层级 | 路径 | 适用范围 | 优先级 |
|------|------|----------|--------|
| **企业/托管** | 参见 managed settings | 组织内所有用户 | 最高 |
| **个人** | `~/.claude/skills/<skill-name>/SKILL.md` | 你的所有项目 | 高 |
| **项目** | `.claude/skills/<skill-name>/SKILL.md` | 当前项目 | 中 |
| **插件** | `<plugin>/skills/<skill-name>/SKILL.md` | 插件启用处 | 低（命名空间隔离） |

插件 Skill 使用 `plugin-name:skill-name` 命名空间，因此不会与其他层级的 Skill 冲突。如果 `.claude/commands/` 中的旧式命令与 Skill 同名，Skill 优先。

## 1、实时变更检测

`Claude Code` 会监视 Skill 目录的文件变更。在 `~/.claude/skills/`、项目 `.claude/skills/` 或 `--add-dir` 目录内的 `.claude/skills/` 中添加、编辑或删除 Skill，会在**当前会话内立即生效**，无需重启。

但如果在会话开始后**首次创建顶层的 skills 目录**，则需要重启 `Claude Code` 才能被监视到。

## 2、嵌套目录自动发现

当处理子目录中的文件时，`Claude Code` 会自动发现嵌套的 `.claude/skills/` 目录。例如，如果你在编辑 `packages/frontend/` 下的文件，它也会查找 `packages/frontend/.claude/skills/`。这支持 monorepo 场景下各包拥有独立 Skill。

---

# 三、Skill 的目录结构

每个 Skill 是一个目录，`SKILL.md` 是必需的入口文件。其他文件可选，用于构建更强大的 Skill：

```text
my-skill/
├── SKILL.md           # 主指令（必需）
├── template.md        # Claude 填写的模板
├── examples/
│   └── sample.md      # 预期输出格式的示例
└── scripts/
    └── validate.sh    # Claude 可执行的脚本
```

> 建议保持 `SKILL.md` 在 500 行以内。将详细参考资料移到独立文件，在 `SKILL.md` 中引用它们，让 Claude 知道每个文件的内容和加载时机。

---

# 四、SKILL.md 文件格式

Skill 通过 YAML frontmatter 配置行为，后跟 Markdown 内容作为指令。

## 1、两种内容类型

### （1）参考型内容（Reference content）

为 Claude 增加可应用于当前工作的知识，如规范、模式、风格指南、领域知识。这类内容以内联方式运行，Claude 可以在对话中 alongside 使用它。

```yaml
---
name: api-conventions
description: API design patterns for this codebase
---

When writing API endpoints:
- Use RESTful naming conventions
- Return consistent error formats
- Include request validation
```

### （2）任务型内容（Task content）

为 Claude 提供特定操作的逐步指令，如部署、提交、代码生成。这类内容通常希望用户通过 `/skill-name` 直接调用，而非让 Claude 自动触发。可添加 `disable-model-invocation: true` 防止自动加载。

```yaml
---
name: deploy
description: Deploy the application to production
context: fork
disable-model-invocation: true
---

Deploy the application:
1. Run the test suite
2. Build the application
3. Push to the deployment target
```

## 2、Frontmatter 完整字段参考

所有字段均为可选，但建议至少填写 `description` 以便 Claude 知道何时使用该 Skill。

| 字段 | 必填 | 说明 |
|------|------|------|
| `name` | 否 | 显示名称。省略时使用目录名。仅限小写字母、数字和连字符，最多 64 字符。 |
| `description` | 推荐 | Skill 的功能和适用场景。Claude 用它判断何时应用该 Skill。省略时使用 Markdown 第一段。 |
| `when_to_use` | 否 | 补充触发条件，如触发短语或示例请求。追加到 `description`，共享 1536 字符上限。 |
| `argument-hint` | 否 | 自动补全时显示的参数提示，如 `[issue-number]`。 |
| `arguments` | 否 | 命名位置参数，用于 `$name` 替换。接受空格分隔字符串或 YAML 列表。 |
| `disable-model-invocation` | 否 | `true` 时阻止 Claude 自动加载。用于需要手动触发的工作流。默认 `false`。 |
| `user-invocable` | 否 | `false` 时从 `/` 菜单隐藏。用于不应被用户直接调用的背景知识。默认 `true`。 |
| `allowed-tools` | 否 | Skill 激活时无需询问权限即可使用的工具。接受空格分隔字符串或 YAML 列表。 |
| `model` | 否 | Skill 激活时使用的模型。覆盖当前会话模型，仅当回合生效。 |
| `effort` | 否 | Skill 激活时的推理努力级别。覆盖会话级别。选项：`low`, `medium`, `high`, `xhigh`, `max`。 |
| `context` | 否 | 设为 `fork` 时在子代理上下文中运行。 |
| `agent` | 否 | `context: fork` 时使用的子代理类型。 |
| `hooks` | 否 | Skill 生命周期钩子。 |
| `paths` | 否 | Glob 模式，限制 Skill 自动激活的文件范围。 |
| `shell` | 否 | 用于 `` !`command` `` 和 ` ```! ` 代码块的 shell。默认 `bash`，可设为 `powershell`。 |

## 3、字符串替换变量

Skill 支持动态值替换：

| 变量 | 说明 |
|------|------|
| `$ARGUMENTS` | 调用时传递的所有参数 |
| `$ARGUMENTS[N]` | 按 0 基索引访问特定参数 |
| `$N` | `$ARGUMENTS[N]` 的简写，如 `$0`, `$1` |
| `$name` | frontmatter 中 `arguments` 声明的命名参数 |
| `${CLAUDE_SESSION_ID}` | 当前会话 ID，用于日志或创建会话特定文件 |
| `${CLAUDE_EFFORT}` | 当前 effort 级别，用于适配指令 |
| `${CLAUDE_SKILL_DIR}` | Skill 目录路径，用于引用捆绑的脚本或文件 |

**示例**：

```yaml
---
name: migrate-component
description: Migrate a component from one framework to another
---

Migrate the $0 component from $1 to $2.
Preserve all existing behavior and tests.
```

运行 `/migrate-component SearchBar React Vue` 时，`$0=SearchBar`, `$1=React`, `$2=Vue`。

---

# 五、调用控制：谁可以调用 Skill

默认情况下，用户和 Claude 都可以调用任何 Skill。两个 frontmatter 字段用于限制：

- **`disable-model-invocation: true`**：仅用户可调用。用于有副作用或需要控制时机的工作流，如 `/deploy`、`/commit`。
- **`user-invocable: false`**：仅 Claude 可调用。用于背景知识，如 `legacy-system-context`，Claude 应在相关时自动加载，但用户直接调用无意义。

| Frontmatter | 用户可调用 | Claude 可调用 | 加载到上下文的时机 |
|-------------|-----------|--------------|------------------|
| （默认） | 是 | 是 | 描述始终在上下文中，完整内容调用时加载 |
| `disable-model-invocation: true` | 是 | 否 | 描述不在上下文中，用户调用时加载完整内容 |
| `user-invocable: false` | 否 | 是 | 描述始终在上下文中，调用时加载完整内容 |

---

# 六、Skill 内容生命周期

当 Skill 被调用时，渲染后的 `SKILL.md` 内容作为单条消息进入对话，并在整个会话中保留。Claude Code 不会在后续回合重新读取 Skill 文件，因此应将需要贯穿任务的指导写成**持续性指令**，而非一次性步骤。

## 1、自动压缩（Auto-compaction）

当上下文被压缩以释放空间时，Claude Code 会在摘要后重新附加每个 Skill 的最近调用记录，保留每个 Skill 的前 5000 tokens。所有重新附加的 Skill 共享 25000 tokens 的合并预算，按最近调用顺序填充，较早的 Skill 可能被完全丢弃。

> 如果 Skill 在首次响应后似乎停止影响行为，通常内容仍在上下文中，但模型选择了其他工具。可通过强化 `description` 和指令，或使用 hooks 确定性强制执行行为。

---

# 七、高级模式

## 1、动态上下文注入

使用 `` !`<command>` `` 语法在 Skill 内容发送给 Claude 之前运行 shell 命令。命令输出替换占位符，Claude 看到的是实际数据而非命令本身。

```yaml
---
name: pr-summary
description: Summarize changes in a pull request
context: fork
agent: Explore
allowed-tools: Bash(gh *)
---

## Pull request context
- PR diff: !`gh pr diff`
- PR comments: !`gh pr view --comments`
- Changed files: !`gh pr diff --name-only`

## Your task
Summarize this pull request...
```

执行流程：
1. 每个 `` !`<command>` `` 立即执行（Claude 看到之前）
2. 输出替换 Skill 内容中的占位符
3. Claude 收到包含实际 PR 数据的完整提示

对于多行命令，使用 ` ```! ` 开头的围栏代码块代替内联形式。

可通过设置 `"disableSkillShellExecution": true` 禁用此行为（对用户、项目、插件和额外目录来源的 Skill 生效）。

## 2、在子代理中运行 Skill

添加 `context: fork` 让 Skill 在隔离上下文中运行。Skill 内容成为驱动子代理的提示词，无法访问对话历史。

`context: fork` 只适用于包含明确指令的 Skill。如果 Skill 只包含"使用这些 API 规范"这类指南而无具体任务，子代理收到指南但无可执行提示，会无意义返回。

Skill 与子代理的两种协作方向：

| 方式 | 系统提示 | 任务 | 额外加载 |
|------|----------|------|----------|
| `context: fork` 的 Skill | 来自 agent 类型（Explore, Plan 等） | SKILL.md 内容 | CLAUDE.md |
| 带 `skills` 字段的子代理 | 子代理的 Markdown 正文 | Claude 的委托消息 | 预加载 Skill + CLAUDE.md |

**示例：使用 Explore 代理的研究 Skill**

```yaml
---
name: deep-research
description: Research a topic thoroughly
context: fork
agent: Explore
---

Research $ARGUMENTS thoroughly:
1. Find relevant files using Glob and Grep
2. Read and analyze the code
3. Summarize findings with specific file references
```

执行时：创建隔离上下文，子代理收到 Skill 内容作为提示，`agent` 字段决定执行环境（模型、工具、权限），结果汇总返回主对话。

## 3、预批准工具权限

`allowed-tools` 字段在 Skill 激活时授予列出工具的免确认权限。它**不限制可用工具**：所有工具仍然可调用，未列出的工具仍受权限设置管辖。

```yaml
---
name: commit
description: Stage and commit the current changes
disable-model-invocation: true
allowed-tools: Bash(git add *) Bash(git commit *) Bash(git status *)
---
```

## 4、传递参数

用户和 Claude 都可以在调用 Skill 时传递参数，通过 `$ARGUMENTS` 占位符获取。

```yaml
---
name: fix-issue
description: Fix a GitHub issue
disable-model-invocation: true
---

Fix GitHub issue $ARGUMENTS following our coding standards.
1. Read the issue description
2. Understand the requirements
3. Implement the fix
4. Write tests
5. Create a commit
```

运行 `/fix-issue 123`，Claude 收到 "Fix GitHub issue 123 following our coding standards..."

> 如果调用时提供了参数但 Skill 未包含 `$ARGUMENTS`，Claude Code 会在 Skill 内容末尾追加 `ARGUMENTS: <your input>`。

## 5、限制 Claude 的 Skill 访问

三种方式控制 Claude 可调用的 Skill：

**禁用所有 Skill**：在 `/permissions` 中拒绝 Skill 工具：
```text
Skill
```

**允许或拒绝特定 Skill**：
```text
Skill(commit)
Skill(review-pr *)
Skill(deploy *)
```

语法：`Skill(name)` 精确匹配，`Skill(name *)` 前缀匹配。

**隐藏单个 Skill**：添加 `disable-model-invocation: true` 从 Claude 上下文中完全移除。

> 注意：`user-invocable` 只控制菜单可见性，不控制 Skill 工具访问。要阻止程序化调用，使用 `disable-model-invocation: true`。

---

# 八、内置 Skill（Bundled Skills）

`Claude Code` 在每个会话中内置一组 Skill，与内置命令一起显示在 `/` 菜单中。与大多数执行固定逻辑的内置命令不同，内置 Skill 是**基于提示词的**：它们给 Claude 提供详细的操作手册，让它使用工具编排工作。

| 命令 | 说明 |
|------|------|
| `/batch <instruction>` | 大规模并行改造。研究代码库后将任务拆分为 5-30 个独立单元，在独立 git worktree 中启动多个后台 agent 并行执行、跑测试、开 PR。适合大型迁移和跨文件重构。 |
| `/claude-api [migrate\|managed-agents-onboard]` | 为 Claude API / Anthropic SDK 开发加载参考材料，覆盖 tool use、streaming、batches、structured outputs 等。 |
| `/debug [description]` | 开启 debug logging 并读取日志排查问题。 |
| `/loop [interval] [prompt]` | 循环运行 Prompt。可指定间隔或让 Claude 自行控制节奏。别名：`/proactive`。 |
| `/simplify [focus]` | 检查最近变更的文件，寻找代码复用、质量和效率问题并尝试修复。 |
| `/fewer-permission-prompts` | 分析常用只读命令和 MCP 工具调用，自动生成推荐允许规则，减少权限确认弹窗。 |

---

# 九、Skill 与相关机制的关系

## 1、Skill 与 Subagent

Skill 和 Subagent 是 `Claude Code` 中两个互补的扩展机制：

- **Skill**：定义"做什么"和"怎么做"，是可复用的指令模板
- **Subagent**：定义"谁来执行"，是具有独立上下文、工具权限和系统提示的专门代理

两者的协作方式：

1. **Skill 在子代理中运行**：通过 `context: fork` + `agent` 字段，让 Skill 的内容作为任务在隔离的子代理上下文中执行
2. **子代理预加载 Skill**：通过子代理 frontmatter 的 `skills` 字段，在子代理启动时将 Skill 的完整内容注入其上下文，作为领域知识参考

子代理**不会继承**父对话的 Skill，必须通过 `skills` 字段显式列出。每个预加载 Skill 的**完整内容**都会注入，而不仅仅是可调用入口。

> 设置了 `disable-model-invocation: true` 的 Skill 不能预加载到子代理中，因为预加载使用的是 Claude Code 可调用的 Skill 集合。

## 2、Skill 与 CLAUDE.md 的对比与选择

| 维度 | CLAUDE.md | Skill |
|------|-----------|-------|
| **加载时机** | 每次会话启动自动加载 | 仅在调用时加载 |
| **内容类型** | 事实、规则、约束 | 流程、任务、操作手册 |
| **适用场景** | 每次对话都应知道的信息 | 特定场景才需要的步骤 |
| **上下文成本** | 始终占用 | 按需占用，几乎为零直到调用 |
| **调用方式** | 自动注入 | `/skill-name` 手动或 Claude 自动 |
| **是否可传参** | 否 | 是 |
| **是否可隔离运行** | 否 | 是（`context: fork`） |

**选择建议**：
- 如果某条内容是"Claude 每次都应该知道的事实"，放入 `CLAUDE.md`
- 如果某条内容是"特定场景下才执行的步骤"，封装为 Skill
- 如果 `CLAUDE.md` 的某个章节已经成长为多步骤流程，考虑将其提取为 Skill

## 3、Skill 在扩展体系中的位置

Claude Code 的扩展能力从底层到上层可分为四个层次：

| 层次 | 机制 | 触发方式 | 适用场景 | 复杂度 |
|------|------|----------|----------|--------|
| **MCP Prompts** | MCP Server 暴露的 Prompt | `/mcp__<server>__<prompt>` | 调用外部工具能力 | 中等 |
| **Skill** | SKILL.md 定义的可复用能力 | `/skill-name` 或自动加载 | 封装方法论与工作流 | 低 |
| **Subagent** | 独立上下文、工具权限的专门代理 | 自动委托或 `@提及` | 隔离高输出、并行研究 | 中 |
| **Plugin** | 打包 Skills、Agents、Hooks、MCP Servers | 插件安装与启用 | 分发完整功能包 | 高 |

> 旧式 `.claude/commands/*.md` 自定义命令已并入 Skill 机制。

---

# 十、Skill 的共享与分发

- **项目 Skill**：将 `.claude/skills/` 提交到版本控制，团队共享
- **插件**：在插件中创建 `skills/` 目录，随插件分发
- **托管设置**：通过 managed settings 在组织范围部署

---

# 十一、故障排查

## 1、Skill 未触发

1. 检查 `description` 是否包含用户自然会说到的关键词
2. 确认 Skill 出现在可用列表中（询问 "What skills are available?"）
3. 尝试重新措辞以更接近 `description`
4. 如果是 `user-invocable`，直接用 `/skill-name` 调用

## 2、Skill 触发过于频繁

1. 让 `description` 更具体
2. 添加 `disable-model-invocation: true` 仅允许手动调用

## 3、Skill 描述被截断

Skill 描述加载到上下文让 Claude 知道可用 Skill。所有 Skill 名称始终包含，但如果 Skill 很多，描述会被缩短以适应字符预算（动态为上下文窗口的 1%，保底 8000 字符）。每个条目的 `description` + `when_to_use` 文本上限为 1536 字符。

可通过设置 `SLASH_COMMAND_TOOL_CHAR_BUDGET` 环境变量提高限制，或在源头精简描述：将关键用例前置，因为每个条目的合并文本无论如何都被限制在 1536 字符。

---

## 关联笔记

- [[1、Claude Code入门]] — Claude Code 的安装、配置与基础使用
- [[2、Slash命令]] — Slash 命令体系，包括内置 Skill 命令速查
- [[3、记忆机制]] — CLAUDE.md 与 Auto Memory 的详细机制
- [[5、Subagent]] — 子代理的创建、配置与使用模式
- [[6、MCP]] — MCP Server 与 Prompts 命令
- [[7、Plugin]] — 插件机制，包括插件 Skill 的命名空间调用
