#!/usr/bin/env python3
"""Enfirst Bridge - 5 场景测试用例

运行：
    python test_bridge.py
    python test_bridge.py --verbose

覆盖：
    1. 语种检测（英语/中文/日文/韩文/俄文/阿拉伯文/混合）
    2. 5 场景翻译指令生成（对话/代码/图片/文案/Agent）
    3. 边界（空输入/纯英语/纯数字/纯代码）
"""
import sys
import json
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from detect_lang import detect_language
from translate import build_translation_directive


def _assert(cond, msg):
    if not cond:
        print(f"  [FAIL] {msg}")
        return False
    print(f"  [PASS] {msg}")
    return True


def test_detect_english():
    print("\n[语种检测] 英语输入不触发桥")
    r = detect_language("Hello world, how are you?")
    return _assert(not r["trigger"], "英语不触发") and _assert(r["primary"] == "en", "主语种=en")


def test_detect_chinese():
    print("\n[语种检测] 中文输入触发桥")
    r = detect_language("你好世界")
    return _assert(r["trigger"], "中文触发") and _assert(r["primary"] == "zh", "主语种=zh")


def test_detect_japanese():
    print("\n[语种检测] 日文输入触发桥")
    r = detect_language("こんにちは世界")
    return _assert(r["trigger"], "日文触发") and _assert(r["primary"] == "ja", "主语种=ja")


def test_detect_korean():
    print("\n[语种检测] 韩文输入触发桥")
    r = detect_language("안녕하세요")
    return _assert(r["trigger"], "韩文触发") and _assert(r["primary"] == "ko", "主语种=ko")


def test_detect_russian():
    print("\n[语种检测] 俄文输入触发桥")
    r = detect_language("Привет мир")
    return _assert(r["trigger"], "俄文触发") and _assert(r["primary"] == "ru", "主语种=ru")


def test_detect_arabic():
    print("\n[语种检测] 阿拉伯文输入触发桥")
    r = detect_language("مرحبا بالعالم")
    return _assert(r["trigger"], "阿拉伯文触发") and _assert(r["primary"] == "ar", "主语种=ar")


def test_detect_mixed():
    print("\n[语种检测] 中英混合输入触发桥")
    r = detect_language("请帮我 run 这个 script")
    return _assert(r["trigger"], "混合触发（含中文）")


def test_detect_empty():
    print("\n[语种检测] 空输入不触发桥")
    r = detect_language("")
    return _assert(not r["trigger"], "空输入不触发")


def test_detect_code_only():
    print("\n[语种检测] 纯代码输入（含注释）")
    r = detect_language("const x = 1; // variable")
    return _assert(not r["trigger"], "纯 ASCII 代码不触发")


def test_scenario_dialog():
    print("\n[场景: 对话]")
    r = build_translation_directive("你觉得这个方案怎么样？", "dialog")
    return _assert(r["need_bridge"], "触发桥") and _assert("语义忠实" in " ".join(r["rules"]), "对话规则已注入")


def test_scenario_code():
    print("\n[场景: 代码]")
    r = build_translation_directive("在 handleSubmit 里加校验", "code")
    return _assert(r["need_bridge"], "触发桥") and _assert(any("标识符" in rule for rule in r["rules"]), "代码规则已注入")


def test_scenario_image():
    print("\n[场景: 图片]")
    r = build_translation_directive("赛博朋克城市夜景", "image")
    return _assert(r["need_bridge"], "触发桥") and _assert(any("关键词短语" in rule for rule in r["rules"]), "图片规则已注入")


def test_scenario_copy():
    print("\n[场景: 文案]")
    r = build_translation_directive("给'云小宝'写slogan", "copy")
    return _assert(r["need_bridge"], "触发桥") and _assert(any("品牌名" in rule for rule in r["rules"]), "文案规则已注入")


def test_scenario_agent():
    print("\n[场景: Agent]")
    r = build_translation_directive("每天8点用sendEmail发报告", "agent")
    return _assert(r["need_bridge"], "触发桥") and _assert(any("工具名" in rule for rule in r["rules"]), "Agent规则已注入")


def test_english_skip():
    print("\n[边界] 英语输入跳过桥")
    r = build_translation_directive("write a function", "code")
    return _assert(not r["need_bridge"], "英语跳过")


def main():
    tests = [
        test_detect_english, test_detect_chinese, test_detect_japanese,
        test_detect_korean, test_detect_russian, test_detect_arabic,
        test_detect_mixed, test_detect_empty, test_detect_code_only,
        test_scenario_dialog, test_scenario_code, test_scenario_image,
        test_scenario_copy, test_scenario_agent, test_english_skip,
    ]
    passed = 0
    failed = 0
    for t in tests:
        try:
            ok = t()
            if ok:
                passed += 1
            else:
                failed += 1
        except Exception as e:
            print(f"  [ERROR] {t.__name__}: {e}")
            failed += 1
    print(f"\n{'='*40}")
    print(f"结果: {passed} passed, {failed} failed, {len(tests)} total")
    sys.exit(0 if failed == 0 else 1)


if __name__ == "__main__":
    main()
