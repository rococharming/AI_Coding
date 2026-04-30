---
title: "Agent Skills"
type: concept
tags: [Agent-Architecture, Skills, 开放标准, AI-Coding]
tools: [Claude Code]
sources: [raw/01-articles/Extend Claude with skills.md]
last_updated: 2026-04-30
---

# Agent Skills

Agent Skills 是一种让 AI 代理（Agent）通过声明式指令文件扩展自身能力的开放标准。其核心思想是：**将可复用的知识、流程和工具封装为 Skill，使代理能够按需加载和调用**。

## 核心定义

Skill 是一个包含指令的文本文件（通常为 `SKILL.md`），通过 YAML frontmatter 描述元数据，通过 Markdown 正文描述行为。代理根据 frontmatter 中的 `description` 和 `when_to_use` 判断是否激活该 Skill，加载后将 Skill 内容作为上下文注入对话。

## 开放标准

Agent Skills 规范由 [agentskills.io](https://agentskills.io/) 维护，旨在实现跨工具的 Skill 互操作性。遵循该标准的 Skill 可在多个支持 Agent Skills 的 AI 工具间复用。

### Claude Code 的扩展

Claude Code 在开放标准基础上增加了以下扩展能力：

| 扩展功能 | 说明 |
|----------|------|
| **调用控制** | `disable-model-invocation` / `user-invocable` 控制谁可以触发 Skill |
| **子代理执行** | `context: fork` + `agent` 字段让 Skill 在隔离上下文中由专用代理执行 |
| **动态上下文注入** | `` !`command` `` 语法在 Skill 加载前执行 shell 命令并注入输出 |
| **工具预授权** | `allowed-tools` 在 Skill 激活期间免除特定工具的权限确认 |
| **路径限定** | `paths` 字段限制 Skill 仅在匹配文件被编辑时自动激活 |
| **模型覆盖** | `model` / `effort` 字段在 Skill 激活期间临时切换模型配置 |

## Skill 与相关概念的区分

| 概念 | 加载时机 | 作用范围 | 典型内容 |
|------|----------|----------|----------|
| **CLAUDE.md** | 会话开始时始终加载 | 项目级 | 项目背景、编码规范、架构决策 |
| **Skill** | 调用时按需加载 | 四级作用域 | 操作流程、检查清单、领域知识 |
| **Memory** | 持久化存储，按需检索 | 用户/项目级 | 用户偏好、项目历史、跨会话事实 |
| **Subagent** | 任务委派时创建 | 单次任务 | 隔离执行环境，可预加载 Skills |

## 设计原则

1. **按需加载**：Skill 内容仅在调用时进入上下文，长参考材料几乎无日常成本
2. **显式控制**：通过 frontmatter 明确声明 Skill 的调用方式、工具权限和执行环境
3. **可组合性**：Skill 可调用其他 Skill，可与 Subagent 结合形成复杂工作流
4. **跨工具复用**：遵循开放标准的 Skill 可在不同 AI 工具间迁移

## 关联链接
- [[Claude_Code]] — Claude Code 的 Skills 实现
- [[claude-code-skill-creation]] — Skill 创建与配置的实操指南
- [[Subagent]] — 子代理与 Skill 的协作模式
- [[Memory_System]] — 记忆系统与 Skill 的互补关系
- [[摘要-extend-claude-with-skills]] — 原始素材摘要
