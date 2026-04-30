---
title: "摘要-subagent"
type: source
tags: [Claude-Code, Subagent, Agent]
tools: [Claude Code]
sources: [raw/01-articles/subagent.md]
last_updated: 2026-04-30
---

# 摘要：Subagent

## 素材来源
- **原始文件**: `raw/01-articles/subagent.md`
- **主题**: Claude Code 的子代理机制

## 核心主旨
本文全面介绍 Claude Code 的 Subagent 系统，包括内置子代理类型、自定义子代理的创建与配置、工具权限控制、以及常见的使用模式（隔离高输出、并行研究、串联工作流）。

## 关键知识点

1. **内置 Subagents**:
   - `Explore`: 只读代码库探索（Haiku 模型）
   - `Plan`: 规划模式研究（只读）
   - `General-purpose`: 通用复杂任务（所有工具）
   - `statusline-setup`, `Claude Code Guide`: 辅助 agents

2. **子代理作用域优先级**: 托管设置 > CLI 标志 > `.claude/agents/` > `~/.claude/agents` > 插件

3. **子代理文件格式**: YAML frontmatter + Markdown system prompt
   - 关键字段: `name`, `description`, `tools`, `disallowedTools`, `model`, `permissionMode`, `maxTurns`, `skills`, `mcpServers`, `hooks`, `memory`, `background`, `effort`, `isolation`, `color`, `initialPrompt`

4. **使用模式**:
   - 隔离高输出量操作（测试、日志分析）
   - 并行研究（多模块同时探索）
   - 串联子代理（分析 → 修改流水线）

## 关联链接
- [[Subagent]] — 子代理概念页
- [[Claude_Code]] — Claude Code 工具专题页
