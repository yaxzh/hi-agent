# hi-agent

一个用于学习 AI Agent 编程的 Python 项目，借鉴 [hermes-agent](https://github.com/NousResearch/Hermes-Agent) 架构设计。

## 特性

- **工具注册表** — 自注册模式，加新工具不改 agent 循环
- **Skill 文档系统** — 渐进式披露（skills_list → skill_view → run_script）
- **Agent 循环** — LLM + Tool Calling 的核心模式
- **兼容 OpenAI API** — 支持智谱 GLM 等兼容接口

## 快速开始

### 环境要求

- Python 3.13+
- [uv](https://docs.astral.sh/uv/) 包管理器

### 安装

```bash
git clone git@github.com:yaxzh/hi-agent.git
cd hi-agent
uv sync
```

### 配置

创建 `.env` 文件：

```
OPENAI_API_KEY=your-api-key
OPENAI_BASE_URL=https://open.bigmodel.cn/api/paas/v4
```

### 运行

```bash
uv run main.py
```

## 项目结构

```
hi-agent/
├── main.py           # 入口 + agent 循环
├── registry.py       # 工具注册表（ToolRegistry 单例）
├── skills_tool.py    # Skill 文档系统（skills_list / skill_view / run_script）
├── skills/           # Skill 文档目录
│   ├── weather/      # 天气查询 skill
│   │   └── SKILL.md
│   └── calculator/   # 计算器 skill
│       ├── SKILL.md
│       └── scripts/calc.py
└── .env              # API 配置
```

## 核心架构

### Agent 循环

所有 agent 框架的底层模式：

```
调 LLM（带工具列表）
  ↓
LLM 返回 tool_calls？
  ├── 是 → 执行工具 → 结果喂回 LLM → 重复
  └── 否 → 返回最终回答
```

### 工具注册表

```python
from registry import registry

def my_tool(param: str) -> str:
    return f"result: {param}"

registry.register(
    name="my_tool",
    schema={"name": "my_tool", "description": "...", "parameters": {...}},
    handler=my_tool,
)
```

Agent 循环统一通过 `registry.dispatch(name, args)` 调用。

### Skill 系统

Skill 是给 LLM 看的 Markdown 文档，不是代码。三级渐进式披露：

| 层级 | 工具 | 内容 |
|---|---|---|
| 1 | `skills_list()` | 名称 + 描述摘要 |
| 2 | `skill_view(name)` | 完整 SKILL.md + 脚本列表 |
| 3 | `run_script(name, script_name, args)` | 执行 skill 下的脚本 |

### 添加新 Skill

1. 在 `skills/` 下创建目录，写入 `SKILL.md`：

```yaml
---
name: my-skill
description: 我的技能描述
---

## 指令
1. 调用 xxx 工具
2. 处理结果返回给用户
```

2. （可选）在目录下创建 `scripts/` 放脚本

## 致谢

架构灵感来自 [hermes-agent](https://github.com/NousResearch/Hermes-Agent)。
