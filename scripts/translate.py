#!/usr/bin/env python3
"""Enfirst Bridge - 直线翻译核心脚本

将非英语输入一次性直译为英语锚点，遵循 SKILL.md 的 R1-R6 规则。
本脚本供 Agent / 自动化调用，也可独立测试。

用法：
    python translate.py --input "改一下 fetchUserData 函数" --scenario code
    python translate.py --input "赛博朋克城市" --scenario image
    python translate.py --input "你觉得呢" --scenario dialog

注意：本脚本不内置翻译模型，它输出的是「翻译指令模板 + 场景规则」，
由调用方（AI 模型 / Agent）按模板执行实际翻译。这样设计是因为
真正的"直线翻译"由模型的英语理解能力完成，脚本负责规范化流程与规则注入。
"""
import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from detect_lang import detect_language


SCENARIO_RULES = {
    "dialog": {
        "name": "普通对话",
        "rules": [
            "语义忠实，保留语气（疑问/命令/感叹）",
            "直译优先，不意译不润色",
            "量化词保留数字（'三个' → 'three'）",
            "不加'翻译如下'等前缀",
        ],
        "example_in": "你觉得这个方案怎么样？",
        "example_out": "what do you think of this plan?",
    },
    "code": {
        "name": "代码编程",
        "rules": [
            "保留所有标识符、函数名、变量名、API 名、文件路径（不翻译它们）",
            "保留错误信息原文",
            "只翻译自然语言部分",
            "代码块内的注释文本可译，但标识符不译",
        ],
        "example_in": "在 handleSubmit 里加一个表单校验，邮箱不能为空",
        "example_out": "add form validation in handleSubmit, email cannot be empty",
    },
    "image": {
        "name": "图片生成",
        "rules": [
            "翻译成英语关键词短语，而非完整句子",
            "保留风格名、艺术家名原文（如 'hanfu', 'ukiyo-e'）",
            "保留量化描述（'三只猫' → 'three cats'）",
            "输出格式：逗号分隔的关键词串，可直接作为 image prompt",
        ],
        "example_in": "画一个穿汉服的女孩在樱花树下读书，水彩风格",
        "example_out": "a girl in hanfu reading under cherry blossom tree, watercolor style",
    },
    "copy": {
        "name": "文案生成",
        "rules": [
            "翻译意图与受众",
            "保留品牌名、产品名、口号原文",
            "保留行业术语原文",
            "译出目标受众特征（'宝妈' → 'young mothers'）",
        ],
        "example_in": "给我们的产品'云小宝'写一句slogan，面向宝妈群体",
        "example_out": "write a slogan for our product '云小宝', targeting young mothers",
    },
    "agent": {
        "name": "Agent 搭建 / 自动化",
        "rules": [
            "翻译任务描述",
            "保留工具名、参数键、API 端点、命令行原文",
            "保留指令动词为英语（search, send, create 等）",
            "保留时间表达式原义（'每天早上8点' → 'every day at 8am'）",
        ],
        "example_in": "每天早上8点用 sendEmail 工具给团队发昨日报告",
        "example_out": "every day at 8am use the sendEmail tool to send yesterday's report to the team",
    },
}

CORE_RULES = [
    "R1 直译优先：逐句直译，不意译不润色",
    "R2 保留标识符：变量名/函数名/API名/路径不译",
    "R3 保留指令动词：Agent 场景动词原样保留为英语",
    "R4 保留图片关键词：图片场景关键词保留为英语供模型直接用",
    "R5 量化词保留数字：'三个'→'three', '百分之二十'→'twenty percent'",
    "R6 不加解释：翻译结果只有译文，不加前缀后缀",
]


def build_translation_directive(text: str, scenario: str = "auto") -> dict:
    """构建翻译指令（供模型执行）。

    返回 dict 含：
        - need_bridge: 是否需要触发桥
        - detected_lang: 检测到的语种
        - scenario: 实际使用的场景规则键
        - rules: 适用规则列表
        - example: 场景示例
        - directive: 完整指令文本（模型按此执行翻译）
    """
    lang_info = detect_language(text)

    if not lang_info["trigger"]:
        return {
            "need_bridge": False,
            "reason": "input is english or empty, skip bridge",
            "detected_lang": lang_info["primary"],
            "scenario": None,
            "rules": [],
            "example": None,
            "directive": None,
        }

    sc = scenario if scenario in SCENARIO_RULES else "dialog"
    rules = CORE_RULES + SCENARIO_RULES[sc]["rules"]
    example = {
        "input": SCENARIO_RULES[sc]["example_in"],
        "output": SCENARIO_RULES[sc]["example_out"],
    }

    directive = (
        f"[Enfirst Bridge - {SCENARIO_RULES[sc]['name']}场景]\n"
        f"将以下{lang_info['primary']}输入直线翻译为英语锚点。\n\n"
        f"规则：\n"
        + "\n".join(f"- {r}" for r in rules)
        + f"\n\n示例：\n  输入: {example['input']}\n  锚点: {example['output']}\n\n"
        f"待翻译输入：\n{text}\n\n"
        f"只输出英语锚点，不加任何前缀后缀解释。"
    )

    return {
        "need_bridge": True,
        "detected_lang": lang_info["primary"],
        "scenario": sc,
        "rules": rules,
        "example": example,
        "directive": directive,
    }


def main():
    ap = argparse.ArgumentParser(description="Enfirst Bridge 直线翻译核心")
    ap.add_argument("--input", "-i", required=True, help="待翻译文本")
    ap.add_argument(
        "--scenario", "-s",
        choices=["auto", "dialog", "code", "image", "copy", "agent"],
        default="auto",
        help="场景类型（auto=自动判定，默认 dialog 规则）",
    )
    ap.add_argument("--json", action="store_true", help="JSON 输出")
    args = ap.parse_args()

    sc = args.scenario if args.scenario != "auto" else "dialog"
    result = build_translation_directive(args.input, sc)

    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        if not result["need_bridge"]:
            print(f"[skip] {result['reason']}")
            sys.exit(0)
        print(f"检测语种: {result['detected_lang']}")
        print(f"场景: {result['scenario']}")
        print(f"适用规则 ({len(result['rules'])} 条):")
        for r in result["rules"]:
            print(f"  - {r}")
        print(f"\n翻译指令：\n{'-'*40}")
        print(result["directive"])
    sys.exit(0)


if __name__ == "__main__":
    main()
