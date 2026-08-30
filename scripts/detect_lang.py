#!/usr/bin/env python3
"""Enfirst Bridge - 语种检测脚本

检测输入文本的主语种，判定是否需要触发英语理解桥。

用法：
    python detect_lang.py --input "你好世界"
    python detect_lang.py --input "Hello world"
    python detect_lang.py --input "你好 hello 世界"
"""
import argparse
import re
import sys
import unicodedata


CJK_RANGES = [
    (0x4E00, 0x9FFF),    # CJK Unified Ideographs
    (0x3400, 0x4DBF),    # CJK Extension A
    (0x20000, 0x2A6DF),  # CJK Extension B
    (0x3040, 0x309F),    # Hiragana
    (0x30A0, 0x30FF),    # Katakana
    (0xAC00, 0xD7AF),    # Hangul
]
CYRILLIC = (0x0400, 0x04FF)
ARABIC = (0x0600, 0x06FF)
DEVANAGARI = (0x0900, 0x097F)


def _in_range(ch: str, lo: int, hi: int) -> bool:
    cp = ord(ch)
    return lo <= cp <= hi


def detect_language(text: str) -> dict:
    """检测文本主语种。

    返回:
        {
            "is_english": bool,        # 是否主英语（无需触发桥）
            "primary": str,            # 主语种代码
            "trigger": bool,           # 是否需触发 Enfirst Bridge
            "ratios": {lang: ratio},   # 各语种字符占比
            "non_latin": bool,          # 是否含非拉丁文字
        }
    """
    if not text or not text.strip():
        return {"is_english": True, "primary": "unknown", "trigger": False, "ratios": {}, "non_latin": False}

    total = 0
    counts = {
        "ascii_alpha": 0,
        "cjk": 0,
        "hiragana": 0,
        "katakana": 0,
        "hangul": 0,
        "cyrillic": 0,
        "arabic": 0,
        "devanagari": 0,
        "digit_punct": 0,
        "other": 0,
    }
    for ch in text:
        if ch.isspace() or ch.isdigit() or ch in ".,;:!?\"'()[]{}<>/*-+=@#$%^&_`|~\\":
            counts["digit_punct"] += 1
            continue
        cp = ord(ch)
        if cp < 128:
            counts["ascii_alpha"] += 1
        elif any(_in_range(ch, lo, hi) for lo, hi in [(0x4E00, 0x9FFF), (0x3400, 0x4DBF), (0x20000, 0x2A6DF)]):
            counts["cjk"] += 1
        elif _in_range(ch, 0x3040, 0x309F):
            counts["hiragana"] += 1
        elif _in_range(ch, 0x30A0, 0x30FF):
            counts["katakana"] += 1
        elif _in_range(ch, 0xAC00, 0xD7AF):
            counts["hangul"] += 1
        elif _in_range(ch, *CYRILLIC):
            counts["cyrillic"] += 1
        elif _in_range(ch, *ARABIC):
            counts["arabic"] += 1
        elif _in_range(ch, *DEVANAGARI):
            counts["devanagari"] += 1
        else:
            try:
                name = unicodedata.name(ch, "")
            except ValueError:
                name = ""
            if "CJK" in name:
                counts["cjk"] += 1
            else:
                counts["other"] += 1
        total += 1

    if total == 0:
        return {"is_english": True, "primary": "empty", "trigger": False, "ratios": {}, "non_latin": False}

    ratios = {k: v / total for k, v in counts.items() if v > 0}
    non_latin_chars = counts["cjk"] + counts["hiragana"] + counts["katakana"] + counts["hangul"] + counts["cyrillic"] + counts["arabic"] + counts["devanagari"]
    is_english = non_latin_chars == 0 and counts["ascii_alpha"] > 0
    non_latin = non_latin_chars > 0

    if counts["cjk"] > 0 or counts["hiragana"] > 0 or counts["katakana"] > 0:
        primary = "ja" if (counts["hiragana"] > 0 or counts["katakana"] > 0) else "zh"
    elif counts["hangul"] > 0:
        primary = "ko"
    elif counts["cyrillic"] > 0:
        primary = "ru"
    elif counts["arabic"] > 0:
        primary = "ar"
    elif counts["devanagari"] > 0:
        primary = "hi"
    else:
        primary = "en"

    return {
        "is_english": is_english,
        "primary": primary,
        "trigger": not is_english and non_latin,
        "ratios": {k: round(v, 3) for k, v in ratios.items()},
        "non_latin": non_latin,
    }


def main():
    ap = argparse.ArgumentParser(description="Enfirst Bridge 语种检测")
    ap.add_argument("--input", "-i", required=True, help="待检测文本")
    ap.add_argument("--json", action="store_true", help="JSON 输出")
    args = ap.parse_args()

    result = detect_language(args.input)
    if args.json:
        import json
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(f"输入: {args.input}")
        print(f"主语种: {result['primary']}")
        print(f"是否英语: {result['is_english']}")
        print(f"触发 Enfirst Bridge: {result['trigger']}")
        if result["ratios"]:
            print("字符占比:")
            for k, v in sorted(result["ratios"].items(), key=lambda x: -x[1]):
                print(f"  {k}: {v}")
    sys.exit(0 if not result["trigger"] else 1)


if __name__ == "__main__":
    main()
