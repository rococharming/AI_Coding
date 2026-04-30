# 一、概述

**子代理（Subagent）** 是专门处理特定任务的 AI 助手，拥有独立的上下文窗口、自定义系统提示词和特定的工具权限。当主代理判断当前任务符合某个子代理的 `description` 描述时，会自动将任务委托给它，由子代理独立完成后返回结果。

子代理的核心价值在于**上下文隔离**与**任务专业化**：把探索、审查、测试等独立任务派出去执行，主对话只接收精炼后的结论，避免冗长中间输出污染主上下文。同时，每个子代理可针对特定场景深度定制，实现权限控制、模型选择和跨项目复用。

> 注意：Subagent 在**单个会话内**工作。如果需要多个 agent 并行工作并相互通信，需要用到 agent teams。

# 二、核心优势

| 优势 | 说明 |
|------|------|
| **上下文保护** | 将探索和实现过程隔离到独立上下文，避免污染主对话 |
| **权限隔离** | 通过限制可用工具强制执行约束（如只读审查器） |
| **专业化** | 每个子代理针对特定领域深度定制 |
| **成本控制** | 简单任务可路由到更快、更便宜的模型 |
| **跨项目复用** | 用户级子代理可在多个项目中共享 |

# 三、内置 Subagents

Claude Code 内置了若干子代理，会在合适时自动调用。

| 子代理 | 模型 | 工具限制 | 用途 |
|--------|------|----------|------|
| **Explore** | Haiku | 只读工具（禁止 Write/Edit） | 快速搜索和分析代码库 |
| **Plan** | 继承自主对话 | 只读工具 | 规划模式下的代码库研究 |
| **General-purpose** | 继承自主对话 | 所有工具 | 复杂研究、多步骤操作、代码修改 |
| **statusline-setup** | Sonnet | — | 运行 `/statusline` 配置状态栏时 |
| **Claude Code Guide** | Haiku | — | 询问 Claude Code 功能相关问题时 |

Explore 代理在调用时可指定探索细致程度：`quick`（目标明确查找）、`medium`（平衡性探索）、`very thorough`（全面分析）。

# 四、创建与配置子代理

## 1、通过 /agents 命令交互式创建

执行 `/agents` 命令打开子代理管理界面：

- **Running** 标签：显示正在运行的子代理，可打开或停止
- **Library** 标签：查看、创建、编辑、删除子代理

创建流程：
1. 切换到 `Library` → `Create new agent`，选择存放位置（Project / User）
2. 描述子代理角色和触发时机（可用 `Generate with Claude` 自动生成）
3. 选择工具权限（白名单/继承/只读）
4. 选择模型（`sonnet` / `opus` / `haiku` / `inherit`）
5. 选择预览背景色（便于区分子代理运行状态）
6. 配置持久记忆作用域（`user` / `project` / `local` / `None`）
7. 保存并试用

命令行列出所有子代理：
```bash
claude agents
```

## 2、手动编写子代理文件

子代理文件本质上是 **YAML frontmatter + Markdown system prompt** 的 Markdown 文件。

```markdown
---
name: code-review
description: 资深代码审查专家。在代码更改后主动使用。
tools: Read, Glob, Grep, Bash
model: sonnet
permissionMode: default
memory: project
---

你是一名代码审查员。被调用时，请分析代码，并针对代码质量、安全性和最佳实践提供具体、可执行的反馈。
```

> 手动添加文件后，需**重启会话**或使用 `/agents` 立即加载。

### 关键 frontmatter 字段

| 字段 | 必填 | 说明 |
|------|:--:|------|
| `name` | 是 | 唯一标识符，小写字母和连字符 |
| `description` | 是 | 触发条件描述（"在什么情况下委托给该子代理"） |
| `tools` | 否 | 白名单工具；省略则继承所有 |
| `disallowedTools` | 否 | 黑名单工具，从继承列表中移除 |
| `model` | 否 | `sonnet` / `opus` / `haiku` / `inherit` |
| `permissionMode` | 否 | `default` / `acceptEdits` / `auto` / `dontAsk` / `bypassPermissions` / `plan` |
| `maxTurns` | 否 | 最大思考+行动轮数 |
| `skills` | 否 | 预加载技能（完整内容注入上下文） |
| `mcpServers` | 否 | 可用 MCP 服务器（可内联定义或引用） |
| `hooks` | 否 | 生命周期钩子（如 `PreToolUse`） |
| `memory` | 否 | 持久记忆作用域：`user` / `project` / `local` |
| `background` | 否 | `true` 时作为后台任务运行 |
| `effort` | 否 | 推理努力级别：`low` / `medium` / `high` / `xhigh` / `max` |
| `isolation` | 否 | `worktree` 时在隔离 git worktree 中运行 |
| `color` | 否 | 显示颜色：`red` / `blue` / `green` / `yellow` / `purple` / `orange` / `pink` / `cyan` |
| `initialPrompt` | 否 | 作为主会话代理运行时的自动首条用户消息 |

