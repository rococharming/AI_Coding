# 一、概述

​	`SubAgent`是**专门处理特定任务的AI助手**。当`Claude Code`判断当前任务符合某`SubAgent`的描述时，会自动将任务委托给它，由子代理独立完成后返回结果。

​	每个子代理都有：

- 独立的上下文窗口
- 自定义的系统提示词
- 特定的工具权限
- 明确的触发条件

> 注意，`Subagent`在**单个会话内**工作，如果需要多个`agent`并行工作并相互通信，就需要用到`agent teams`。

​	`Subagent`具有如下优点：

1. 上下文保护：保护主对话上下文，把探索和实现过程隔离出去
2. 灵活控制权限：通过限制`Subagent`可用工具强制执行约束
3. 跨项目复用：设置用户级`Subagents`，在多个项目中复用配置
4. 专业化知识：每个子代理可以针对特定领域深度定制
5. 控制成本：简单任务可路由到更快、更便宜的模型



# 二、内置Subagents

 	`Claude Code`内置了一些`Subagents`，并会在合适的时候自动使用它们。每个内置`Subagent`都会继承父对话的权限，并有额外的工具限制。下面简单介绍。

## 1、Explore（探索代理）

​	`Explore`是一个快速、只读的`agent`，专为搜索和分析代码库而优化。

- 模型：Haiku，速度快、低延迟
- 工具：只读工具，禁止访问`Write`和`Edit`工具
- 用途：文件发现、代码搜索、代码库分析

​	当`Claude Code`需要探索或理解代码库，但不需要修改内容时，会委托给`Explore`，这样可以避免探索结果进入主对话上下文。

​	调用`Explore`时，`Claude Code`会自动指定探索细致程度：

- `quick`：用于目标明确的查找

- `medium`：用于平衡性探索

- `very thorough`：用于全面分析

## 2、Plan（规划代理）

​	`Plan`是一个研究型`agent`，主要在`plan mode`中使用，用于在提出计划之前收集上下文。

- 模型：继承自主对话
- 工具：只读工具，禁止访问`Write`和`Edit`工具
- 用途：为指定计划而进行代码库研究

​	当我们处于`plan mode`，并且`Claude Code`需要理解代码库时，它会把研究任务委托给`Plan`代理。

## 3、General-purpose（通用代理）

​	`General-purpose`是一个能力较强的通用`agent`，适合处理复杂、多步骤、并且需要同时探索和执行操作的任务。

- 模型：继承自主对话
- 工具：所有工具
- 用途：复杂研究、多步骤操作、代码修改

​	当任务同时需要探索和修改、需要复杂推理来解读结果，或者包含多个相互依赖的步骤时，`Claude Code`会委托给`General-purpose`。

## 4、Other

​	 `Claude Code`还包含**一些用于特定任务的辅助agents**。这些`agents`通常会被自动调用，因此一般不需要直接使用它们。

|        Agent        |  模型  |             何时使用              |
| :-----------------: | :----: | :-------------------------------: |
| `statusline-setup`  | Sonnet |  当运行`/statusline`配置状态栏时  |
| `Claude Code Guide` | Haiku  | 当询问`Claude Code`功能相关问题时 |



# 三、快速定义一个Subagent

## 1、/agents

​	执行`/agents`命令可以创建子代理。

![image-20260428141624412](assets/image-20260428141624412.png)

## 2、创建新代理

​	下面介绍如何使用`/agents`命令创建一个自定义`Subagent`。

1. 切换到`Library`标签页，选择`Create new agent`，选择要创建的subagent的位置。

![image-20260428142003487](assets/image-20260428142003487.png)

​     这里选择`Project`项目级Subagent，这样会把`Subagent`保存到当前项目的`.claude/agents`目录。



2. 描述Subagent

![image-20260428142228831](assets/image-20260428142228831.png)

​        这里选择让`Generate with Claude`，让`Claude Code`生成配置。

​	点击后，会要求描述该`Subagent`以及何时应该被使用，输入：

```text
一个代码改进代理，它会扫描项目文件，针对可读性、性能和最佳实践提出改进建议。它需要解释每个问题，展示当前代码，并提供改进后的版本
```

![image-20260428142538485](assets/image-20260428142538485.png)

​          `Enter`提交后，等待一阵子，`Claude Code`会自动生成该`Subagent`的`identifier`、`description`和`system prompt`。

![image-20260428142640665](assets/image-20260428142640665.png)



3. 选择工具

​        如果这是一个**只读审查器**，取消除`Read-only tools`之外的所有工具。

​	如果保持**所有工具都被选中**，则`Subagent`会**继承主对话可用的所有工具**。

