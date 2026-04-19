"""简单计算器脚本"""
import sys

if len(sys.argv) < 2:
    print("Usage: python calc.py '<expression>'")
    sys.exit(1)

expression = sys.argv[1]
try:
    result = eval(expression, {"__builtins__": {}}, {})
    print(f"{expression} = {result}")
except Exception as e:
    print(f"Error: {e}")
    sys.exit(1)
