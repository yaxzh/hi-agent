---
name: calculator
description: 数学计算工具，支持加减乘除和复杂表达式
version: 1.0.0
---

## 使用场景
当用户需要进行数学计算时使用此 skill。

## 指令
1. 从用户问题中提取数学表达式
2. 调用 `run_script` 工具，参数：name="calculator", script_name="calc.py", args=数学表达式
3. 将计算结果清晰地返回给用户
