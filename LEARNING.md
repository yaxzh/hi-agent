# AI Agent 学习进度

## 阶段一：手写 Agent（已完成）

### 1.1 Agent 核心循环
- [x] 理解 agent 循环模式：调 LLM → 检查 tool_calls → 执行工具 → 喂回 → 重复
- [x] 理解 message 的 role 类型：system、user、assistant、tool
- [x] 理解 tool_call 流程：LLM 返回 function name + arguments → 代码执行 → tool message 回传

### 1.2 工具注册表模式（借鉴 hermes-agent）
- [x] 实现 ToolRegistry 类：register()、get_schemas()、dispatch()
- [x] 自注册模式：每个工具调用 registry.register() 注册自己
- [x] agent 循环通过 registry.dispatch() 统一调用，不硬编码函数名

### 1.3 Skill 文档系统（借鉴 hermes-agent）
- [x] 理解渐进式披露：skills_list（摘要）→ skill_view（详情）→ run_script（执行）
- [x] SKILL.md 格式：YAML frontmatter + Markdown 指令
- [x] 实现 skills_list、skill_view、run_script 三个工具
- [x] system prompt 中嵌入 skill 摘要，LLM 按需加载

### 1.4 多轮对话记忆
- [x] messages 从局部变量变为模块级变量，跨轮次共享
- [x] 交互式循环：while True 读取用户输入

### 1.5 项目工程化
- [x] uv 包管理器使用
- [x] .env 环境变量管理（python-dotenv）
- [x] .gitignore 配置
- [x] Git 仓库初始化 + 推送到 GitHub
- [x] README.md 编写
- [x] CLAUDE.md 编写

---

## 阶段二：OpenAI SDK 深入（已完成）

### 2.1 OpenAI 客户端
- [x] OpenAI 初始化参数：api_key、base_url、timeout、max_retries、http_client 等
- [x] 环境变量自动读取：OPENAI_API_KEY、OPENAI_BASE_URL
- [x] 兼容智谱 GLM 等 OpenAI 兼容接口

### 2.2 Chat Completions API
- [x] create() 完整参数：model、messages、tools、temperature、max_tokens、stream、tool_choice 等
- [x] response 结构：choices、message、tool_calls、usage
- [x] token 用量统计：resp.usage.prompt_tokens / completion_tokens / total_tokens

### 2.3 OpenAI 客户端其他能力
- [x] chat.completions（对话）、images（图片）、audio（语音）、embeddings（向量）
- [x] models（模型管理）、fine_tuning（微调）、batches（批量）
- [x] stream() 流式输出、parse() 结构化输出

---

## 阶段三：框架认知（已完成）

### 3.1 LLM 客户端 SDK
| SDK | 了解程度 |
|---|---|
| openai | 深入使用 |
| anthropic | 了解存在，Claude 独有特性 |
| zhipuai | 了解，不如 openai 兼容模式通用 |

### 3.2 Agent 框架对比
| 框架 | 了解程度 | 核心理念 |
|---|---|---|
| Pydantic AI | 了解，推荐下一个学 | 类型安全、Pydantic 校验、输出可靠 |
| CrewAI | 了解 | 角色扮演多 agent 协作（Agent + Task + Crew） |
| AutoGen (AG2) | 了解 | 微软出品，对话式多 agent 讨论 |
| Smolagents | 了解 | HuggingFace 出品，极简，CodeAgent 模式 |
| LangChain | 了解 | 链式管道（A→B→C），适合 RAG |
| LangGraph | 了解 | 状态图（分支/循环/并行），适合复杂工作流 |

### 3.3 框架选择认知
- [x] 理解框架解决了什么问题：重复劳动 + 工程化（上下文压缩、错误重试、流式输出等）
- [x] 确定学习路径：手写（已完成）→ Pydantic AI → CrewAI → LangGraph

---

## 阶段四：hermes-agent 源码研读（已完成）

