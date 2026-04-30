---
title: "Superpowers"
type: tool
tags: [AI-Coding, Skill-Framework, TDD, Agent]
tools: [Claude Code, Cursor, Copilot, OpenAI Codex]
sources: [raw/01-articles/superpowers.md]
last_updated: 2026-04-30
---

# Superpowers

Superpowers 是由 Jesse Vincent 开发的一套**跨平台 AI 编程智能体技能框架与软件开发方法论**。它基于可组合的技能和初始指令构建，确保编程智能体遵循系统化的开发流程而非直接开始写代码。

## 核心理念

1. **测试驱动开发（TDD）**: 始终先写测试，红-绿-重构循环
2. **系统性优于临时性**: 流程胜过猜测，每个阶段都有明确技能触发
3. **降低复杂度**: 将简洁性作为首要目标
4. **证据胜于断言**: 在宣称成功之前先验证

## 基本工作流程

Superpowers 定义了 7 个阶段的标准化开发流程：

1. **头脑风暴（Brainstorming）**: 在编码前通过提问完善想法，探索替代方案，分块展示设计
2. **使用 Git 工作树**: 在新建分支上创建隔离工作空间，验证干净测试基线
3. **编写计划（Write Plan）**: 将工作分解为小块任务（每个 2-5 分钟），包含确切文件路径、完整代码、验证步骤
4. **子代理驱动开发 / 执行计划**: 为每个任务派遣子代理，进行两阶段审查（规格合规性 + 代码质量）
5. **测试驱动开发**: 强制执行红-绿-重构：编写失败测试 → 观察失败 → 编写最少代码 → 观察通过 → 提交
6. **请求代码审查**: 对照计划审查，按严重程度报告问题，严重问题阻止进度
7. **完成开发分支**: 验证测试，提供合并/PR/保留/丢弃选项，清理工作树

## 技能库

### 测试
- **测试驱动开发**: 红-绿-重构循环，含测试反模式参考

### 调试
- **系统性调试**: 四阶段根本原因分析（根本原因追踪、纵深防御、基于条件的等待技术）
- **完成前验证**: 确保问题真正被修复

### 协作
- **头脑风暴**: 苏格拉底式设计完善
- **编写计划**: 详细实施计划
- **执行计划**: 带检查点的批量执行
- **派遣并行代理**: 并发子代理工作流
- **请求/接收代码审查**: 预审查检查清单和反馈回应
- **使用 Git 工作树**: 并行开发分支管理
- **完成开发分支**: 合并/拉取请求决策流程
- **子代理驱动开发**: 通过两阶段审查快速迭代

### 元技能
- **编写技能**: 遵循最佳实践创建新技能
- **使用 Superpowers**: 技能系统介绍

## 跨平台支持

| 平台 | 安装方式 |
|------|----------|
| Claude Code | `/plugin install superpowers@claude-plugins-official` |
| Cursor | `/add-plugin superpowers` |
| GitHub Copilot CLI | `copilot plugin install superpowers@superpowers-marketplace` |
| OpenAI Codex CLI | 插件搜索安装 |
| Gemini CLI | `gemini extensions install https://github.com/obra/superpowers` |
| OpenCode | 从 GitHub 安装 |

## 关联链接
- [[Claude_Code]] — Claude Code 工具页
- [[Subagent]] — 子代理概念（Superpowers 核心依赖）
- [[摘要-superpowers]] — 原始素材摘要