![image-20260428143006790](assets/image-20260428143006790.png)

​	这里因为生成的代码改进代理，因此之需要只读工具即可。

​	点击`[ Continue ]`继续。



4. 选择模型

 	为子代理选择模型。这里的模型实际映射到接入的第三方模型。

![image-20260428143421704](assets/image-20260428143421704.png)

​         这里选择`Inherit from parent`。



5. 选择子代理的预览背景色

​      这里表示当调用子代理后，会话显示的子代理的背景色，方便用户清晰看到调用了子代理。

![image-20260428143500365](assets/image-20260428143500365.png)

​	这里选择红色，预览效果如上图所示。



6. 配置记忆

​	为子代理提供一个持久记忆目录。子代理会用它在不同对话之间积累洞察，例如代码库模式和反复出现的问题。若不希望子代理持久化学习内容，可选择`None`。

![image-20260428143708368](assets/image-20260428143708368.png)

​	这里选择项目级范围`Project scope`，它使用当前项目的`.claude/agent-memory`作为项目持久化目录。



7. 保存并试用

​	当一切都完成后，最终进入检查摘要配置。

​	如果觉得没有问题，按`s`或`Enter`保存。

​	如果觉得还需要自行修改，按`e`在编辑器打开文件进行编辑。

![image-20260428144547518](assets/image-20260428144547518.png)

​	保存后，因为默认生成的是英文版本，因此可以让`Claude Code`改成中文版本：

![image-20260428145215608](assets/image-20260428145215608.png)

​         之后，在对话框中就可以这样试用：

```text
使用 code-improvement-reviewer 为这个项目提供改进。 
```

​	`Claude Code`会委托给新的子代理，由它扫描代码库并返回改进建议。

​	如下图所示，这个红色背景说明子代理开始运行了：

![image-20260428145720094](assets/image-20260428145720094.png)

​	可以看到最终给出了符合要求的改进建议：

​	![image-20260428145830072](assets/image-20260428145830072.png)



# 四、配置子代理

## 1、/agents命令

​	`/agents`命令会打开一个带标签页的子代理管理界面。其中：

- `Running`标签显示正在运行的子代理，并允许你打开或停止它们。
- `Library`标签允许：
  - 查看所有可用子代理（内置 / 用户级 / 项目级 / 插件）
  - 创建新的子代理
  - 编译已有子代理配置和工具访问权限
  - 删除自定义子代理
  - 查看存在重名时哪个子代理处于激活状态

![image-20260428150449194](assets/image-20260428150449194.png)

​	这是**创建和管理子代理的推荐方式**，如果想手动创建，也可以直接添加子代理文件。

​	如果希望在命令行列出所有已配置子代理，而不进入交互式会话，执行：

```bash
claude agents
```

​	如图所示，该命令会按源对代理进行分组，并会表明哪些代理被更高优先级的定义覆盖：

![image-20260428150817120](assets/image-20260428150817120.png)



## 2、子代理的作用域

​	子代理是带有**`YAML frontmatter`的`Markdown`文件**。根据作用域不同，会把它们存放在不同的位置。当多个子代理使用相同名称时，优先级更高的位置生效。

|       位置       |      作用域      |  优先级   |           创建方式            |
| :--------------: | :--------------: | :-------: | :---------------------------: |
|     托管设置     |     组织范围     | 1（最高） |       通过托管设置部署        |
| --agents CLI标志 |     当前会话     |     2     | 启动`Claude Code`时传入`JSON` |
| .claude/agents/  |     当前目录     |     3     |       交互式或手动创建        |
| ~/.claude/agents |   你的所有项目   |     4     |       交互式或手动创建        |
| 插件的agents目录 | 启用该插件的位置 | 5（最低） |          随插件安装           |

​	项目子代理（`.claude/agents/`）适合专属于某个代码库的子代理，可以把它们提交到版本控制，方便团队共同使用和改进。

​	**项目子代理会从当前工作目录向上查找发现，通过`--add-dir`添加的目录只授予文件访问权限，不会扫描器其中的子代理配置**。若要在多个项目之间共享子代理，请使用`~/.claude/agents/`或插件。

​	用户子代理（`~/.claude/agents/`）是个人子代理，可用于所有项目。

​	CLI定义的子代理会在启动`Claude Code`时以`JSON`形式传入，它们只存在于当前会话中，不会保存到磁盘，适合快速测试和自动化脚本。可以在一次`--agents`调用定义多个子代理：

