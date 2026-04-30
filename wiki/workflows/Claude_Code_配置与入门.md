---
title: "Claude Code 配置与入门"
type: workflow
tags: [Setup, Configuration, Quickstart]
tools: [Claude Code]
sources: [raw/01-articles/claude-code-intro.md]
last_updated: 2026-04-30
---

# Claude Code 配置与入门

## 目标
在 macOS 上完成 Claude Code 的安装、第三方模型配置，并成功启动第一个会话。

## 前置条件
- macOS 系统
- 国内第三方模型账号（Kimi Code 或 MiniMax）及 API Key

## 步骤

### 1. 安装 Claude Code

```bash
curl -fsSL https://claude.ai/install.sh | bash
claude --version
```

### 2. 获取 API Key

**方案 A：Kimi Code**
1. 访问 https://www.kimi.com/code 购买会员订阅
2. 进入 https://www.kimi.com/code/console 创建 API Key
3. 复制以 `sk-kimi-` 开头的密钥

**方案 B：MiniMax**
1. 访问 https://platform.minimaxi.com/ 注册并购买 Token Plan
2. 复制对应的 API Key

### 3. 配置 settings.json

编辑 `~/.claude/settings.json`：

**Kimi 配置示例**:
```json
{
  "env": {
    "ANTHROPIC_API_KEY": "sk-kimi-your-key",
    "ANTHROPIC_BASE_URL": "https://api.kimi.com/coding/",
    "ANTHROPIC_MODEL": "kimi-for-coding",
    "ANTHROPIC_DEFAULT_SONNET_MODEL": "kimi-for-coding",
    "ANTHROPIC_DEFAULT_OPUS_MODEL": "kimi-for-coding",
    "ANTHROPIC_DEFAULT_HAIKU_MODEL": "kimi-for-coding",
    "ANTHROPIC_REASONING_MODEL": "kimi-for-coding",
    "API_TIMEOUT_MS": "3000000",
    "CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC": "1"
  },
  "permissions": {
    "defaultMode": "default"
  }
}
```

**MiniMax 配置示例**:
```json
{
  "env": {
    "ANTHROPIC_AUTH_TOKEN": "your-minimax-key",
    "ANTHROPIC_BASE_URL": "https://api.minimaxi.com/anthropic",
    "ANTHROPIC_MODEL": "MiniMax-M2.7",
    "ANTHROPIC_DEFAULT_SONNET_MODEL": "MiniMax-M2.7",
    "ANTHROPIC_DEFAULT_OPUS_MODEL": "MiniMax-M2.7",
    "ANTHROPIC_DEFAULT_HAIKU_MODEL": "MiniMax-M2.7",
    "API_TIMEOUT_MS": "3000000",
    "CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC": "1"
  }
}
```

> 注意：Kimi 使用 `ANTHROPIC_API_KEY`，MiniMax 使用 `ANTHROPIC_AUTH_TOKEN`（会被自动加上 `Bearer` 前缀）。

### 4. 启动并验证

```bash
cd path/to/your-project
claude
```

进入会话后，输入：
```
你使用的是什么模型？
```

确认回复中显示的是第三方模型（如 `kimi-for-coding`）。

### 5. 诊断环境

```
/doctor
```

检查安装、配置和运行环境是否存在问题。

### 6. 选择权限模式

启动后默认是 `default`（保守）模式。根据任务类型选择：

| 场景 | 推荐模式 |
|------|----------|
| 首次使用 / 敏感项目 | `default` |
| 快速迭代开发 | `acceptEdits` |
| 大型改造前的方案设计 | `plan` |

切换方式：`Shift + Tab` 循环切换，或在 `settings.json` 中设置 `permissions.defaultMode`。

## 验证清单

- [ ] `claude --version` 返回版本号
- [ ] 配置文件路径正确（`~/.claude/settings.json`）
- [ ] API Key 已填入且未泄露给他人
- [ ] 启动后模型回复显示第三方模型名称
- [ ] `/doctor` 无严重错误
- [ ] 了解如何切换权限模式

## 常见问题

**Q: 配置后仍请求官方登录？**
A: 检查 `ANTHROPIC_BASE_URL` 是否正确，以及 `ANTHROPIC_API_KEY`/`ANTHROPIC_AUTH_TOKEN` 是否填写正确。

**Q: 模型名显示为 Claude 官方模型？**
A: 这是正常的映射显示。实际请求已通过 `ANTHROPIC_BASE_URL` 转发到第三方网关。

**Q: 如何禁用自动更新？**
A: 在 `env` 中设置 `"CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC": "1"`。

## 关联链接
- [[Claude_Code]] — Claude Code 工具专题页
- [[摘要-claude-code-intro]] — 原始素材摘要
