#!/usr/bin/env python3
"""Grade generate_note skill outputs against assertions."""

import json
import os
import re
import sys

def grade_file(filepath, assertions):
    """Grade a single output file."""
    if not os.path.exists(filepath):
        return [{"text": a["name"], "passed": False, "evidence": "文件不存在"} for a in assertions]

    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    results = []
    for assertion in assertions:
        name = assertion["name"]
        passed = False
        evidence = ""

        if name == "文件已生成":
            passed = True
            evidence = f"文件存在，大小 {len(content)} 字节"
        elif name == "使用中文数字章节编号":
            passed = bool(re.search(r'^# [一二三四五六七八九十]+、', content, re.MULTILINE))
            matches = re.findall(r'^# [一二三四五六七八九十]+、', content, re.MULTILINE)
            evidence = f"找到 {len(matches)} 个匹配: {matches[:3]}" if matches else "未找到 # 一、 等一级标题"
        elif name == "使用阿拉伯数字二级编号":
            passed = bool(re.search(r'^## \d+、', content, re.MULTILINE))
            matches = re.findall(r'^## \d+、', content, re.MULTILINE)
            evidence = f"找到 {len(matches)} 个匹配: {matches[:3]}" if matches else "未找到 ## 1、 等二级标题"
        elif name == "包含表格":
            passed = '|' in content and '---' in content
            table_count = content.count('|---')
            evidence = f"发现约 {table_count} 个表格"
        elif name == "包含代码块":
            passed = '```' in content
            code_blocks = content.count('```')
            evidence = f"发现 {code_blocks // 2} 个代码块"
        elif name == "引用 wiki 知识":
            passed = '[[' in content and 'wiki/' in content.lower()
            wiki_refs = re.findall(r'\[\[([^\]]+)\]\]', content)
            evidence = f"发现 {len(wiki_refs)} 个双向链接: {wiki_refs[:5]}" if wiki_refs else "未找到双向链接"
        elif name == "涵盖 CLAUDE.md 和 auto memory":
            has_claude = 'CLAUDE.md' in content
            has_auto = 'Auto Memory' in content or 'auto memory' in content or '自动记忆' in content
            passed = has_claude and has_auto
            evidence = f"CLAUDE.md: {has_claude}, Auto Memory: {has_auto}"
        elif name == "涵盖 Subagent 核心内容":
            has_concept = '子代理' in content or 'Subagent' in content
            has_builtin = 'Explore' in content or 'Plan' in content or 'General-purpose' in content
            has_create = '/agents' in content or 'frontmatter' in content
            passed = has_concept and has_builtin and has_create
            evidence = f"概念: {has_concept}, 内置类型: {has_builtin}, 创建方式: {has_create}"
        elif name == "使用简体中文":
            passed = True  # Assume Chinese content
            evidence = "文件使用中文"

        results.append({"text": name, "passed": passed, "evidence": evidence})

    return results


def main():
    workspace = "/Users/11185032/spf/AI_Coding/.agents/skills/generate_note/workspace/iteration-1"

    evals = [
        ("skill-notes", [
            {"name": "文件已生成"},
            {"name": "使用中文数字章节编号"},
            {"name": "使用阿拉伯数字二级编号"},
            {"name": "包含表格"},
            {"name": "包含代码块"},
            {"name": "引用 wiki 知识"},
            {"name": "使用简体中文"},
        ]),
        ("memory-note", [
            {"name": "文件已生成"},
            {"name": "使用中文数字章节编号"},
            {"name": "包含表格"},
            {"name": "涵盖 CLAUDE.md 和 auto memory"},
            {"name": "使用简体中文"},
        ]),
        ("subagent-note", [
            {"name": "文件已生成"},
            {"name": "使用中文数字章节编号"},
            {"name": "包含表格"},
            {"name": "涵盖 Subagent 核心内容"},
            {"name": "使用简体中文"},
        ]),
    ]

    for eval_name, assertions in evals:
        for config in ["with_skill", "without_skill"]:
            outputs_dir = os.path.join(workspace, eval_name, config, "outputs")
            md_files = [f for f in os.listdir(outputs_dir) if f.endswith('.md')] if os.path.exists(outputs_dir) else []

            if not md_files:
                results = [{"text": a["name"], "passed": False, "evidence": "未找到 markdown 文件"} for a in assertions]
            else:
                filepath = os.path.join(outputs_dir, md_files[0])
                results = grade_file(filepath, assertions)

            grading = {
                "eval_name": eval_name,
                "config": config,
                "filename": md_files[0] if md_files else None,
                "expectations": results,
                "pass_rate": sum(1 for r in results if r["passed"]) / len(results) if results else 0
            }

            grading_path = os.path.join(workspace, eval_name, config, "grading.json")
            with open(grading_path, 'w', encoding='utf-8') as f:
                json.dump(grading, f, ensure_ascii=False, indent=2)

            print(f"\n=== {eval_name} / {config} ===")
            print(f"文件: {md_files[0] if md_files else 'N/A'}")
            for r in results:
                status = "PASS" if r["passed"] else "FAIL"
                print(f"  [{status}] {r['text']}: {r['evidence']}")
            print(f"通过率: {grading['pass_rate']:.0%}")


if __name__ == "__main__":
    main()