```bash
claude --agents '{
  "code-reviewer": {
    "description": "资深代码审查专家。在代码更改后主动使用。",
    "prompt": "你是一名高级代码审查员。重点关注代码质量、安全性和最佳实践。",
    "tools": ["Read", "Grep", "Glob", "Bash"],
    "model": "sonnet"
  },
  "debugger": {
    "description": "用于处理错误和测试失败的调试专家。",
    "prompt": "你是一名调试专家。分析错误，找出根本原因，并提供修复方案。"
  }
}'

```

​	`--agents` 标志接受的 JSON 字段与基于文件的子代理 frontmatter 字段相同，包括：`description`、`prompt`、`tools`、`disallowedTools`、`model`、`permissionMode`、`mcpServers`、`hooks`、`maxTurns`、`skills`、`initialPrompt`、`memory`、`effort`、`background`、`isolation` 和 `color`。其中 `prompt` 用作系统提示词，等同于文件式子代理中的 Markdown 正文。

​	托管子代理由组织管理员部署。把 Markdown 文件放在托管设置目录内的 `.claude/agents/` 中，格式与项目和用户子代理相同。对于相同名称的子代理，托管定义优先于项目和用户定义。

​	插件子代理来自安装的插件。它们会与自定义子代理一起出现在`/agents`中。

> 注意：处于安全考虑，插件子代理不支持`hooks`、`mcpServers`或`permissionMode`frontmatter字段。从插件加载代理时，这些字段会被忽略。
>
> 如果需要这些字段，请把代理文件复制到`.claude/agents`或`~/.claude/agents`。你也可以在 `settings.json` 或 `settings.local.json` 的 `permissions.allow` 中添加规则，但这些规则会应用到整个会话，而不是仅应用到插件子代理。

# 五、编写子代理文件

## 1、子代理文件的本质

​	子代理文件使用`YAML frontmatter`配置，后跟`Markdown`格式的system prompt（系统提示词）。

> 注意：子代理会在会话启动时自动加载。如果通过**手动添加文件**来创建子代理，需要**重启会话或使用`/agents`立即加载它**。

​	一个简单示例：

```markdown
---
name: code-review
description: 资深代码审查专家。在代码更改后主动使用。
tools: Read, Glob, Grep, Bash
model: sonnet
---

你是一名代码审查员。被调用时，请分析代码，并针对代码质量、安全性和最佳实践提供具体、可执行的反馈。
```

​	`frontmatter`定义子代理的元数据和配置。正文则是引导子代理行为的系统提示词（system prompt）。子代理只接收这个系统提示词，以及基本环境信息，例如工作目录，它不会接收完整的`Claude Code`系统提示词。

​	**子代理启动时位于主对话当前工作目录**。在子代理内部，`cd`命令并不会在`Bash`或`PowerShell`工具调用之间持久化，也不会影响主对话的工作目录。如果要给主仓库一个隔离的仓库副本，需要设置`isolation: worktree`。

## 2、支持的`frontmatter`片段

​	以下字段可用于`YAML frontmatter`。只有`name`和`description`是必填项。

| 字段              | 必填 | 说明                                                         |
| ----------------- | :--: | :----------------------------------------------------------- |
| `name`            |  是  | 唯一标识符，使用**小写字母和连字符**。                       |
| `description`     |  是  | 描述`Claude Code`应该在什么情况下把任务委托给该子代理。      |
| `tools`           |  否  | 子代理可以使用的工具。若省略，则继承所有工具。               |
| `disallowedTools` |  否  | 要禁止的工具，会从继承或指定的工具列表中移除。               |
| `model`           |  否  | 要使用的模型：`sonnet`、`opus`、`haiku`、完整模型 ID（例如 `claude-opus-4-7`）或 `inherit`。默认值为 `inherit`。 |
| `permissionMode`  |  否  | 权限模式：`default`、`acceptEdits`、`auto`、`dontAsk`、`bypassPermissions` 或 `plan`。 |
| `maxTurns`        |  否  | 子代理停止前允许的最大“思考+行动”轮数。                      |
| `skills`          |  否  | 启动时加载到子代理上下文中的技能。注入的是完整技能内容，不只是可调用入口。子代理不会继承父对话的技能。 |
| `mcpServers`      |  否  | 该子代理可用的 MCP 服务器。每项可以是已配置服务器名称，也可以是以内联方式定义的完整 MCP 服务器配置。 |
| `hooks`           |  否  | 作用于该子代理的生命周期钩子。                               |
| `memory`          |  否  | 持久记忆作用域：`user`、`project` 或 `local`。启用跨会话学习。 |
| `background`      |  否  | 设置为 `true` 时，该子代理总是作为后台任务运行。默认值为 `false`。 |
| `effort`          |  否  | 子代理活动时使用的推理努力级别。会覆盖会话级 `effort`。默认继承自会话。选项包括 `low`、`medium`、`high`、`xhigh`、`max`，可用级别取决于模型。 |
| `isolation`       |  否  | 设置为 `worktree` 时，子代理会在临时 git worktree 中运行，获得隔离的仓库副本。如果子代理未做修改，该 worktree 会自动清理。 |
| `color`           |  否  | 子代理在任务列表和记录中的显示颜色。可选：`red`、`blue`、`green`、`yellow`、`purple`、`orange`、`pink` 或 `cyan`。 |
| `initialPrompt`   |  否  | 当该代理通过`--agent`或agent设置作为主会话代理运行时，会自动作为第一条用户信息提交。命令和技能会被处理。该字段会被添加到用户提供的提示词之前。 |

