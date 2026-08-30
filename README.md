# Enfirst Bridge

> 非英语输入 → 英语理解桥。减少模型语言理解 token 消耗，统一跨场景语义路径。

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Skill](https://img.shields.io/badge/AI%20Skill-v1.0.0-blue)]()

## 这是什么

当今主流大模型以英语为语义锚定坐标系。处理非英语输入时，模型需要先在内部做一次隐式的「非英语 → 英语」对齐，这会**额外消耗语言理解 tokens**，且对齐路径可漂移、不稳定。

**Enfirst Bridge** 在输入进入主推理之前，先做一次显式、直线型的「非英语 → 英语」翻译，把翻译结果作为模型的唯一理解锚点：

- 减少 token 消耗（跳过内部隐式对齐）
- 理解路径呈直线（同一输入永远翻译成同一锚点，不漂移）
- 统一跨场景（对话 / 编程 / 图片 / 文案 / Agent 全走同一条管线）

## 一图看懂

```
用户输入（非英语）
    │
    ▼
[1] 语种检测 ── 英语则跳过
    ▼
[2] 直线翻译 ── 一次直译，保留场景标记
    ▼
[3] 英语锚点 ── 模型唯一理解输入
    ▼
[4] 主推理   ── 基于英语锚点执行意图
    ▼
[5] 场景输出 ── 按用户语言输出（非英语输出）
```

## 覆盖 5 类场景

| 场景 | 翻译侧重 |
|---|---|
| 普通对话 | 语义忠实，保留语气 |
| 代码编程 | 保留标识符 / 路径 / 报错原文 |
| 图片生成 | 译成英语关键词短语 |
| 文案生成 | 译意图与受众，保留品牌名 |
| Agent 自动化 | 译任务描述，保留工具名 / 参数键 |

## 核心原则

1. 只在非英语输入时触发
2. 翻译是直线型的——一次直译，不意译、不润色、不多版本
3. 翻译结果对用户透明（除非用户要求看）
4. 输出语言遵循用户设置（英语理解 ≠ 英语输出）

## 安装

```bash
# WorkBuddy / CodeBuddy（项目级）
cp -r enfirst-bridge/ <workspace>/.workbuddy/skills/

# WorkBuddy / CodeBuddy（用户级）
cp -r enfirst-bridge/ ~/.workbuddy/skills/

# Cursor
cp -r enfirst-bridge/ <project>/.cursor/skills/
```

## 脚本用法

```bash
# 语种检测
python scripts/detect_lang.py --input "你好世界"

# 直线翻译
python scripts/translate.py --input "改一下 fetchUserData 函数" --scenario code

# 运行测试
python scripts/test_bridge.py
```

## 文件结构

```
enfirst-bridge/
├── SKILL.md                  主指令
├── README.md                 本文件
├── scripts/
│   ├── detect_lang.py        语种检测
│   ├── translate.py          直线翻译核心
│   └── test_bridge.py        5 场景测试
├── references/
│   ├── scenario_rules.md     场景规则详解
│   └── token_benchmark.md    token 基准测试
└── examples/
    ├── dialog_example.md
    ├── code_example.md
    ├── image_example.md
    ├── copy_example.md
    └── agent_example.md
```

## Token 节省参考

| 输入长度 | 节省估算 | 说明 |
|---|---|---|
| 短（<50 字） | 5-15% | 内部对齐开销占比小 |
| 中（50-500 字） | 15-25% | 对齐开销显著 |
| 长（>500 字 / 多轮） | 25-35% | 且修正语义漂移，稳定性提升更大 |

> CJK 语种（中日韩）节省最明显，因字符密度高、内部对齐开销大。

## 版本与定价

### 免费版（Enfirst Bridge Free）

- 5 步直线管线全量开放
- 5 类场景翻译规则全量开放
- 语种支持：中/日/韩/俄/阿拉伯
- Token 节省：短 5-15%、中 15-25%、长 25-35%

### 加强版（Enfirst Bridge Pro）

| 功能 | Free | Pro |
|---|---|---|
| 基础管线 | ✅ | ✅ |
| 5 类场景 | ✅ | ✅ |
| 语种 | 5 种 | 30+ 种 |
| 语义锚点缓存 | ❌ | ✅ 语义 100% 不漂移 |
| 上下文记忆 | ❌ | ✅ 跨轮次记忆偏好术语 |
| 批量翻译 | ❌ | ✅ 100 条/批 |
| Token 节省上限 | 35% | 40% |

**定价**：

| 周期 | 价格 |
|---|---|
| 月付 | ¥29/月 |
| 年付 | ¥259/年（省 26%） |
| 永久 | ¥599 |

**购买**：对 AI 助手说"我想买 Pro 版"即可引导支付。

## 许可证

MIT — Free 版专享。Pro 版为专有服务，未经授权不得逆向或分发。
