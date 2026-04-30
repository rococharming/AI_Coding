---
title: "Claude Code Skill 创建与配置"
type: workflow
tags: [Claude-Code, Skills, 配置指南, workflow]
tools: [Claude Code]
sources: [raw/01-articles/Extend Claude with skills.md]
last_updated: 2026-04-30
---

# Claude Code Skill 创建与配置

## 何时创建 Skill

- 反复粘贴相同的操作手册、检查清单或多步骤流程
- CLAUDE.md 中某部分内容已演变为"流程"而非"事实"
- 需要封装副作用操作（如部署、发送消息），严格控制触发时机

## 创建步骤

### 1. 确定存储位置

| 级别 | 路径 | 适用范围 |
|------|------|----------|
| Enterprise | 由 managed settings 配置 | 组织内所有用户 |
| Personal | `~/.claude/skills/<skill-name>/SKILL.md` | 当前用户的所有项目 |
| Project | `.claude/skills/<skill-name>/SKILL.md` | 仅当前项目 |
| Plugin | `<plugin>/skills/<skill-name>/SKILL.md` | 插件启用处 |

同名 Skill 的覆盖规则：Enterprise > Personal > Project。Plugin 使用 `plugin-name:skill-name` 命名空间，不与其他级别冲突。

### 2. 编写 SKILL.md

每个 Skill 是一个目录，`SKILL.md` 为入口文件（必需），可附带支持文件：

```text
my-skill/
├── SKILL.md           # 主指令（必需）
├── template.md        # 供 Claude 填写的模板（可选）
├── examples/
│   └── sample.md      # 预期输出格式示例（可选）
└── scripts/
    └── validate.sh    # Claude 可执行的脚本（可选）
```

> 建议 SKILL.md 保持在 500 行以内，详细参考材料放入独立文件。

### 3. 配置 Frontmatter

在 `SKILL.md` 顶部通过 YAML frontmatter 控制 Skill 行为：

```yaml
---
name: my-skill              # 显示名称（默认使用目录名）
description: What this skill does and when to use it  # 推荐填写，Claude 用它判断是否调用
when_to_use: 额外触发场景说明  # 追加到 description，共享 1536 字符上限
argument-hint: "[issue-number]"  # 自动补全提示
disable-model-invocation: true   # 仅用户可调用（用于有副作用的操作）
user-invocable: false            # 仅 Claude 可自动调用（用于背景知识）
allowed-tools: Read Grep Bash(git *)  # Skill 激活期间免确认的工具
context: fork                    # 在子代理中执行
agent: Explore                   # 子代理类型（Explore/Plan/general-purpose）
paths: "src/**/*.ts"             # 仅匹配文件时自动激活
---
```

**调用控制矩阵**：

| Frontmatter | 用户可 /name | Claude 可自动调用 | 加载方式 |
|-------------|-------------|-------------------|----------|
| （默认） | Yes | Yes | Description 常驻上下文，完整内容调用时加载 |
| `disable-model-invocation: true` | Yes | No | Description 不加载，用户调用时加载完整内容 |
| `user-invocable: false` | No | Yes | Description 常驻上下文，Claude 自动触发 |

### 4. 编写 Skill 内容

**Reference 类型**（内联知识，Claude 可自动应用）：

```markdown
---
name: api-conventions
description: API design patterns for this codebase
---

When writing API endpoints:
- Use RESTful naming conventions
- Return consistent error formats
- Include request validation
```

**Task 类型**（分步骤操作，通常手动触发）：

```markdown
---
name: deploy
description: Deploy the application to production
disable-model-invocation: true
---

Deploy the application:
1. Run the test suite
2. Build the application
3. Push to the deployment target
```

### 5. 参数传递

Skill 支持多种占位符替换：

| 占位符 | 说明 |
|--------|------|
| `$ARGUMENTS` | 调用时传入的全部参数 |
| `$ARGUMENTS[N]` / `$N` | 按 0-based 索引取参数，如 `$0`, `$1` |
| `$name` | frontmatter `arguments: [name1, name2]` 声明的命名参数 |
| `${CLAUDE_SESSION_ID}` | 当前会话 ID |
| `${CLAUDE_EFFORT}` | 当前 effort 级别 |
| `${CLAUDE_SKILL_DIR}` | Skill 目录路径 |

示例（迁移组件）：

```yaml
---
name: migrate-component
description: Migrate a component from one framework to another
---

Migrate the $0 component from $1 to $2.
Preserve all existing behavior and tests.
```

调用：`/migrate-component SearchBar React Vue`

### 6. 动态上下文注入

使用 `` !`command` `` 语法在 Skill 发送给 Claude **之前**执行命令，将输出替换到内容中：

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

### 7. 在子代理中执行

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

**Skill + Subagent 的两种协作模式**：

| 方式 | System Prompt | 任务来源 | 额外加载 |
|------|--------------|----------|----------|
| Skill 带 `context: fork` | 由 `agent` 字段决定 | SKILL.md 内容 | CLAUDE.md |
| Subagent 带 `skills` 字段 | Subagent 的 markdown 正文 | Claude 的委派消息 | 预加载 Skills + CLAUDE.md |

## 验证与调试

1. **检查 Skill 是否加载**：查看 `What skills are available?` 提示
2. **直接调用测试**：`/skill-name` 手动触发
3. **描述匹配**：确保 `description` 包含用户可能使用的自然语言关键词
4. **触发过于频繁**：添加 `disable-model-invocation: true` 或使描述更具体
5. **配置诊断**：参考官方 [Debug your configuration](https://code.claude.com/docs/en/debug-your-config) 文档

## 关联链接
- [[Claude_Code]] — Claude Code 工具总览
- [[Agent_Skills]] — Agent Skills 开放标准
- [[Subagent]] — 子代理架构与配置
- [[摘要-extend-claude-with-skills]] — 本文档的原始素材摘要
