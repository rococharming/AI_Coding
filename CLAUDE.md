# CLAUDE.md

本文件说明 Claude Code 在当前 Obsidian Vault 中的使用规范。

## 使用规范

- 当前工作目录就是 Obsidian Vault 根目录。
- 优先通过 obsidian-cli skill 调用命令
- 所有命令默认加上 silent（除非特别说明要在前台打开）
- 标签搜索优先使用 obsidian tag 命令，比全文搜索更精确
- 文件创建、写入等操作须以当前工作目录为基准直接落盘，不依赖 Obsidian 内部路径解析（避免受「新建笔记存放位置」等设置影响）