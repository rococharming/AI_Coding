---
title: "Claude Code"
type: tool
tags: [AI-Coding, CLI, Anthropic, IDE]
sources: [raw/01-articles/claude-code-intro.md, raw/01-articles/slash-commands.md]
last_updated: 2026-04-30
---

# Claude Code

Claude Code 是 Anthropic 推出的 AI 编码助手，能在终端或 IDE 中理解代码库、编辑文件、执行命令，帮助开发者用**自然语言**完成代码阅读、开发、调试、重构、测试等任务。

## 核心功能

- **代码理解**: 分析项目结构、读取文件、搜索代码
- **代码编辑**: 自动创建、修改、删除文件
- **命令执行**: 运行 shell 命令、测试、构建
- **多模态**: 支持图片输入（拖拽到对话框）
- **上下文管理**: 会话恢复、上下文压缩、分支管理

## 安装与更新

```bash
# 安装（macOS）
curl -fsSL https://claude.ai/install.sh | bash

# 验证安装
claude --version

# 手动更新
claude update
```

## 配置第三方模型

由于官方接口需要国外手机号且存在封号风险，推荐通过网关转发接入国内第三方模型。

**基本原理**: 配置 `ANTHROPIC_BASE_URL` + `ANTHROPIC_API_KEY/ANTHROPIC_AUTH_TOKEN` + 模型映射，将 Claude Code 的默认请求转发到第三方兼容接口。

在 `~/.claude/settings.json` 中配置：

```json
{
  "env": {
    "ANTHROPIC_BASE_URL": "https://api.kimi.com/coding/",
    "ANTHROPIC_API_KEY": "your-api-key",
    "ANTHROPIC_MODEL": "kimi-for-coding",
    "ANTHROPIC_DEFAULT_SONNET_MODEL": "kimi-for-coding",
    "ANTHROPIC_DEFAULT_OPUS_MODEL": "kimi-for-coding",
    "ANTHROPIC_DEFAULT_HAIKU_MODEL": "kimi-for-coding",
    "API_TIMEOUT_MS": "3000000",
    "CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC": "1"
  }
}
```

**关键环境变量说明**:
- `ANTHROPIC_BASE_URL`: API 网关地址
- `ANTHROPIC_API_KEY` / `ANTHROPIC_AUTH_TOKEN`: 认证密钥（不同厂商格式不同）
- `ANTHROPIC_MODEL`: 默认主模型
- `ANTHROPIC_DEFAULT_*_MODEL`: 将 Claude 模型档位映射到实际模型
- `CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC`: 关闭自动更新和遥测

## 权限模式

| 模式 | 说明 | 适用场景 |
|------|------|----------|
| `default` | 保守模式，危险操作前确认 | 新手、敏感项目、生产代码 |
| `acceptEdits` | 自动批准工作目录内文件编辑 | 迭代开发、信任当前任务 |
| `plan` | 只读探索，给出方案但不修改 | 大型改造前、代码评审 |
| `bypassPermissions` | 跳过大部分权限检查（Yolo 模式） | 明确安全的环境、快速脚本 |

**切换方式**:
- 会话中: `Shift + Tab` 循环切换
- 启动时: `claude --permission-mode acceptEdits`
- 默认设置: `settings.json` 中配置 `permissions.defaultMode`

**受保护路径**（任何模式下都不会自动写入）:
`.git`, `.vscode`, `.idea`, `.husky`, `.claude`（除 `commands/skills/agents/worktrees` 子目录外）、`.gitconfig`, `.bashrc`, `.zshrc` 等配置文件。

## 常用 Slash 命令

### 会话与上下文
| 命令 | 功能 |
|------|------|
| `/clear` | 清空上下文，开始新对话（别名: `/reset`, `/new`） |
| `/compact [说明]` | 压缩上下文，保留关键信息 |
| `/resume [会话]` | 恢复历史会话（别名: `/continue`） |
| `/exit` | 退出 CLI（别名: `/quit`） |

### 模型与诊断
| 命令 | 功能 |
|------|------|
| `/model [模型]` | 切换模型，支持调整推理强度 |
| `/usage` / `/cost` | 查看会话用量和成本 |
| `/doctor` | 检查安装和配置健康状态 |
| `/status` | 查看版本、模型、连接状态 |

### 工程操作
| 命令 | 功能 |
|------|------|
| `/init` | 为项目初始化 `CLAUDE.md` |
| `/diff` | 查看当前 git diff 和对话改动 |
| `/plan [描述]` | 进入规划模式 |
| `/review [PR]` | 审查 Pull Request |

### 配置与集成
| 命令 | 功能 |
|------|------|
| `/config` / `/settings` | 打开设置界面 |
| `/memory` | 管理持久记忆文件 |
| `/agents` | 管理子代理配置 |
| `/mcp` | 管理 MCP Server |
| `/plugin` | 管理插件 |

### 内置 Skill 命令
| 命令 | 功能 |
|------|------|
| `/batch <指令>` | 大规模并行改造，拆分任务到多个 worktree |
| `/claude-api` | Claude API / Anthropic SDK 开发辅助 |
| `/debug` | 开启调试日志排查问题 |
| `/loop [间隔] [prompt]` | 循环运行 Prompt（别名: `/proactive`） |
| `/simplify` | 检查代码复用、质量和效率问题 |

## 用量统计说明

`/usage` 输出字段解释：
- `input`: 普通输入 tokens（未命中缓存）
- `output`: 生成的输出 tokens（含 thinking tokens）
- `cache read`: 命中 prompt cache 的 tokens（更便宜）
- `cache write`: 写入 cache 的 tokens（供后续复用）

## 关联链接
- [[Memory_System]] — 记忆系统（CLAUDE.md 与 Auto Memory）
- [[Subagent]] — 子代理架构
- [[Superpowers]] — Superpowers 技能框架
- [[摘要-claude-code-intro]] — 入门素材来源
- [[摘要-slash-commands]] — 命令速查素材来源
