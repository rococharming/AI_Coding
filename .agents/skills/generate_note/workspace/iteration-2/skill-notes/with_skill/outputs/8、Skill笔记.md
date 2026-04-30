# 一、概述

**Skill** 是 Claude Code 生态中用于封装可复用方法论与工作流的核心扩展机制。它通过 `SKILL.md` 文件定义一套标准化的触发条件、执行流程和约束边界，让 Claude Code 能够在特定场景下自动加载并执行预设能力。

Skill 与 **Slash 命令**、**子代理（Subagent）**、**MCP Prompts** 共同构成 Claude Code 的扩展能力体系。其中 Skill 的定位是"封装方法论"——它将重复性的知识工作流固化为可自动触发的能力单元，降低每次任务的手动配置成本。

> Skill 的前身是 `.claude/commands/*.md` 自定义命令，现已统一并入 Skill 机制。

# 二、Skill 的核心结构

## 1、SKILL.md 文件格式

Skill 通过一个 `SKILL.md` 文件定义，采用 **YAML frontmatter + Markdown 正文** 的格式：

```yaml
---
name: skill-name
description: 描述该 Skill 的触发时机和功能定位
---

# Skill 标题

## 触发时机

- 用户说"xxx"时触发
- 用户要求"yyy"时调用

## 执行流程

### 1、步骤一
...

### 2、步骤二
...

## 边界与约束

- 不要修改 xxx 目录下的文件
- 如果 yyy 则如实告知用户
```

**关键字段说明**：

| 字段 | 说明 | 示例 |
|------|------|------|
| `name` | Skill 的唯一标识符 | `generate_note` |
| `description` | 触发条件描述，决定何时自动加载 | "当用户要求生成笔记时调用" |

## 2、Skill 的存放位置

Skill 文件通常存放在以下位置：

| 位置 | 范围 | 用途 |
|------|------|------|
| `.claude/skills/` | 当前项目 | 项目专属 Skill |
| `~/.claude/skills/` | 个人全局 | 跨项目复用的个人 Skill |
| 插件包内 | 随插件分发 | 插件提供的内置 Skill |

# 三、Skill 与相关机制的对比

## 1、扩展能力层次

Claude Code 的扩展能力从底层到上层可分为四个层次：

| 层次 | 机制 | 触发方式 | 适用场景 | 复杂度 |
|------|------|----------|----------|--------|
| **MCP Prompts** | MCP Server 暴露的 Prompt | `/mcp__<server>__<prompt>` | 调用外部工具能力 | 中等 |
| **Skill** | `SKILL.md` 定义的可复用能力 | `/skill-name` 或自动加载 | 封装方法论与工作流 | 低 |
| **子代理** | YAML + Markdown 定义的专用 Agent | 自动委托或手动调用 | 隔离上下文、专业化处理 | 中等 |
| **插件** | 完整的扩展包 | `/plugin install` | 跨平台能力集成 | 高 |

> 旧式 `.claude/commands/*.md` 自定义命令已并入 Skill 机制。

## 2、Skill vs 子代理

| 维度 | Skill | 子代理（Subagent） |
|------|-------|-------------------|
| **核心目的** | 封装工作流和方法论 | 隔离上下文、专业化处理任务 |
| **触发方式** | 关键词匹配自动加载 | 描述匹配自动委托 |
| **上下文** | 在主对话中执行 | 独立的上下文窗口 |
| **工具权限** | 继承主会话 | 可独立配置白名单/黑名单 |
| **适用场景** | 标准化流程（如生成笔记、代码审查） | 高输出量操作、并行研究、专业角色 |
| **配置复杂度** | 低（单文件） | 中等（YAML + 多字段） |

**选择策略**：
- 使用 **Skill**：任务需要遵循固定流程、在主对话中完成、不需要隔离上下文
- 使用 **子代理**：任务需要独立上下文、大量中间输出、需要限制工具权限、需要专业角色处理

## 3、Skill vs 内置 Slash 命令

Claude Code 内置了一批 Skill 级别的 Slash 命令，它们本质上是官方预装的 Skill：

| 命令 | 功能定位 | 本质 |
|------|----------|------|
| `/batch` | 大规模并行改造 | Skill（拆分任务到多个 worktree） |
| `/claude-api` | Claude API 开发辅助 | Skill（SDK 开发工作流） |
| `/debug` | 调试日志 | Skill（诊断工作流） |
| `/loop` | 循环运行 Prompt | Skill（定时任务工作流） |
| `/simplify` | 代码质量检查 | Skill（代码审查工作流） |
| `/fewer-permission-prompts` | 自动生成权限规则 | Skill（配置优化工作流） |

这些命令与普通 Skill 的区别仅在于它们是 Claude Code 官方内置的，无需额外安装即可使用。

# 四、Skill 的典型应用场景

## 1、知识库笔记生成

以 `generate_note` Skill 为例，它展示了 Skill 如何整合 wiki 知识并输出结构化笔记：

**触发条件**：用户说"生成笔记"、"写笔记"、"整理成笔记"等。

