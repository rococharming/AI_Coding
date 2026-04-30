# 一、概述

**Skill** 是 Claude Code 生态中用于封装可复用能力的核心机制。它将特定领域的知识、操作流程和最佳实践打包成标准化模块，供用户在会话中通过 `/skill-name` 调用，或由 Claude Code 在相关场景下自动加载触发。

Skill 的定位介于"一次性提示词"与"完整子代理"之间：它比临时指令更结构化、可复用，又比子代理更轻量、无需独立上下文窗口。在 Claude Code 中，Skill 与 Slash 命令、插件、子代理共同构成了多层次的扩展能力体系。

> Skill 的本质是**用结构化文档（SKILL.md）定义可复用的 AI 工作流**，让 Claude Code 在特定场景下自动遵循预设的方法论和操作步骤。

# 二、Skill 在 Claude Code 中的位置

## 1、四层扩展能力体系

Claude Code 的扩展能力从底层到上层可分为四个层次：

| 层次 | 机制 | 触发方式 | 适用场景 | 复杂度 |
|------|------|----------|----------|--------|
| **MCP Prompts** | MCP Server 暴露的 Prompt | `/mcp__<server>__<prompt>` | 调用外部工具能力 | 中等 |
| **Skill** | SKILL.md 定义的可复用能力 | `/skill-name` 或自动加载 | 封装方法论与工作流 | 低 |
| **插件** | 打包的 Skills + Agents + Hooks + MCP | 命名空间调用如 `my-plugin:hello` | 跨项目复用完整能力包 | 高 |
| **子代理** | 独立上下文 + 自定义系统提示的 Agent | 自动委托或手动调用 | 隔离任务、专业化处理 | 高 |

> 旧式 `.claude/commands/*.md` 自定义命令已并入 Skill 机制，仍兼容读取，但新写法推荐使用 `.claude/skills/<skill-name>/SKILL.md`。

## 2、Skill 与内置命令的区别

Claude Code 的 `/` 菜单同时包含**内置命令**和**内置 Skill**，两者容易混淆：

| 类型 | 本质 | 示例 | 是否可自定义 |
|------|------|------|------------|
| 内置命令 | Claude Code CLI 的固定逻辑 | `/clear`、`/model`、`/compact` | 不可 |
| 内置 Skill | Anthropic 随 Claude Code 分发的 Skill | `/batch`、`/debug`、`/loop`、`/simplify` | 不可修改，但可参考其写法 |
| 自定义 Skill | 用户或项目自行编写的 SKILL.md | 任意自定义名称 | 可完全自定义 |

# 三、Skill 的核心结构

## 1、SKILL.md 文件格式

Skill 通过 `SKILL.md` 文件定义，采用 **YAML frontmatter + Markdown 正文** 的标准格式：

```yaml
---
name: skill-name
description: 该 Skill 的触发条件描述，说明在什么场景下应该调用此 Skill
---

# Skill 名称

## 触发时机

- 用户说"xxx"时触发
- 检测到 yyy 场景时自动加载

## 执行流程

### 1. 步骤一
...

### 2. 步骤二
...

## 边界与约束

- 不要修改 xxx
- 如果 yyy 则告知用户
```

## 2、关键字段说明

| 字段 | 说明 | 是否必填 |
|------|------|----------|
| `name` | Skill 的唯一标识符，决定 `/` 命令名称 | 是 |
| `description` | 触发条件描述，Claude Code 据此判断是否自动加载 | 是 |
| 正文 Markdown | 具体的执行流程、约束条件、输出格式等 | 是 |

## 3、存放位置与作用范围

Skill 文件可以存放在不同位置，对应不同的生效范围：

| 位置 | 范围 | 用途 |
|------|------|------|
| `.claude/skills/<skill-name>/SKILL.md` | 当前项目 | 项目专属的工作流封装 |
| `~/.claude/skills/<skill-name>/SKILL.md` | 个人所有项目 | 跨项目复用的个人 Skill |
| 插件内 | 启用该插件的位置 | 第三方分发的标准化能力 |

# 四、内置 Skill 速查

Claude Code 内置了多个实用 Skill，可通过 `/` 菜单直接调用：

| Skill 命令 | 功能 | 典型场景 |
|-----------|------|----------|
| `/batch <指令>` | 大规模并行改造，拆分任务到多个 worktree | 批量重构、多文件同步修改 |
| `/claude-api` | Claude API / Anthropic SDK 开发辅助 | 构建基于 Claude API 的应用 |
| `/debug` | 开启调试日志排查问题 | 定位 Claude Code 异常行为 |
| `/loop [间隔] [prompt]` | 循环运行 Prompt（别名 `/proactive`） | 定时检查、持续监控任务 |
| `/simplify` | 检查代码复用、质量和效率问题 | 代码审查、重构优化 |
| `/fewer-permission-prompts` | 自动生成权限允许规则 | 减少重复权限确认 |

