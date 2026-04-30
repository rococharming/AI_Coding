---
title: "摘要-slash-commands"
type: source
tags: [Claude-Code, Slash-Command]
tools: [Claude Code]
sources: [raw/01-articles/slash-commands.md]
last_updated: 2026-04-30
---

# 摘要：Slash 命令详解

## 素材来源
- **原始文件**: `raw/01-articles/slash-commands.md`
- **主题**: Claude Code 中所有 Slash 命令的分类与速查

## 核心主旨
本文系统梳理了 Claude Code 的 Slash 命令体系，将其分为内建命令、Skill 命令、插件命令和 MCP Prompts 四类，并提供详细的功能速查表。

## 关键知识点

1. **命令分类**:
   - 内建命令: `/clear`, `/model`, `/compact`, `/usage`, `/doctor`, `/status`, `/resume`
   - 内置 Skill: `/batch`, `/debug`, `/loop`, `/simplify`, `/claude-api`
   - 插件命令: 命名空间调用如 `my-plugin:hello`
   - MCP Prompts: `/mcp__<server>__<prompt>`

2. **常用内建命令**:
   - 会话与上下文: `/clear`, `/compact`, `/context`, `/resume`, `/branch`, `/btw`, `/recap`, `/rename`, `/rewind`, `/exit`
   - 模型与用量: `/model`, `/effort`, `/usage`, `/cost`, `/stats`, `/fast`
   - 文件与工程: `/init`, `/add-dir`, `/diff`, `/review`, `/security-review`, `/plan`
   - 配置与集成: `/config`, `/permissions`, `/mcp`, `/memory`, `/agents`, `/hooks`, `/plugin`, `/reload-plugins`, `/ide`, `/statusline`, `/keybindings`, `/theme`, `/color`, `/tui`, `/terminal-setup`, `/sandbox`
   - 诊断与辅助: `/login`, `/logout`, `/status`, `/doctor`, `/help`, `/feedback`, `/release-notes`, `/export`, `/copy`, `/mobile`, `/tasks`, `/insights`, `/powerup`, `/sticks`
   - 团队协作: `/team-onboarding`

3. **内置 Skill 命令**:
   - `/batch`: 大规模并行改造
   - `/claude-api`: Claude API 开发辅助
   - `/debug`: 调试日志
   - `/loop`: 循环运行 Prompt
   - `/simplify`: 代码质量检查
   - `/fewer-permission-prompts`: 自动生成权限允许规则

## 关联链接
- [[Claude_Code]] — Claude Code 工具专题页
