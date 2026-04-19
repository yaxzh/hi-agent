import os

from cohere.manually_maintained.cohere_aws import mode
from dotenv import load_dotenv
from mistralai.extra.run import result
from openai import AsyncOpenAI
from pydantic_ai import Agent
from pydantic_ai.models.openai import OpenAIChatModel
from pydantic_ai.providers.openai import OpenAIProvider
from pydantic import BaseModel
import skills_tool

load_dotenv()

custom_client = AsyncOpenAI(
    base_url=os.getenv("OPENAI_API_URL"),
    api_key=os.getenv("OPENAI_API_KEY"))
model = OpenAIChatModel("glm-4.7", provider=OpenAIProvider(openai_client=custom_client))

class WeatherAnswer(BaseModel):
    city: str
    weather: str
    temperature: float
    suggestion: str

# 创建 Agent
agent = Agent(
    model=model,
    system_prompt=skills_tool.build_skill_prompt())

# 注册工具
@agent.tool_plain
def get_weather(location: str) -> str:
    """查询城市天气"""
    return f"{location}: 晴， 28 ℃"

@agent.tool_plain
def skills_list(dump: str = "") -> str:
    """列出所有可用的技能"""
    return skills_tool.skills_list()

@agent.tool_plain
def skill_view(name: str) -> str:
    """查看指定技能的详细内容"""
    return skills_tool.skill_view(name)

if __name__ == '__main__':
    print("hi-agent v2 (Pydantic AI)已经启动，输入q退出")
    history = []
    while True:
        user_input = input("你： ").strip()
        if not user_input:
            continue
        if user_input in ("q", "quit"):
            break
        result = agent.run_sync(user_input, message_history=history)
        history = result.all_messages()
        print(f"Agent: {result.output}\n")

