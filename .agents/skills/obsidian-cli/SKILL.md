---
name: obsidian-cli
description: 使用 Obsidian CLI 与 Obsidian 仓库进行交互，包括读取、创建、搜索和管理笔记、任务、属性等。还支持插件和主题开发，提供重新加载插件、运行 JavaScript、捕获错误、截图和检查 DOM 等命令。当用户要求与其 Obsidian 仓库交互、管理笔记、搜索仓库内容、从命令行执行仓库操作，或开发和调试 Obsidian 插件与主题时使用。
---

# Obsidian CLI

使用 `obsidian` CLI 与运行中的 Obsidian 实例进行交互。需要 Obsidian 处于打开状态。

## 命令参考

运行 `obsidian help` 查看所有可用命令。该命令始终反映最新状态。完整文档：https://help.obsidian.md/cli

## 语法格式

**参数** 通过 `=` 接收值。含有空格的值需要加引号：

```bash
obsidian create name="My Note" content="Hello world"
```

**标志** 是布尔开关，不需要值：

```bash
obsidian create name="My Note" silent overwrite
```

多行内容使用 `\n` 表示换行，`\t` 表示制表符。

## 文件定位

许多命令接受 `file` 或 `path` 参数来指定目标文件。如果不提供这两个参数，则默认使用当前活动文件。

- `file=<名称>` — 类似 wikilink 的解析方式（只需名称，无需路径或扩展名）
- `path=<路径>` — 从仓库根目录开始的精确路径，例如 `folder/note.md`

## 仓库定位

命令默认面向最近聚焦的仓库。使用 `vault=<名称>` 作为第一个参数来指定目标仓库：

```bash
obsidian vault="My Vault" search query="test"
```

## 常用模式

```bash
obsidian read file="My Note"
obsidian create name="New Note" content="# Hello" template="Template" silent
obsidian append file="My Note" content="New line"
obsidian search query="search term" limit=10
obsidian daily:read
obsidian daily:append content="- [ ] New task"
obsidian property:set name="status" value="done" file="My Note"
obsidian tasks daily todo
obsidian tags sort=count counts
obsidian backlinks file="My Note"
```

在任何命令上使用 `--copy` 将输出复制到剪贴板。使用 `silent` 防止文件被打开。在列表命令上使用 `total` 获取计数。

## 插件开发

### 开发/测试循环

对插件或主题进行代码修改后，按以下流程操作：

1. **重新加载** 插件以使更改生效：
   ```bash
   obsidian plugin:reload id=my-plugin
   ```
2. **检查错误** — 如果出现错误，修复后从步骤 1 重复：
   ```bash
   obsidian dev:errors
   ```
3. **视觉验证** — 通过截图或 DOM 检查确认效果：
   ```bash
   obsidian dev:screenshot path=screenshot.png
   obsidian dev:dom selector=".workspace-leaf" text
   ```
4. **检查控制台输出** — 查看警告或意外日志：
   ```bash
   obsidian dev:console level=error
   ```

### 其他开发者命令

在应用上下文中运行 JavaScript：

```bash
obsidian eval code="app.vault.getFiles().length"
```

检查 CSS 值：

```bash
obsidian dev:css selector=".workspace-leaf" prop=background-color
```

切换移动端模拟：

```bash
obsidian dev:mobile on
```

运行 `obsidian help` 查看更多开发者命令，包括 CDP 和调试器控制。