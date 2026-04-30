# 一、概述

**Skills** 是 `Claude Code` 的扩展机制，通过编写 `SKILL.md` 文件定义可复用的指令集，让 Claude 获得新能力。与每次会话都自动加载的 `CLAUDE.md` 不同，Skills **按需加载**——只有在用户手动调用（`/skill-name`）或 Claude 判断相关时才会进入上下文，因此长参考材料几乎不产生日常上下文成本。

Skills 遵循 [Agent Skills](https://agentskills.io/) 开放标准，这意味着一份遵循规范的 `SKILL.md` 可以在多个支持该标准的 AI 工具间复用。`Claude Code` 在此基础上增加了调用控制、子代理执行、动态上下文注入等扩展能力。

在 `Claude Code` 的交互体系中，Skills 与以下几类机制紧密相关：
- `CLAUDE.md`：始终加载的项目上下文，适合存放全局规则（详见[[3、记忆机制]]）
- **Slash 命令**：`/` 菜单中既包含内置固定逻辑命令，也包含 Skill 命令（详见[[2、Slash命令]]）
- **Subagent**：Skill 可通过 `context: fork` 在隔离子代理中执行（详见[[5、Subagent]]）

> **何时使用 Skill**：当你反复粘贴相同的操作手册、检查清单或多步骤流程时；当 `CLAUDE.md` 中某部分内容已演变为"流程"而非"事实"时；当需要封装副作用操作（如部署）并严格控制触发时机时。

# 二、核心概念

## 1、Skills 存储作用域

Skill 的存放位置决定了它的生效范围。`Claude Code` 支持四级作用域：

| 级别 | 路径 | 适用范围 | 覆盖优先级 |
|------|------|----------|-----------|
| **Enterprise** | 由 managed settings 配置 | 组织内所有用户 | 最高 |
| **Personal** | `~/.claude/skills/<name>/SKILL.md` | 当前用户的所有项目 | 中高 |
| **Project** | `.claude/skills/<name>/SKILL.md` | 仅当前项目 | 中 |
| **Plugin** | `<plugin>/skills/<name>/SKILL.md` | 插件启用处 | 独立命名空间 |

同名 Skill 的覆盖规则：**Enterprise > Personal > Project**。Plugin Skills 使用 `plugin-name:skill-name` 命名空间，不会与其他级别冲突。

旧版的 `.claude/commands/<name>.md` 自定义命令仍然兼容，但新写法推荐使用 `.claude/skills/<name>/SKILL.md`，因为 Skills 支持 frontmatter、支持文件和自动加载等更多特性。

### 自动发现机制

- `Claude Code` **实时监控** skill 目录的增删改，当前会话内即时生效
- 编辑子目录中的文件时，自动发现嵌套的 `.claude/skills/`（支持 monorepo 场景）
- `--add-dir` 附加目录中的 `.claude/skills/` 也会被加载

## 2、SKILL.md 文件结构

每个 Skill 是一个独立目录，`SKILL.md` 为入口文件（必需），可附带支持文件：

```text
my-skill/
├── SKILL.md           # 主指令（必需）
├── template.md        # 供 Claude 填写的模板（可选）
├── examples/
│   └── sample.md      # 预期输出格式示例（可选）
└── scripts/
    └── validate.sh    # Claude 可执行的脚本（可选）
```

> 建议 `SKILL.md` 保持在 **500 行以内**，详细参考材料放入独立文件，在 `SKILL.md` 中通过相对路径引用。

## 3、Frontmatter 配置

在 `SKILL.md` 顶部通过 YAML frontmatter 控制 Skill 的行为：

```yaml
---
name: my-skill              # 显示名称（默认使用目录名）
description: What this skill does and when to use it
when_to_use: 额外触发场景说明
argument-hint: "[issue-number]"
disable-model-invocation: true
user-invocable: false
allowed-tools: Read Grep Bash(git *)
context: fork
agent: Explore
paths: "src/**/*.ts"
---
```

**常用 frontmatter 字段说明**：

| 字段 | 必填 | 说明 |
|------|------|------|
| `name` | 否 | 显示名称，默认使用目录名 |
| `description` | **推荐** | Skill 的功能说明，Claude 用它判断是否调用 |
| `when_to_use` | 否 | 额外触发场景，与 `description` 共享 1536 字符上限 |
| `disable-model-invocation` | 否 | `true` 时仅用户可调用，防止 Claude 自动触发 |
| `user-invocable` | 否 | `false` 时从 `/` 菜单隐藏，仅 Claude 自动调用 |
| `allowed-tools` | 否 | Skill 激活期间免确认的工具列表 |
| `context` | 否 | 设为 `fork` 时在子代理中执行 |
| `agent` | 否 | 子代理类型：`Explore` / `Plan` / `general-purpose` |
| `paths` | 否 | 仅匹配文件被编辑时自动激活 |

## 4、调用控制

Skill 默认支持两种调用方式：用户手动输入 `/skill-name`，以及 Claude 在相关场景中自动加载。通过 frontmatter 可以精细控制：

**调用控制矩阵**：

| 配置 | 用户可 `/name` | Claude 可自动调用 | 加载方式 |
|------|---------------|-------------------|----------|
| （默认） | Yes | Yes | Description 常驻上下文，完整内容调用时加载 |
| `disable-model-invocation: true` | Yes | No | Description 不加载，用户调用时加载完整内容 |
| `user-invocable: false` | No | Yes | Description 常驻上下文，Claude 自动触发 |

> **建议**：有副作用的操作（如 `/deploy`、发送消息）设置 `disable-model-invocation: true`；纯背景知识（如旧系统说明）设置 `user-invocable: false`。

## 5、参数传递

Skill 支持多种占位符替换，用于接收调用时传入的参数：

| 占位符 | 说明 | 示例 |
|--------|------|------|
| `$ARGUMENTS` | 全部参数原样传入 | `/fix 123` → `123` |
| `$ARGUMENTS[N]` / `$N` | 按 0-based 索引取参数 | `$0`, `$1`, `$2` |
| `$name` | frontmatter 声明的命名参数 | `arguments: [issue, branch]` |
| `${CLAUDE_SESSION_ID}` | 当前会话 ID | 用于日志命名 |
| `${CLAUDE_EFFORT}` | 当前 effort 级别 | `low` / `medium` / `high` |
| `${CLAUDE_SKILL_DIR}` | Skill 目录路径 | 引用捆绑脚本 |

示例——迁移组件 Skill：

```yaml
---
name: migrate-component
description: Migrate a component from one framework to another
---

Migrate the $0 component from $1 to $2.
Preserve all existing behavior and tests.
```

调用方式：`/migrate-component SearchBar React Vue`

## 6、动态上下文注入

使用 `` !`command` `` 语法可以在 Skill 内容发送给 Claude **之前**执行 shell 命令，将命令输出替换到 prompt 中：

```markdown
---
name: pr-summary
description: Summarize changes in a pull request
context: fork
agent: Explore
allowed-tools: Bash(gh *)
---

## Pull request context
- PR diff: !\`gh pr diff\`
- PR comments: !\`gh pr view --comments\`
- Changed files: !\`gh pr diff --name-only\`

## Your task
Summarize this pull request...
```

多行命令使用 ` ```! ` 代码块：

````markdown
## Environment
```!
node --version
npm --version
```
````

> 这是**预处理**，不是 Claude 执行。Claude 只收到最终渲染后的内容。管理员可在 settings 中设置 `"disableSkillShellExecution": true` 禁用此行为。

## 7、子代理执行

添加 `context: fork` 让 Skill 在隔离上下文中运行，适合需要独立探索或长时运行的任务：

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

**Skill 与 Subagent 的两种协作模式**：

| 方式 | System Prompt | 任务来源 | 额外加载 |
|------|--------------|----------|----------|
| Skill 带 `context: fork` | 由 `agent` 字段决定 | `SKILL.md` 内容 | `CLAUDE.md` |
| Subagent 带 `skills` 字段 | Subagent 的 markdown 正文 | Claude 的委派消息 | 预加载 Skills + `CLAUDE.md` |

# 三、使用方法

## 1、创建第一个 Skill

以项目级 Skill 为例，在 `.claude/skills/explain-code/SKILL.md` 创建：

```yaml
---
name: explain-code
description: Explain code using visual diagrams and analogies
---

Explain the provided code:
1. Identify the core logic and data flow
2. Create a mental model using an analogy
3. Describe any tricky edge cases
```

创建后，在 `Claude Code` 中输入 `/` 即可看到 `/explain-code`，或在对话中直接问"解释这段代码"让 Claude 自动加载。

## 2、捆绑技能速查

`Claude Code` 官方内置了若干基于 prompt 的 Skill，通过 `/` 调用：

| 命令 | 功能 |
|------|------|
| `/batch <指令>` | 大规模并行改造，拆分任务到多个 worktree |
| `/claude-api` | Claude API / Anthropic SDK 开发辅助 |
| `/debug` | 开启调试日志排查问题 |
| `/loop [间隔] [prompt]` | 循环运行 Prompt（别名: `/proactive`） |
| `/simplify` | 检查代码复用、质量和效率问题 |
| `/fewer-permission-prompts` | 分析常用命令，生成允许规则减少权限确认 |

## 3、验证与调试

1. **检查是否加载**：启动时查看 `What skills are available?` 提示
2. **手动测试**：直接输入 `/skill-name` 调用
3. **描述匹配**：确保 `description` 包含用户可能使用的自然语言关键词
4. **触发过于频繁**：添加 `disable-model-invocation: true` 或使描述更具体
5. **诊断配置**：参考官方 [Debug your configuration](https://code.claude.com/docs/en/debug-your-config)

# 四、Skill 与相关机制的对比

## 1、Skill vs CLAUDE.md vs Memory vs Subagent

| 机制 | 加载时机 | 作用范围 | 典型内容 |
|------|----------|----------|----------|
| **CLAUDE.md** | 会话开始时**始终加载** | 项目级 | 编码规范、架构决策、全局规则 |
| **Skill** | **按需加载**（调用时） | 四级作用域 | 操作流程、检查清单、领域知识 |
| **Memory** | 按需检索 | 用户/项目级 | 偏好、历史经验、跨会话事实 |
| **Subagent** | 任务委派时创建 | 单次任务 | 隔离执行环境，可预加载 Skills |

> **选择建议**：始终需要遵守的规则放 `CLAUDE.md`；可复用的操作流程放 Skill；从协作中学习到的偏好让 Auto Memory 自动沉淀。

## 2、生命周期与上下文管理

- Skill 被调用后，其内容作为**单条消息**进入会话并持续存在
- 自动压缩（auto-compaction）时保留最近调用的 Skill，每 Skill 前 **5000 tokens**，共享 **25000 tokens** 预算
- 如果 Skill 在压缩后似乎失效，可**重新调用**以恢复完整内容
- 在子代理中预加载的 Skill 则会在子代理启动时**全量注入**

# 五、补充

## 1、Skill 与 Slash 命令的关系

在 `Claude Code` 的 `/` 菜单中，命令来源有三类：

1. **内置命令**：固定逻辑（如 `/clear`、`/model`）
2. **内置 Skill**：基于 prompt 的 Skill（如 `/batch`、`/debug`）
3. **自定义 Skill**：用户或插件定义的 Skill

对使用者而言，调用方式没有区别——都是输入 `/` 加名称。区别在于底层实现：内置命令由 CLI 直接执行，而 Skill 是 prompt-based，由 Claude 读取 playbook 后自主编排工具完成。

## 2、旧版自定义命令迁移

旧式 `.claude/commands/<name>.md` 仍然兼容，调用方式相同。迁移到 Skills 只需要：

```bash
# 旧
.claude/commands/deploy.md

# 新
.claude/skills/deploy/SKILL.md
```

迁移后可使用 frontmatter 控制调用行为，并支持附加支持文件。