​	

# 六、控制子代理的能力

​       可以通过工具访问权限、权限模式和条件规则控制子代理能做什么。

## 1、可用工具

​	子代理可以使用`Claude Code`的任何内置工具。默认情况下，子代理会继承主对话的所有工具，包括`MCP工具`。

​	若要限制工具，需要使用`tools`字段（白名单）和`disallowedTools`字段（黑名单）。

​	示例1：

```yaml
---
name: safe-researcher
description: Research agent with restricted capabilities
tools: Read, Grep, Glob, Bash
---
```

​	这表示该子代理只允许使用`Read`、`Grep`、`Glob`、`Bash`，因此不能编辑文件和写文件，也不能使用任何`MCP工具`。

​	示例2：

```YAML
---
name: no-writes
description: Inherits every tool except file writes
disallowedTools: Write, Edit
---
```

​	这表示该子代理会继承主会话的所有工具，但排除了`Write`和`Edit`。该子代理仍保留 Bash、MCP 工具和其他所有工具。

​	如果同时设置了`tools`和`disallowedTools`，会先继承或获取全部工具，再删掉`disallowedTools`，最后再用`tools`做筛选。如果某个工具既在 `tools` 又在 `disallowedTools` ，最终被禁用。



## 2、限制可以生成哪些子代理

​	当某个代理通过`claude --agent`作为主会话代理运行时，它可以使用Agent工具生成子代理。若要限制它可以生成哪些子代理类型，要在`tools`字段使用`Agent(agent_type)`语法。

​	示例：

```yaml
---
name: coordinator
description: 负责在多个专业子代理之间协调工作
tools: Agent(worker, researcher), Read, Bash
---
```

​	这是一个白名单：只允许生成`worker`和`research`子代理。若要允许所有子代理、但屏蔽特定代理，请使用 `permissions.deny`。

​	若要允许生成任意子代理且不加限制，则使用不带括号的`Agent`：

```YAML
tools: Agent, Read, Bash
```

​	如果`tools`列表完全省略`Agent`，则该代理不能生成任何子代理。这个限制只适用于通过 `claude --agent` 作为主线程运行的代理。子代理不能生成其他子代理，因此 `Agent(agent_type)` 在子代理定义中没有效果。

## 3、将MCP服务器限定到某个子代理

​	子代理引入`MCP server`有两种方式：内联（inline）定义和字符串引用。列表中的每一项可以是一个内联服务器定义，也可以是对会话中已配置 MCP 服务器的字符串引用：

```YAML
---
name: browser-tester
description: Tests features in a real browser using Playwright
mcpServers:
  # Inline definition: scoped to this subagent only
  - playwright:
      type: stdio
      command: npx
      args: ["-y", "@playwright/mcp@latest"]
  # Reference by name: reuses an already-configured server
  - github
---

Use the Playwright tools to navigate, screenshot, and interact with pages.
```

​	其中：

- 内联定义（inline）

```YAML
mcpServers:
	- playwright:
		type: stdio
		command: npx
		args: ["-y", "@playwright/mcp@latest"]
```

- 字符串引用（reference）

```yaml
mcpServers:
	- github
```

> 使用字符串引用的前提是已经在主对话配置了`github`这个MCP服务器。

​	使用`mcpServers`字段可以让子代理访问主对话不可用的MCP服务器。**以内联方式定义的服务器会在子代理启动时连接，并在子代理结束时断开。字符串引用会共享父会话中的连接**。	

​	如果你希望某个 MCP 服务器完全不进入主对话，避免其工具描述占用主上下文，就应在这里以内联方式定义，而不是放在 `.mcp.json` 中。这样只有子代理能获得这些工具，父对话不会获得。	

## 4、权限模式

