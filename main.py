import json
from dotenv import load_dotenv
from openai import OpenAI
from registry import registry
import skills_tool


load_dotenv()

client = OpenAI(timeout=300, max_retries=3)

def get_weather(location: str) -> str:
    return f"{location}: 晴，28℃"

def calculate(expression: str) -> str:
    """安全计算数学表达式"""
    try:
        result = eval(expression, {"__builtins__": {}}, {})
        return json.dumps({"expression": expression, "result": result}, ensure_ascii=False)
    except Exception as e:
        return json.dumps({"error": str(e)}, ensure_ascii=False)

registry.register(
    name="get_weather",
    schema={
        "name": "get_weather",
        "description": "查询城市天气",
        "parameters": {
                "type": "object",
                "properties": {"location": {"type": "string"}},
                "required": ["location"]
        }},
    handler=get_weather,
)

# registry.register(
#     name="calculate",
#     schema={
#         "name": "calculate",
#         "description": "计算数学表达式，支持加减乘除和基本运算",
#         "parameters": {
#             "type": "object",
#             "properties": {"expression": {"type": "string", "description": "数学表达式，如'15 * 23'"}},
#             "required": ["expression"]
#         }
#     },
#     handler=calculate,
# )

def agent(user_input):
    messages = [
        {"role": "system", "content": skills_tool.build_skill_prompt()},
        {"role": "user", "content": user_input}]
    while True:
        resp = client.chat.completions.create(
            model="glm-4.7",
            messages=messages,
            tools=registry.get_schema("all")
        )
        msg = resp.choices[0].message
        messages.append(msg)
        if not msg.tool_calls:
            return msg.content
        for tc in msg.tool_calls:
            print(tc.function)
            result = registry.dispatch(tc.function.name, json.loads(tc.function.arguments))
            messages.append({"role": "tool", "tool_call_id": tc.id, "content": result})

if __name__ == '__main__':
    # print(agent("深圳的天气怎么样?"))
    # print(agent("你有什么技能"))
    print(agent("帮我算15*23"))
