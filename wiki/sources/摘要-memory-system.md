---
title: "摘要-memory-system"
type: source
tags: [Claude-Code, Memory, Context]
tools: [Claude Code]
sources: [raw/01-articles/memory-system.md]
last_updated: 2026-04-30
---

# 摘要：记忆机制

## 素材来源
- **原始文件**: `raw/01-articles/memory-system.md`
- **主题**: Claude Code 的记忆系统（CLAUDE.md 与 Auto Memory）

## 核心主旨
本文深入解析 Claude Code 的两种记忆机制：手动维护的 `CLAUDE.md`（项目上下文）和自动生成的 `Auto Memory`（学习偏好），以及它们的存放位置、加载规则、编写规范和团队管理策略。

## 关键知识点

1. **CLAUDE.md**: 用户手动编写的跨会话持久指令文件
   - 存放层级: 托管策略（组织级）> 项目指令（`./CLAUDE.md`）> 用户指令（`~/.claude/CLAUDE.md`）> 本地指令（`CLAUDE.local.md`）
   - 加载规则: 从当前目录向上查找，所有发现的文件拼接而非覆盖
   - 编写规范: 控制在 200 行以内，使用清晰结构，具体可验证，避免规则冲突
   - 支持路径导入（`@path`）和 `.claude/rules/` 路径限定规则

2. **Auto Memory**: Claude Code 自动生成的跨会话学习记忆
   - 默认开启，存储在 `~/.claude/projects/<project>/memory/`
   - 只加载 MEMORY.md 前 200 行或 25KB
   - 可随时手动审计和编辑

3. **AGENTS.md 兼容**: 可通过 `CLAUDE.md` 导入 `AGENTS.md` 实现多工具共享

## 关联链接
- [[Memory_System]] — 记忆系统概念页
- [[Claude_Code]] — Claude Code 工具专题页
