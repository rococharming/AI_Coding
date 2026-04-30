---
title: obra/superpowers：一个有效的智能体技能框架与软件开发方法论
source: https://github.com/obra/superpowers
author:
published:
created: 2026-04-30
description: 一个有效的智能体技能框架与软件开发方法论。 - obra/superpowers
tags:
  - clippings
---
## Superpowers

Superpowers 是一套完整的软件开发方法论，专为你的编程智能体设计。它基于一组可组合的技能和一些初始指令构建，确保你的智能体会使用这些技能。

## 工作原理

从你启动编程智能体的那一刻起，它就开始工作了。当它发现你正在构建某个东西时，它**不会**直接开始写代码。相反，它会退一步，问你真正想要做什么。

一旦它从对话中梳理出需求规格，它会以足够短的片段向你展示，让你能够真正阅读和理解。

在你确认设计之后，你的智能体会制定一个足够清晰的实施计划，让一位充满热情但品味不佳、缺乏判断力、没有项目背景且厌恶测试的初级工程师也能遵循。它强调真正的红/绿测试驱动开发（TDD）、YAGNI（你不会需要它）原则和 DRY（不要重复自己）原则。

接下来，一旦你说了"开始"，它就会启动一个**子代理驱动开发**流程，让智能体逐个完成工程任务，检查并审查它们的工作，然后继续前进。Claude 经常能够根据你制定的计划自主工作数小时而不会偏离轨道。

这套系统还有更多内容，但以上就是核心。而且由于这些技能会自动触发，你不需要做任何特殊操作。你的编程智能体就拥有了 Superpowers。

## 赞助

如果 Superpowers 帮助你做了一些赚钱的事情，并且你有这个意愿，我非常感谢你能考虑[赞助我的开源工作](https://github.com/sponsors/obra)。

谢谢！

- Jesse

## 安装

**注意：** 安装方式因平台而异。

### Claude Code 官方市场

Superpowers 可通过[官方 Claude 插件市场](https://claude.com/plugins/superpowers)获取。

从 Anthropic 官方市场安装插件：

```
/plugin install superpowers@claude-plugins-official
```

### Claude Code（Superpowers 市场）

Superpowers 市场为 Claude Code 提供 Superpowers 及其他相关插件。

在 Claude Code 中，先注册市场：

```
/plugin marketplace add obra/superpowers-marketplace
```

然后从此市场安装插件：

```
/plugin install superpowers@superpowers-marketplace
```

### OpenAI Codex CLI

- 打开插件搜索界面
```
/plugins
```

搜索 Superpowers

```
superpowers
```

选择 `Install Plugin`

### OpenAI Codex App

- 在 Codex 应用中，点击侧边栏中的 Plugins。
- 你应该会在 Coding 部分看到 `Superpowers`。
- 点击 `Superpowers` 旁边的 `+` 并按照提示操作。

### Cursor（通过插件市场）

在 Cursor Agent 聊天中，从市场安装：

```
/add-plugin superpowers
```

或者在插件市场中搜索 "superpowers"。

### OpenCode

告诉 OpenCode：

```
Fetch and follow instructions from https://raw.githubusercontent.com/obra/superpowers/refs/heads/main/.opencode/INSTALL.md
```

**详细文档：** [docs/README.opencode.md](https://github.com/obra/superpowers/blob/main/docs/README.opencode.md)

### GitHub Copilot CLI

```
copilot plugin marketplace add obra/superpowers-marketplace
copilot plugin install superpowers@superpowers-marketplace
```

### Gemini CLI

```
gemini extensions install https://github.com/obra/superpowers
```

更新：

```
gemini extensions update superpowers
```

## 基本工作流程

1. **头脑风暴** - 在编写代码之前激活。通过提问来完善粗略的想法，探索替代方案，分块展示设计以供验证。保存设计文档。
2. **使用 Git 工作树** - 在设计批准后激活。在新建分支上创建隔离的工作空间，运行项目设置，验证干净的测试基线。
3. **编写计划** - 在获得批准的设计后激活。将工作分解为小块任务（每个 2-5 分钟）。每个任务都包含确切的文件路径、完整的代码、验证步骤。
4. **子代理驱动开发** 或 **执行计划** - 在获得计划后激活。为每个任务派遣全新的子代理，并进行两阶段审查（规格合规性审查，然后是代码质量审查），或者分批执行并设置人工检查点。
5. **测试驱动开发** - 在实施过程中激活。强制执行红-绿-重构：编写失败的测试，观察它失败，编写最少量的代码，观察它通过，提交。删除在测试之前编写的代码。
6. **请求代码审查** - 在任务之间激活。对照计划进行审查，按严重程度报告问题。严重问题会阻止进度。
7. **完成开发分支** - 在任务完成时激活。验证测试，提供选项（合并/拉取请求/保留/丢弃），清理工作树。

**智能体在执行任何任务之前都会检查相关技能。** 这些是强制性的工作流程，而非建议。

## 内容概览

### 技能库

**测试**

- **测试驱动开发** - 红-绿-重构循环（包含测试反模式参考）

**调试**

- **系统性调试** - 四阶段根本原因分析流程（包含根本原因追踪、纵深防御、基于条件的等待技术）
- **完成前验证** - 确保问题真正被修复

**协作**

- **头脑风暴** - 苏格拉底式的设计完善
- **编写计划** - 详细的实施计划
- **执行计划** - 带检查点的批量执行
- **派遣并行代理** - 并发子代理工作流
- **请求代码审查** - 预审查检查清单
- **接收代码审查** - 回应反馈
- **使用 Git 工作树** - 并行开发分支
- **完成开发分支** - 合并/拉取请求决策流程
- **子代理驱动开发** - 通过两阶段审查（规格合规性，然后是代码质量）进行快速迭代

**元技能**

- **编写技能** - 遵循最佳实践创建新技能（包含测试方法论）
- **使用 Superpowers** - 技能系统介绍

## 核心理念

- **测试驱动开发** - 始终先写测试
- **系统性优于临时性** - 流程胜过猜测
- **降低复杂度** - 将简洁性作为首要目标
- **证据胜于断言** - 在宣称成功之前先验证

阅读[最初的发布声明](https://blog.fsck.com/2025/10/09/superpowers/)。

## 贡献

以下是 Superpowers 的一般贡献流程。请记住，我们通常不接受新技能的贡献，而且任何技能的更新都必须适用于我们支持的所有编程智能体。

1. Fork 仓库
2. 切换到 'dev' 分支
3. 为你的工作创建一个分支
4. 遵循 `writing-skills` 技能来创建和测试新技能及修改后的技能
5. 提交拉取请求，请务必填写拉取请求模板。

完整的指南请参见 `skills/writing-skills/SKILL.md`。

## 更新

Superpowers 的更新在某种程度上取决于编程智能体，但通常是自动的。

## 许可证

MIT 许可证 - 详情请参见 LICENSE 文件。

## 社区

Superpowers 由 [Jesse Vincent](https://blog.fsck.com/) 和 [Prime Radiant](https://primeradiant.com/) 的其他人员构建。

- **Discord**：[加入我们](https://discord.gg/35wsABTejz)，获取社区支持、提问以及分享你使用 Superpowers 构建的内容
- **Issues**：[https://github.com/obra/superpowers/issues](https://github.com/obra/superpowers/issues)
- **发布通知**：[注册](https://primeradiant.com/superpowers/)以获取新版本的通知