## 3、子代理作用域与优先级

当多个位置定义同名子代理时，按优先级生效：

| 优先级 | 位置 | 范围 | 创建方式 |
|:------:|------|------|----------|
| 1 | 托管设置 | 组织范围 | 托管策略部署 |
| 2 | `--agents` CLI 标志 | 当前会话 | 启动时传入 JSON |
| 3 | `.claude/agents/` | 当前项目 | 交互式或手动创建 |
| 4 | `~/.claude/agents` | 个人所有项目 | 交互式或手动创建 |
| 5 | 插件 | 启用该插件的位置 | 随插件安装 |

项目子代理会从当前工作目录**向上查找**发现。`--add-dir` 添加的目录只授予文件访问权限，**不会扫描其中的子代理配置**。

CLI 快速定义多个子代理：
```bash
claude --agents '{
  "code-reviewer": {
    "description": "资深代码审查专家。在代码更改后主动使用。",
    "prompt": "你是一名高级代码审查员。重点关注代码质量、安全性和最佳实践。",
    "tools": ["Read", "Grep", "Glob", "Bash"],
    "model": "sonnet"
  }
}'
```

# 五、控制子代理的能力

## 1、工具权限控制

- **`tools` 白名单**：只允许使用指定工具
- **`disallowedTools` 黑名单**：继承全部工具后排除指定工具
- 若同时设置，先继承/获取全部 → 删 `disallowedTools` → 用 `tools` 筛选
- 某工具同时在两者中，**最终被禁用**

限制子代理生成其他子代理：
```yaml
tools: Agent(worker, researcher), Read, Bash  # 只允许生成 worker 和 researcher
```

完全省略 `Agent` 则该代理不能生成任何子代理。

## 2、MCP 服务器限定

支持**内联定义**（仅该子代理可用）和**字符串引用**（复用父会话连接）：

```yaml
mcpServers:
  - playwright:
      type: stdio
      command: npx
      args: ["-y", "@playwright/mcp@latest"]
  - github
```

> 内联定义的服务器在子代理启动时连接、结束时断开。若希望 MCP 服务器完全不进入主对话，应以内联方式定义而非放在 `.mcp.json` 中。

## 3、权限模式

| 模式 | 行为 |
|------|------|
| `default` | 标准权限检查，需要时提示 |
| `acceptEdits` | 自动接受工作目录内文件编辑 |
| `auto` | 后台分类器检查命令和受保护目录写入 |
| `dontAsk` | 自动拒绝权限提示；显式允许的工具仍可工作 |
| `bypassPermissions` | 跳过权限提示 |
| `plan` | 计划模式，只读探索 |

> 父级使用 `bypassPermissions` 或 `acceptEdits` 时，父级设置优先，子代理无法覆盖。

## 4、持久记忆

`memory` 字段给子代理一个可跨对话保留的持久记忆目录：

| 作用域 | 位置 | 适用场景 |
|--------|------|----------|
| `user` | `~/.claude/agent-memory/<name>/` | 跨所有项目共享知识 |
| `project` | `.claude/agent-memory/<name>/` | 项目特定知识，可版本控制共享 |
| `local` | `.claude/agent-memory-local/<name>/` | 项目特定但不上传 Git |

启用后：
- 子代理系统提示词包含读写记忆目录的说明
- 自动加载 `MEMORY.md` 前 200 行或 25KB
- `Read`、`Write`、`Edit` 工具自动启用

建议：在子代理 Markdown 中增加记忆指令，让它主动维护知识库：
```markdown
当你发现代码路径、设计模式、库的位置以及关键架构决策时，及时更新你的代理记忆。
```

## 5、条件规则钩子

使用 `PreToolUse` 钩子动态控制工具使用：

```yaml
---
name: db-reader
description: 执行只读数据库查询
tools: Bash
hooks:
  PreToolUse:
    - matcher: "Bash"
      hooks:
        - type: "command"
          command: "./scripts/validate-readonly-query.sh"
---
```

脚本通过 `stdin` 接收 JSON 格式的命令，退出码 0 表示允许，2 表示阻止。

## 6、禁用特定子代理

在 `.claude/settings.json` 中：
```json
{
  "permissions": {
    "deny": ["Agent(Explore)", "Agent(my-custom-agent)"]
  }
}
```

或通过 CLI：
```bash
claude --disallowedTools "Agent(Explore)"
```

# 六、使用子代理

## 1、触发方式

