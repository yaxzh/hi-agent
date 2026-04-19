# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**hi-agent** — a learning project for AI agent programming, inspired by hermes-agent architecture.

- **Python**: 3.13+
- **Package manager**: `uv`
- **LLM**: 智谱 GLM (via OpenAI-compatible API)
- **Dependencies**: openai, python-dotenv, pyyaml

## Commands

```bash
uv run main.py          # Run the agent
uv add <package>        # Add a dependency
```

## Architecture

```
main.py           # 入口 + agent 循环
registry.py       # 工具注册表（ToolRegistry 单例）
skills_tool.py    # Skill 文档系统（skills_list / skill_view）
skills/           # SKILL.md 文档目录（每个 skill 一个子目录）
.env              # OPENAI_API_KEY, OPENAI_BASE_URL
```

### 核心模式

- **工具注册表**：每个工具调用 `registry.register()` 自注册，agent 循环用 `registry.dispatch()` 统一调用
- **Skill 文档系统**：SKILL.md 带 YAML frontmatter，渐进式披露（skills_list → skill_view）
- **Agent 循环**：调 LLM → 检查 tool_calls → 执行 → 喂回 → 重复直到无 tool_calls

### 添加新工具

1. 写函数 + `registry.register(name, schema, handler)`
2. 在 skills/ 下建目录写 SKILL.md（可选）

### 注意事项

- GLM API 不接受空 `properties`，无参数工具需要加占位字段
- SKILL.md 文件名必须大写
- registry.dispatch 用 `**args` 解包参数