### 4.1 工具注册表（tools/registry.py）
- [x] ToolRegistry 单例 + 自注册模式
- [x] ToolEntry 存储：name、toolset、schema、handler、check_fn
- [x] dispatch 统一调度

### 4.2 Skills 系统
- [x] SKILL.md 文档格式（YAML frontmatter + 指令）
- [x] 三层渐进式披露：skills_list → skill_view → skill_view(file_path)
- [x] 三层缓存：LRU 内存 → 磁盘快照 → 全量扫描
- [x] 条件可见性：requires_tools、fallback_for_toolsets
- [x] 安全机制：原子写入、路径遍历防护、注入检测

### 4.3 Agent 循环（run_agent.py）
- [x] 迭代预算控制（max_iterations）
- [x] 工具并发执行（安全分类：可并行 / 必须串行）
- [x] 上下文压缩（接近 token 限制时自动摘要）

---

## 阶段五：Pydantic AI 实战（已完成）

### 5.1 框架迁移
- [x] 用 Pydantic AI 重写 hi-agent（main_v2.py）
- [x] 对比手写 vs 框架：代码量减少约 70%
- [x] 连接智谱 GLM：OpenAIModel + OpenAIProvider + AsyncOpenAI

### 5.2 Pydantic AI 核心模式
- [x] `@agent.tool_plain` 装饰器替代 `registry.register()`
- [x] `agent.run_sync()` / `agent.run()` 替代 while True 循环
- [x] `message_history` 参数管理多轮对话
- [x] `result_type=PydanticModel` 结构化输出
- [x] `result.output` 返回结果（v1.84+）
- [x] `result.all_messages()` / `stream.all_messages()` 获取完整消息历史

### 5.3 流式输出与错误重试
- [x] `agent.run_stream()` 流式输出
- [x] `stream.stream_output(delta=True)` 逐字输出（注意：不能用 stream_text，会跳过工具调用）
- [x] `Agent(retries=3)` LLM 输出无效时重试
- [x] `AsyncOpenAI(max_retries=3, timeout=...)` API 层重试

### 5.3 手写 vs 框架对比

| 手写 hi-agent | Pydantic AI |
|---|---|
| `while True` + tool_calls 判断 | `agent.run_sync()` |
| `registry.register(name, schema, handler)` | `@agent.tool_plain` |
| messages 模块级变量 | `message_history` 参数 |
| 手动拼 tool message | 自动管理 |
| 字符串输出 | 可选 Pydantic model 结构化输出 |

---

## 阶段六：待学习

- [ ] Pydantic AI 实战（用 Pydantic AI 重写 hi-agent）
- [ ] 流式输出（stream=True）
- [x] 错误重试策略
- [ ] 上下文压缩（对话太长时截断/摘要）
- [ ] 结构化输出（response_format + Pydantic model）
- [ ] CrewAI 多 agent 协作实战
- [ ] LangGraph 状态图工作流
- [ ] RAG（检索增强生成）

---

## 踩坑记录

| 问题 | 原因 | 解决 |
|---|---|---|
| ChatCompletionMessageParam 不能实例化 | 是 Union 类型别名，不是类 | 用 dict |
| GLM API 返回 400 | skills_list 的 parameters 用了 list 包 dict | 改为纯 dict |
| GLM API 不接受空 properties | 无参数工具的 properties 为 {} | 加占位字段 |
| handler(args) 参数没解包 | 传了整个 dict 而非关键字参数 | 改为 handler(**args) |
| run_script 没被 LLM 调用 | skill_view 没返回 scripts 列表 | skill_view 增加 scripts 字段 |
| IDE 类型警告 list[dict] | OpenAI SDK 要求具体 MessageParam 类型 | 加 list[dict] 类型注解 |
| stream_text() 不调工具 | Pydantic AI 的 stream_text 拿到首个文本就结束 | 改用 stream_output() |