> 输入 `/` 后，Claude Code 会显示当前环境所有可用的命令列表，实际可用项以该列表为准。

# 五、Skill 与相关机制的协作

## 1、Skill 与 CLAUDE.md 的分工

| 机制 | 定位 | 适合存放的内容 | 不适合存放的内容 |
|------|------|----------------|------------------|
| **CLAUDE.md** | 项目长期上下文 | 编码规范、目录约束、构建命令、全局规则 | 多步骤流程、特定区域规则 |
| **Skill** | 可复用工作流 | 特定场景的方法论、操作步骤、检查清单 | 全局性、始终生效的基础约束 |

> 如果某条内容属于**多步骤流程**，或只适用于代码库中的**某个特定区域**，更推荐放入 Skill 或路径限定规则中，而非 CLAUDE.md。

## 2、Skill 与子代理的协作

Skill 和子代理（Subagent）可以形成互补：

- **Skill 定义"做什么"**：提供方法论、流程模板和约束条件
- **子代理执行"怎么做"**：在独立上下文中实际执行任务

典型协作模式：

```
主会话加载 "代码审查" Skill → 触发审查流程 → 派遣 code-reviewer 子代理执行具体审查 → 返回结果
```

子代理的配置中可以通过 `skills` 字段预加载特定 Skill：

```yaml
---
name: code-review
description: 资深代码审查专家
skills: [review-checklist, security-guidelines]
---
```

## 3、Skill 与 Superpowers 框架的关系

[[Superpowers]] 是一套跨平台的 AI 编程技能框架，它将软件开发方法论封装为标准化 Skill。Superpowers 中的每个阶段（头脑风暴、编写计划、子代理驱动开发等）本质上都是 Skill 的具体实践：

| Superpowers 阶段 | 对应的 Skill 能力 |
|------------------|-------------------|
| 头脑风暴 | 苏格拉底式提问 Skill |
| 编写计划 | 任务分解与规划 Skill |
| 子代理驱动开发 | 并行代理派遣 Skill |
| 测试驱动开发 | TDD 红-绿-重构 Skill |
| 代码审查 | 两阶段审查 Skill |

> Superpowers 证明了 Skill 机制在规模化软件开发中的价值：将最佳实践固化为可重复触发的标准流程。

# 六、编写自定义 Skill 的最佳实践

## 1、设计原则

1. **聚焦单一职责**：每个 Skill 只解决一个明确场景，避免大而全
2. **明确触发条件**：`description` 要清晰描述"在什么情况下使用该 Skill"
3. **流程化输出**：将操作步骤拆解为编号阶段，便于 Claude Code 遵循
4. **声明边界约束**：明确说明 Skill 不做什么，防止过度扩展

## 2、典型 Skill 结构模板

```markdown
---
name: my-skill
description: 当用户需要执行 XXX 操作时触发
---

# Skill 标题

## 触发时机

- 用户明确请求 xxx
- 检测到 yyy 场景

## 执行流程

### 1. 准备阶段
...

### 2. 执行阶段
...

### 3. 验证阶段
...

## 输出格式

...

## 边界与约束

- 不要修改 wiki/ 目录
- 如果 zzz 则停止并询问用户
```

## 3、测试与迭代

- 编写完成后，在真实会话中测试 Skill 的触发和执行效果
- 根据实际表现调整 `description` 的精确度
- 收集边界案例，补充约束条件

# 七、常见问题

| 问题 | 解答 |
|------|------|
| Skill 和自定义命令有什么区别？ | 旧式 `.claude/commands/*.md` 已并入 Skill 机制，功能等价，但 Skill 支持更丰富的 frontmatter 和结构化流程定义 |
| Skill 会被自动触发吗？ | 取决于 `description` 的匹配度。描述越精确，自动触发越可靠 |
| 一个项目可以有多个 Skill 吗？ | 可以，按场景拆分，每个 Skill 聚焦一个具体任务 |
| Skill 可以调用其他 Skill 吗？ | 不能直接嵌套调用，但可以通过子代理的 `skills` 字段预加载 |
| 内置 Skill 可以修改吗？ | 不能修改，但可以通过编写同名自定义 Skill 覆盖（作用域优先级决定） |

# 八、补充

1. **查看可用 Skill**：在 Claude Code 会话中输入 `/`，浏览所有可用命令和 Skill
2. **Skill 与插件命名空间**：插件中的 Skill 使用命名空间调用（如 `my-plugin:hello`），避免与个人 Skill 冲突
3. **权限继承**：Skill 执行时继承当前会话的权限模式，如需特殊权限需在流程中说明
4. **参考内置 Skill**：Claude Code 内置的 `/batch`、`/simplify` 等 Skill 是编写自定义 Skill 的最佳参考

---

> 本笔记综合了 Claude Code 官方文档、Superpowers 框架实践以及子代理协作模式，聚焦 Skill 机制的核心概念与使用方式。
