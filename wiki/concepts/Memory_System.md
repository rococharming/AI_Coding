---
title: "Memory System"
type: concept
tags: [Context-Management, Persistence, Agent]
tools: [Claude Code]
sources: [raw/01-articles/memory-system.md]
last_updated: 2026-04-30
---

# Memory System

在 AI Coding 工具中，**记忆系统（Memory System）** 是跨会话保留信息的机制。由于每次对话都从全新上下文窗口开始，记忆系统成为持续协作的基础设施。

## 两种记忆模式

### 1. 手动记忆（Manual Memory）

由用户主动编写和维护的持久上下文文件，典型代表是 Claude Code 的 **CLAUDE.md**。

**特点**:
- **事先约定**: 强调"在开始前定义规则"
- **长期稳定**: 存放构建命令、代码风格、架构决策等不变信息
- **层级管理**: 支持组织级、项目级、用户级、本地级多层配置

**CLAUDE.md 存放层级**:

| 层级 | 位置 | 范围 |
|------|------|------|
| 托管策略 | `/Library/Application Support/ClaudeCode/CLAUDE.md` (macOS) | 组织内所有用户 |
| 项目指令 | `./CLAUDE.md` 或 `./.claude/CLAUDE.md` | 当前项目团队 |
| 用户指令 | `~/.claude/CLAUDE.md` | 个人所有项目 |
| 本地指令 | `./CLAUDE.local.md` | 仅当前项目且不上传 Git |

**加载规则**:
- 从当前工作目录**向上查找**，所有发现的文件**拼接**而非覆盖
- 子目录的 `CLAUDE.md` **不在启动时加载**，仅在读取该子目录文件时加载
- `CLAUDE.local.md` 追加在同层 `CLAUDE.md` 之后

**编写规范**:
- 控制在 **200 行以内**
- 使用 Markdown 标题和列表分组
- 指令要**具体、可验证**（如"使用 2 个空格缩进"而非"格式化好代码"）
- 定期检查冲突和过期内容

### 2. 自动记忆（Auto Memory）

由 AI 工具在交互过程中**自动生成**的记忆，记录学习到的偏好、经验和模式。

**特点**:
- **在使用中学习**: 强调"在协作中沉淀知识"
- **选择性记录**: 只保存对未来对话可能有帮助的内容
- **主题拆分**: 自动将记忆组织到不同主题文件中

**存储结构**:
```
~/.claude/projects/<project>/memory/
├── MEMORY.md        # 索引文件（前 200 行/25KB 自动加载）
├── debugging.md     # 调试经验
├── api-conventions.md
└── ...
```

**加载策略**:
- 只加载 `MEMORY.md` 的前 200 行或 25KB（取较小者）
- 主题文件（如 `debugging.md`）**按需读取**，不在启动时加载

## 记忆系统的通用设计原则

1. **上下文 vs 配置**: 记忆本质上是"上下文"而非"强制配置"，效果取决于内容清晰度
2. **分层隔离**: 组织/项目/个人/本地四级隔离，避免个人偏好污染团队规范
3. **路径限定**: 复杂项目应使用路径限定规则（如 `.claude/rules/*.md`），让特定规则只在处理匹配文件时加载
4. **审计友好**: 记忆文件是标准 Markdown，可随时查看、编辑、删除

## 不同工具的实现对比

| 特性 | Claude Code | Cursor | GitHub Copilot |
|------|-------------|--------|----------------|
| 手动记忆 | `CLAUDE.md` | `.cursorrules` | 通过 VS Code 设置 |
| 自动记忆 | `Auto Memory` | 无（需手动维护） | 无 |
| 路径限定规则 | `.claude/rules/*.md` | 无 | 无 |
| 层级加载 | 向上查找 + 拼接 | 单文件 | 编辑器配置 |

## 关联链接
- [[Claude_Code]] — Claude Code 工具页
- [[摘要-memory-system]] — 原始素材摘要
