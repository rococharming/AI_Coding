---
title: "摘要-claude-code-intro"
type: source
tags: [Claude-Code, 入门]
tools: [Claude Code]
sources: [raw/01-articles/claude-code-intro.md]
last_updated: 2026-04-30
---

# 摘要：Claude Code 入门

## 素材来源
- **原始文件**: `raw/01-articles/claude-code-intro.md`
- **主题**: Claude Code 的安装、配置与基础使用

## 核心主旨
本文是 Claude Code 的入门级指南，涵盖从安装到实战的完整路径，重点介绍如何通过配置接入国内第三方模型（MiniMax、Kimi），以及权限模式的选择与切换。

## 关键知识点

1. **安装方式**: 通过官方 install.sh 脚本安装，支持 `claude update` 手动更新
2. **第三方模型接入**: 通过 `~/.claude/settings.json` 配置 `ANTHROPIC_BASE_URL` 和 `ANTHROPIC_API_KEY/ANTHROPIC_AUTH_TOKEN` 实现网关转发
3. **核心命令**: `/usage`（用量查看）、`/doctor`（诊断）、`/status`（状态）、`/clear`（清空上下文）、`/model`（切换模型）、`/resume`（恢复会话）、`/compact`（压缩上下文）
4. **权限模式**: `default`（保守）、`acceptEdits`（自动编辑）、`plan`（规划模式）、`bypassPermissions`（Yolo 模式，高危）
5. **受保护路径**: `.git`、`.vscode`、`.idea`、`.husky`、`.claude`（除子目录外）、各种 shell 配置文件

## 关联链接
- [[Claude_Code]] — Claude Code 工具专题页
- [[Claude_Code_配置与入门]] — 配置工作流
