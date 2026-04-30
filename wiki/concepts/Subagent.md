---
title: "Subagent"
type: concept
tags: [Agent-Architecture, Parallelism, Delegation]
tools: [Claude Code]
sources: [raw/01-articles/subagent.md]
last_updated: 2026-04-30
---

# Subagent

**子代理（Subagent）** 是专门处理特定任务的 AI 助手，拥有独立的上下文窗口、自定义系统提示词和特定的工具权限。当主代理判断任务符合某个子代理的描述时，会自动将任务委托给它。

## 核心优势

1. **上下文保护**: 将探索和实现过程隔离到独立上下文，避免污染主对话
2. **权限隔离**: 通过限制可用工具强制执行约束（如只读审查器）
3. **专业化**: 每个子代理针对特定领域深度定制
4. **成本控制**: 简单任务可路由到更快、更便宜的模型
5. **跨项目复用**: 用户级子代理可在多个项目中共享

## 常见使用模式

### 1. 隔离高输出量操作
将产生大量中间内容的任务委托给子代理，主对话只接收摘要：
- 运行测试套件
- 分析日志文件
- 扫描大型代码库
- 获取大量文档

### 2. 并行研究
多个调查任务彼此独立时，同时启动多个子代理并行处理：
```
使用不同的子代理并行研究认证模块、数据库模块和API模块
```

### 3. 串联工作流
多步骤任务按顺序调用多个子代理，形成流水线：
```
先使用 code-reviewer 查找性能问题，然后使用 optimizer 修复
```

## 子代理配置要素

子代理文件使用 **YAML frontmatter + Markdown system prompt** 格式：

```yaml
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

**关键配置字段**:

| 字段 | 说明 |
|------|------|
| `name` | 唯一标识符（小写字母和连字符） |
| `description` | 触发条件描述（"在什么情况下委托给该子代理"） |
| `tools` / `disallowedTools` | 白名单/黑名单工具控制 |
| `model` | 使用的模型（`sonnet`/`opus`/`haiku`/`inherit`） |
| `permissionMode` | 权限模式（可覆盖主会话） |
| `mcpServers` | 可用的 MCP 服务器（可内联定义或引用） |
| `skills` | 预加载的技能（完整内容注入上下文） |
| `memory` | 持久记忆作用域（`user`/`project`/`local`） |
| `isolation` | 设置为 `worktree` 时在隔离 git worktree 中运行 |
| `background` | 设置为 `true` 时作为后台任务运行 |

## 作用域与优先级

当多个位置定义了同名子代理时，按优先级生效：

| 优先级 | 位置 | 范围 |
|--------|------|------|
| 1 | 托管设置 | 组织范围 |
| 2 | `--agents` CLI 标志 | 当前会话 |
| 3 | `.claude/agents/` | 当前项目 |
| 4 | `~/.claude/agents` | 个人所有项目 |
| 5 | 插件 | 启用该插件的位置 |

## 与主对话的选择策略

**留在主对话**: 需要频繁沟通、调整方向、上下文连续的小任务
**使用子代理**: 独立任务、大量中间输出、需要限制工具权限、专业角色处理

## 关联链接
- [[Claude_Code]] — Claude Code 工具页（内置 Subagent 机制）
- [[Superpowers]] — Superpowers 框架（大量使用子代理驱动开发）
- [[摘要-subagent]] — 原始素材摘要