**执行流程**：
1. 解析用户需求（主题、目标目录、文件名）
2. 检索 wiki 知识库（读取 index、定位相关页面、深度阅读）
3. 学习写作风格（读取风格参考文件）
4. 整合生成笔记（按编号标题体系组织内容）
5. 写入文件并报告

**边界约束**：
- 不修改 wiki/ 目录下的任何文件
- 不修改 Claude Code/ 目录下的任何文件
- 若 wiki 中无相关知识，如实告知用户

## 2、跨平台技能框架

**Superpowers** 是一个典型的 Skill 框架案例。它由 Jesse Vincent 开发，是一套跨平台的 AI 编程智能体技能框架，强调测试驱动开发（TDD）和系统性流程。

**核心理念**：
- 测试驱动开发：始终先写测试，红-绿-重构循环
- 系统性优于临时性：流程胜过猜测
- 降低复杂度：将简洁性作为首要目标
- 证据胜于断言：在宣称成功之前先验证

**标准化工作流程**（7 个阶段）：

| 阶段 | 名称 | 说明 |
|------|------|------|
| 1 | 头脑风暴 | 在编码前通过提问完善想法 |
| 2 | Git 工作树 | 在新建分支上创建隔离工作空间 |
| 3 | 编写计划 | 将工作分解为小块任务（2-5 分钟/个） |
| 4 | 子代理驱动开发 | 为每个任务派遣子代理 |
| 5 | 测试驱动开发 | 红-绿-重构循环 |
| 6 | 请求代码审查 | 对照计划审查，严重问题阻止进度 |
| 7 | 完成开发分支 | 验证测试，提供合并/保留/丢弃选项 |

**跨平台支持**：

| 平台 | 安装方式 |
|------|----------|
| Claude Code | `/plugin install superpowers@claude-plugins-official` |
| Cursor | `/add-plugin superpowers` |
| GitHub Copilot CLI | `copilot plugin install superpowers@superpowers-marketplace` |
| OpenAI Codex CLI | 插件搜索安装 |
| Gemini CLI | `gemini extensions install https://github.com/obra/superpowers` |

## 3、自定义 Skill 的创建

创建自定义 Skill 的步骤：

1. 在 `.claude/skills/` 或 `~/.claude/skills/` 下创建目录
2. 在该目录中创建 `SKILL.md` 文件
3. 编写 YAML frontmatter（name、description）
4. 用 Markdown 编写 Skill 的执行流程和约束
5. 在对话中通过 `/reload-plugins` 或重启 Claude Code 加载

**编写建议**：
- `description` 要精确描述触发时机，这是 Skill 能否被正确调用的关键
- 执行流程要步骤清晰，像操作手册一样可执行
- 边界约束要明确列出 Skill 不会做的事情
- 语言使用简体中文（如果面向中文用户）

# 五、Skill 与记忆系统的协作

Skill 与 Claude Code 的记忆系统（`CLAUDE.md` 和 `auto memory`）存在互补关系：

| 机制 | 定位 | 与 Skill 的关系 |
|------|------|----------------|
| `CLAUDE.md` | 项目级持久指令 | 可包含"使用某 Skill 的默认参数"等约定 |
| `auto memory` | 自动积累的经验 | 可记录 Skill 的使用效果和偏好 |
| Skill | 可复用的工作流 | 可被 `CLAUDE.md` 引用，也可独立触发 |

> 如果某条内容属于多步骤流程，或只适用于代码库中的某个特定区域，更适合放到 Skill 或路径限定规则中，而不是堆积在 `CLAUDE.md` 中。

# 六、注意事项与最佳实践

## 1、Skill 的边界意识

Skill 应明确声明自己的边界：
- 哪些目录只读不修改
- 什么情况下需要询问用户
- 与哪些其他机制存在互斥或依赖关系

## 2、避免 Skill 冲突

如果多个 Skill 的 `description` 描述过于相似，可能导致触发冲突。建议：
- 让 `description` 尽可能具体和差异化
- 在 Skill 正文中声明与其他 Skill 的优先级关系

## 3、Skill 与子代理的协同

复杂的 Skill 可以在执行流程中调用子代理：
- Skill 负责整体流程编排
- 子代理负责具体任务的隔离执行
- 例如：Superpowers 的"子代理驱动开发"阶段

## 4、测试 Skill

创建 Skill 后，建议通过以下方式验证：
- 用明确的触发语句测试是否正常加载
- 检查 Skill 是否按预期流程执行
- 验证边界约束是否生效（如是否误改了受保护目录）

---

## 关联笔记

- [[Claude_Code]] — Claude Code 工具专题页（Skill 的运行环境）
- [[Subagent]] — 子代理概念页（与 Skill 互补的扩展机制）
- [[Superpowers]] — 跨平台 Skill 框架专题页
- [[Memory_System]] — 记忆系统（与 Skill 协作的持久化机制）
- [[摘要-slash-commands]] — Slash 命令详解（内置 Skill 命令速查）
- [[摘要-superpowers]] — Superpowers 框架素材摘要
- [[摘要-subagent]] — Subagent 素材摘要
