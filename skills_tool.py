import json
import os
from unittest import result

import yaml

from registry import registry

SKILLS_DIR = os.path.join(os.path.dirname(__file__), "skills")

def _parse_frontmatter(content: str) -> tuple[dict, str]:
    """
    解析skill.md的yaml frontmatter和正文
    :param content:
    :return:
    """
    if content.startswith("---"):
        _, fm, body = content.split("---", 2)
        return yaml.safe_load(fm) or {}, body.strip()
    return {}, ""

def _scan_skills() -> list[dict]:
    """扫描skills目录，返回所有skill的元数据"""
    skills = []
    if not os.path.isdir(SKILLS_DIR):
        return skills
    for category_dir in sorted(os.listdir(SKILLS_DIR)):
        cat_path = os.path.join(SKILLS_DIR, category_dir)
        if not os.path.isdir(cat_path):
            continue
        skill_md = os.path.join(cat_path, "SKILL.md")
        if os.path.isfile(skill_md):
            with open(skill_md, "r", encoding="utf-8") as f:
                fm, _ = _parse_frontmatter(f.read())
            skills.append({
                "name": fm.get("name", category_dir),
                "description": fm.get("description", ""),
                "category": category_dir
            })
    return skills

def skills_list() -> str:
    skills = _scan_skills()
    return json.dumps({
        "success": True,
        "skills": skills,
        "count": len(skills),
        "hint": "使用skill_view(name)查看完整内容"
    }, ensure_ascii=False)

def skill_view(name: str) -> str:
    """查看指定skill的完整内容"""
    skill_dir = os.path.join(SKILLS_DIR, name)
    skill_md = os.path.join(skill_dir, "SKILL.md")
    if not os.path.isfile(skill_md):
        return json.dumps({"error": f"Skill '{name}' not found."}, ensure_ascii=False)
    with open(skill_md, "r", encoding="utf-8") as f:
        content = f.read()
    fm, body = _parse_frontmatter(content)
    scripts_dir = os.path.join(skill_dir, "scripts")
    scripts = sorted(os.listdir(scripts_dir)) if os.path.isdir(scripts_dir) else []
    return json.dumps({
        "success": True,
        "name": fm.get("name", name),
        "description": fm.get("description", ""),
        "content": body,
        "scripts": scripts,
        "hint": "可以用 run_script(name, script_name) 执行 scripts/ 下的脚本" if scripts else "",
    }, ensure_ascii=False)

def build_skill_prompt() -> str:
    """
    构建system prompt中的skill摘要
    :return:
    """
    skills = _scan_skills()
    lines = ["你可以使用以下技能(skill), 如果用户的问题与某个技能相关，请先调用skill_view查看详细指定：\n"]
    for s in skills:
        lines.append(f"  - {s['name']}: {s['description']}")
    return "\n".join(lines)

def run_script(name: str, script_name: str, args: str = "") -> str:
    script_path = os.path.join(SKILLS_DIR, name, "scripts", script_name)
    if not os.path.isfile(script_path):
        return json.dumps({"error": f"Script '{script_name}' not found in skill '{name}'."}, ensure_ascii=False)
    import subprocess
    try:
        result = subprocess.run(["python3", script_path] + (args.split() if args else []),
                                capture_output=True, text=True, timeout=30
                                )
        return json.dumps({
            "exit_code": result.returncode,
            "stdout": result.stdout.strip(),
            "stderr": result.stderr.strip()}, ensure_ascii=False)
    except Exception as e:
        return json.dumps({"error": str(e)}, ensure_ascii=False)


# 自注册到registry
registry.register(
    name = "skills_list",
    schema={
        "name": "skills_list",
        "description": "列出所有可用的技能",
        "parameters": {
            "type": "object",
            "properties": {"dummy": {"type": "string", "description": "无参数时传空字符串"}}
        }
    },
    handler=skills_list
)

registry.register(
    name = "skill_view",
    schema={
        "name": "skill_view",
        "description": "查看指定技能的详细内容",
        "parameters": {
            "type": "object",
            "properties": {"name": {"type": "string", "description": "技能名称"}},
            "required": ["name"]
        }
    },
    handler=skill_view
)

registry.register(
    name = "run_script",
    schema={
        "name": "run_script",
        "description": "执行指定skill里的脚本",
        "parameters": {
            "type": "object",
            "properties": {
                "name": {"type": "string", "description": "skill名称"},
                "script_name": {"type": "string", "description": "scripts/目录下的脚本文件名"},
                "args": {"type": "string", "description": "传递给脚本的参数，空格分隔"},
            },
            "required": ["name", "script_name"]
        }
    },
    handler=run_script
)