| 方式 | 说明 |
|------|------|
| **自动委托** | Claude Code 根据 `description` 自动判断并调用 |
| **自然语言** | 在请求中点名使用某个子代理 |
| **@提及** | 输入 `@` 从提示列表中选择 |
| **CLI 启动** | `claude --agent code-review` 让整个会话以子代理身份运行 |
| **默认代理** | 在 `settings.json` 中设置 `"agent": "code-reviewer"` |

> 在 `description` 中添加 "use proactively" 等短语，可促进 Claude Code 主动委托。

## 2、前台与后台运行

| 模式 | 特点 |
|------|------|
| **前台** | 阻塞主会话，权限提示和澄清问题传递给你 |
| **后台** | 并发运行，启动前提示授予所有工具权限；`Ctrl + B` 可将前台任务转后台 |

设置环境变量禁用后台任务：
```bash
export CLAUDE_CODE_DISABLE_BACKGROUND_TASKS=1
```

## 3、常见使用模式

### （1）隔离高输出量操作

将产生大量中间内容的任务委托给子代理，主对话只接收摘要：
- 运行测试套件
- 分析日志文件
- 扫描大型代码库
- 获取大量文档

```text
使用一个子代理运行测试套件，并只报告失败的测试及其错误信息。
```

### （2）并行研究

多个独立调查任务同时启动多个子代理并行处理：

```text
使用不同的子代理并行研究认证模块、数据库模块和API模块。
```

> 注意：子代理结果返回主对话，若同时运行很多且每个返回详细内容，主对话仍可能消耗大量上下文。

### （3）串联工作流

多步骤任务按顺序调用多个子代理，形成流水线：

```text
先使用 code-reviewer 查找性能问题，然后使用 optimizer 修复这些问题。
```

适合：先分析再修改、先研究再实现、先审查再优化。

## 4、主对话 vs 子代理的选择策略

| 场景 | 推荐方式 |
|------|----------|
| 需要频繁沟通、调整方向、上下文连续 | **主对话** |
| 独立任务、大量中间输出 | **子代理** |
| 需要限制工具权限 | **子代理** |
| 专业角色处理（code-reviewer、debugger） | **子代理** |
| 很小、很明确的修改 | **主对话** |
| 希望响应更快 | **主对话** |

> 简单判断：如果任务可以"派出去做"，最后只要一个结果，就适合用子代理。

# 七、在 Superpowers 框架中的应用

[[Superpowers]] 框架大量使用子代理驱动开发，其标准化流程中的关键步骤：

1. **编写计划（Write Plan）**：将工作分解为小块任务
2. **子代理驱动开发**：为每个任务派遣子代理，进行两阶段审查（规格合规性 + 代码质量）
3. **请求代码审查**：对照计划审查，严重问题阻止进度
4. **派遣并行代理**：并发子代理工作流

Superpowers 通过子代理实现**测试驱动开发（TDD）**的红-绿-重构循环，以及系统化的代码审查流程。

# 八、常见问题与注意事项

| 问题 | 说明 |
|------|------|
| 子代理不能生成其他子代理 | `Agent(agent_type)` 语法仅在主会话代理定义中有效 |
| 插件子代理限制 | 不支持 `hooks`、`mcpServers`、`permissionMode` 字段 |
| 权限继承规则 | 父级 `bypassPermissions` / `acceptEdits` 优先，子代理无法覆盖 |
| 工作目录 | 子代理启动时位于主对话当前工作目录；`cd` 不在工具调用间持久化 |
| 上下文上限 | 并行子代理过多且返回详细内容时，主对话上下文仍可能超限 |
| 记忆加载限制 | `MEMORY.md` 只加载前 200 行或 25KB，主题文件按需读取 |

# 九、补充

## 速查：子代理文件模板

```markdown
---
name: my-agent
description: 描述何时委托给该子代理
tools: Read, Grep, Glob, Bash
model: sonnet
permissionMode: default
memory: project
color: blue
---

你是 [角色定义]。被调用时，请 [具体任务说明]。

## 记忆维护
当你发现代码路径、设计模式、库的位置以及关键架构决策时，及时更新你的代理记忆。
```

## 速查：常用命令

| 命令 | 作用 |
|------|------|
| `/agents` | 打开子代理管理界面 |
| `claude agents` | 列出所有已配置子代理 |
| `claude --agent <name>` | 以指定子代理启动会话 |
| `Ctrl + B` | 将前台子代理转为后台运行 |

---

## 关联连接

- [[Claude_Code]] — Claude Code 工具页（内置 Subagent 机制）
- [[Superpowers]] — Superpowers 技能框架（大量使用子代理驱动开发）
- [[Memory_System]] — 记忆系统（子代理持久记忆机制）
- [[Subagent]] — 子代理概念页（wiki 中的结构化知识）
- [[摘要-subagent]] — 原始素材摘要
