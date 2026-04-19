import json
from typing import Callable


class ToolRegistry:
    def __init__(self):
        self._tools = {}

    def register(self, name: str, schema: dict, handler: Callable):
        self._tools[name] = {
            'schema': schema,
            "handler": handler
        }

    def get_schema(self, name: str) -> list[dict]:
        """返回所有工具的schema（传给LLM的tools参数）"""
        return [
            {"type": "function", "function": tool['schema']} for tool in self._tools.values()
        ]

    def dispatch(self, name: str, args: dict) -> str:
        """根据名字执行工具，返回结果字符串"""
        if name not in self._tools:
            return json.dumps({"error": f"Unknown tool: {name}"}, ensure_ascii=False)
        try:
            result = self._tools[name]['handler'](**args)
            return result if isinstance(result, str) else json.dumps(result, ensure_ascii=False)
        except Exception as e:
            return json.dumps({"error": str(e)}, ensure_ascii=False)

registry = ToolRegistry()
