---
name: lint
description: 对 Obsidian wiki/ 目录进行健康检查。优先使用 obsidian-cli（backlinks / search / tags）查找孤岛页面、死链、逻辑冲突、frontmatter 缺失。操作 wiki 文件时优先触发 obsidian-cli，减少文件系统遍历的 token 消耗。定期执行以保持知识库健康，并向用户报告发现的问题。
---

# Lint

Wiki 健康检查。

## 触发时机

- 用户说"/lint"
- 用户要求"检查 wiki 健康状态"
- 用户要求"扫描死链/孤岛页面"
- 定期维护（建议每周一次）

## 检查项

### 1. 孤岛页面（Orphan Pages）
**定义**：除 `index.md` 和 `log.md` 外，没有任何其他页面通过 `[[wikilink]]` 链接到它的页面。

**检查方法（优先使用 obsidian-cli）**：
1. 使用 `obsidian search query="path:wiki/" limit=1000` 获取 wiki 下所有页面
2. 对每个页面执行 `obsidian backlinks path="wiki/..."`
3. 如果 backlinks 返回为空，标记为孤岛页面

**处理建议**：
- 在相关页面中添加指向该孤岛页面的链接
- 或判断该页面是否应删除/合并

### 2. 死链（Dead Links）
**定义**：`[[页面名称]]` 链接到一个不存在的 `.md` 文件。

**检查方法**：
1. 使用 `obsidian read path="wiki/..."` 读取页面内容
2. 提取所有 `[[...]]` 链接的目标名称
3. 使用 `obsidian search query="目标名称"` 验证目标文件是否存在
4. 不存在的标记为死链

**处理建议**：
- 创建缺失的目标页面
- 或修正/删除错误的链接

### 3. 逻辑冲突（Conflicts）
**定义**：两个（或多个）页面对同一事实给出矛盾的说法，且未被标记在 `## 知识冲突` 区域。

**检查方法**：
- 使用 `obsidian read` 读取相关页面内容
- 识别涉及相同实体/概念的主张
- 对比不同页面中的描述
- 发现矛盾时检查是否已有 `## 知识冲突` 标注

**处理建议**：
- 在相关页面中新建/更新 `## 知识冲突` 区块
- 保留两种说法并做对比说明
- 在 log.md 中记录

### 4. Frontmatter 完整性
**检查内容**：
- 使用 `obsidian read` 读取页面
- 检查是否包含 YAML frontmatter（`---` 包裹）
- `title` 是否存在且非空
- `type` 是否为 tool/concept/entity/source/workflow 之一
- `tags` 是否存在（可为空数组）
- `last_updated` 是否为 YYYY-MM-DD 格式

### 5. 索引同步
**检查 `wiki/index.md` 是否包含所有 wiki 页面**：
- 使用 `obsidian read path="wiki/index.md"` 读取索引
- 使用 `obsidian search query="path:wiki/" limit=1000` 获取所有实际页面
- 对比两者，找出缺失或多余的条目

### 6. 日志完整性
**检查 `wiki/log.md`**：
- 使用 `obsidian read path="wiki/log.md"` 读取日志
- 格式是否符合 `## [YYYY-MM-DD] <动作> | <简述>`
- 最近的 ingest/query/lint 操作是否已记录

## qmd 辅助增强（大规模 wiki 时启用）

当 wiki 页面数 ≥ 100 时，可利用 qmd 加速以下检查：

### 快速死链验证

传统方式：读取每个文件提取 `[[...]]`，逐个检查文件是否存在。

优化方式：对每个 `[[页面名称]]` 链接目标执行：
```bash
qmd search "页面名称" --limit 1
```
如果无结果，则判定为死链。qmd 的搜索覆盖全文和路径，比简单文件名匹配更可靠。

### 孤立页面检查（辅助）

使用 `qmd search "path:wiki/" --limit 1000` 获取所有页面，结合 `obsidian backlinks` 检查入站链接。

### 重复内容检测

使用 `qmd vsearch "页面核心概念"` 检查是否有多个页面对同一概念给出了高度相似的内容，提示可能需要合并。

## 执行流程

1. **获取页面列表**：`obsidian search query="path:wiki/" limit=1000`
2. **检查孤岛页面**：对每个页面执行 `obsidian backlinks path="..."`
3. **检查死链**：读取页面内容，提取 `[[...]]`，用 search 验证目标
4. **检查 frontmatter**：`obsidian read` 读取样本页面验证
5. **检查索引同步**：对比 index.md 和 search 结果
6. **生成报告**：向用户汇报发现的问题

## 报告格式

```markdown
## [YYYY-MM-DD] lint | 健康检查

- **孤岛页面**: 2 个
  - [[UnlinkedPage]] — 无入站链接，建议添加到 [[Claude_Code]] 的关联链接中

- **死链**: 1 个
  - [[不存在的页面]] — 在 [[来源页面]] 中引用，建议创建或删除链接

- **逻辑冲突**: 1 处
  - [[Memory_System]] vs [[Claude_Code]] — 关于 auto memory 默认状态的描述不一致

- **Frontmatter 问题**: 0 个

- **索引不同步**: 1 个
  - wiki 中存在 [[NewPage]] 但未在 index.md 中列出

- **建议**: ...
```

## 修复优先级

1. **死链** — 影响页面可信度，优先修复
2. **孤岛页面** — 影响知识发现，次优先
3. **逻辑冲突** — 影响知识准确性，需人工判断
4. **索引不同步** — 影响导航，容易修复
5. **Frontmatter 问题** — 影响元数据，批量修复

## 关联链接
- [[index.md]] — 知识库总目录
- [[log.md]] — 操作日志
