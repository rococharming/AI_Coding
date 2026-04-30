---
title: "摘要：Extend Claude with skills"
type: source
tags: [clippings, Claude-Code, Skills]
tools: [Claude Code]
sources: [raw/01-articles/Extend Claude with skills.md]
last_updated: 2026-04-30
---

# 摘要：Extend Claude with skills

> 原始素材：[raw/01-articles/Extend Claude with skills.md](raw/01-articles/Extend%20Claude%20with%20skills.md)
> 来源：Claude Code 官方文档 — https://code.claude.com/docs/en/skills

## 核心主旨

Claude Code Skills 系统允许用户通过编写 `SKILL.md` 文件来扩展 Claude 的能力。Skills 遵循 [Agent Skills](https://agentskills.io/) 开放标准，支持四级作用域（Enterprise/Personal/Project/Plugin）、动态上下文注入、子代理执行和精细的调用控制。

## 关键知识点

1. **Skills 本质**：通过 `SKILL.md` 文件定义指令集，Claude 按需加载（不同于始终加载的 CLAUDE.md），长参考材料几乎无上下文成本。
2. **四级存储**：Enterprise（组织级）→ Personal（用户级）→ Project（项目级）→ Plugin（插件级），同名时前者覆盖后者。
3. **两种内容类型**：Reference content（内联知识，如编码规范）和 Task content（分步骤操作，如部署流程）。
4. **调用控制 frontmatter**：
   - `disable-model-invocation: true`：仅用户可调用（防止 Claude 自动触发副作用操作）
   - `user-invocable: false`：仅 Claude 可自动调用（背景知识类）
5. **动态上下文注入**：使用 `` !`command` `` 语法在 Skill 加载前执行 shell 命令，将输出注入到 prompt 中（如实时获取 PR diff）。
6. **子代理执行**：`context: fork` + `agent: Explore/Plan` 让 Skill 在隔离上下文中由专用代理执行。
7. **参数传递**：支持 `$ARGUMENTS`、`$N`、命名参数 `$name` 等占位符替换。
8. **工具预授权**：`allowed-tools` 字段可在 Skill 激活期间免除特定工具的权限确认。
9. **生命周期**：Skill 一旦被调用，其内容作为单条消息进入会话并持续存在；自动压缩时会保留最近调用的 Skill（每 Skill 前 5000 tokens，总预算 25000 tokens）。
10. **捆绑技能**：Claude Code 内置 `/simplify`, `/batch`, `/debug`, `/loop`, `/claude-api` 等基于 prompt 的 Skill。

## 关联链接
- [[Claude_Code]] — Claude Code 工具总览与 Skills 体系说明
- [[claude-code-skill-creation]] — Skill 创建与配置的详细操作指南
- [[Agent_Skills]] — Agent Skills 开放标准跨工具概念
- [[Subagent]] — Skill 中 context: fork 与子代理的配合