​	`permissionMode` 字段控制子代理如何处理权限提示。子代理会继承主对话的权限上下文，并可以覆盖权限模式，但下文所述的父级优先情况除外。

| 模式                | 行为                                                         |
| ------------------- | ------------------------------------------------------------ |
| `default`           | 标准权限检查，并在需要时提示。                               |
| `acceptEdits`       | 自动接受工作目录或 `additionalDirectories` 中路径的文件编辑和常见文件系统命令。 |
| `auto`              | 自动模式：由后台分类器检查命令和受保护目录写入。             |
| `dontAsk`           | 自动拒绝权限提示；显式允许的工具仍可工作。                   |
| `bypassPermissions` | 跳过权限提示。                                               |
| `plan`              | 计划模式，只读探索。                                         |

​	如果父级使用`bypassPermissions`或`acceptEdits`，父级设置优先，子代理无法覆盖。如果父级使用自动模式，子代理会继承自动模式，其 frontmatter 中的 `permissionMode` 会被忽略：分类器会用与父会话相同的阻止和允许规则评估子代理的工具调用。

## 5、预加载技能到子代理

​	子代理不会继承父对话的技能，必须显式列出。使用`skills`字段可以在子代理启动时将技能注入其上下文。这样子代理无需在执行过程中发现和加载技能，就能获得领域知识。

```markdown
---
name: api-developer
description: Implement API endpoints following team conventions
skills:
  - api-conventions
  - error-handling-patterns
---

Implement API endpoints. Follow the conventions and patterns from the preloaded skills.
```

​	每个技能的**完整内容**都会注入子代理上下文，而不仅仅提供可调用入口。

​	有些`skill`可能设置了`disable-model-invocation: true`，即不允许模型主动调用/加载这个技能，因此这种技能不能预加载到子代理里，因为预加载使用的是`Claude Code`可以调用的一组技能。

## 6、启用持久记忆

​	`memory`字段会给子代理一个**可跨对话保留的持久记忆目录**。子代理用这个目录会随时间积累知识，例如代码库模式、调试洞察和架构决策。

```markdown
---
name: code-reviewer
description: Reviews code for quality and best practices
memory: user
---

You are a code reviewer. As you review code, update your agent memory with
patterns, conventions, and recurring issues you discover.
```

​	根据记忆适用范围选择作用域：

| 作用域    | 位置                                          | 适用场景                                       |
| --------- | --------------------------------------------- | ---------------------------------------------- |
| `user`    | `~/.claude/agent-memory/<name-of-agent>/`     | 子代理应在所有项目之间记住学习内容。           |
| `project` | `.claude/agent-memory/<name-of-agent>/`       | 子代理知识与项目相关，并且可通过版本控制共享。 |
| `local`   | `.claude/agent-memory-local/<name-of-agent>/` | 子代理知识与项目相关，但不应提交到版本控制。   |

​	启用`memory`后：

- 子代理系统提示词会包含读写记忆目录的说明
- 子代理系统提示词还会包含记忆目录中的`MEMORY.md`中的前200行或25KB内容，以先达到者为准，并包含在超出限制时整理 `MEMORY.md` 的说明。
- Read、Write 和 Edit 工具会自动启用，方便子代理管理自己的记忆文件

​	持久记忆建议：

- 推荐默认使用`project`作用域，它可以让子代理知识通过版本控制共享。若子代理知识普遍适用于多个项目，使用 `user`；若知识是项目特定但不应提交到版本控制，使用 `local`。
- **可以要求子代理在开始工作前先查阅自己的记忆**，例如："请审查这个 PR ，并检查你的记忆中是否有你之前见过的相关模式"
- **可以要求子代理完成任务后更新记忆**，"现在你已经完成任务，请把学到的内容保存到你你的记忆中"。久而久之，这会构建一个知识库，让子代理更有效。
- 可以直接在子代理的 `Markdown`文件中增加记忆指令，让它主动维护自己的知识库：

```markdown
当你发现代码路径、设计模式、库的位置以及关键架构决策时，及时更新你的代理记忆。这有助于在多次对话中逐步积累团队级的知识。请用简洁的方式记录你发现了什么，以及它所在的位置。
```

## 7、使用钩子定义条件规则

​	如果要更动态地控制工具使用，可以使用`PreToolUse`钩子，在操作执行前验证。当你需要允许某个工具的部分操作、同时阻止其他操作时，这非常有用。

​	例如创建一个只读数据库查询的子代理。`PreToolUse`钩子会在每个`Bash`命令执行前运行`command`中指定的脚本：

```markdown
---
name: db-reader
description: Execute read-only database queries
tools: Bash
hooks:
	PreToolUse:
---
```























