# Token 节省基准测试方法

## 测试目的

量化 Enfirst Bridge 在不同输入长度、不同语种下，相对"直接理解非英语"节省的语言理解 token 数量与比例。

## 测试方法

### 对照组设计

| 组 | 处理方式 | 说明 |
|---|---|---|
| A 对照 | 直接输入非英语，模型自行内部对齐 | 模拟无 Bridge 的常规流程 |
| B 实验 | Enfirst Bridge 翻译为英语锚点后输入 | 本 skill 流程 |

### 测试维度

1. **输入长度**：短（<50字）/ 中（50-500字）/ 长（>500字）
2. **语种**：中文、日文、韩文、俄文、阿拉伯文
3. **场景**：对话 / 代码 / 图片 / 文案 / Agent

### 测量指标

- **理解 token 消耗**：模型处理输入到开始输出之间的 input tokens
- **翻译额外 token**：B 组的翻译步骤本身消耗的 token（计入成本）
- **净节省**：A 组 input tokens - (B 组翻译 tokens + B 组锚点 input tokens)
- **净节省比例**：净节省 / A 组 input tokens

### 测量脚本框架

```python
# 伪代码，实际需对接模型 API 的 usage 字段
def benchmark(text, scenario, model):
    # A 组：直接输入
    resp_a = model.complete(text)
    tokens_a = resp_a.usage.prompt_tokens

    # B 组：先翻译
    anchor = enfirst_translate(text, scenario)  # 翻译消耗
    resp_translate = model.complete(translation_directive(text))
    tokens_translate = resp_translate.usage.prompt_tokens + resp_translate.usage.completion_tokens

    resp_b = model.complete(anchor)
    tokens_b = resp_b.usage.prompt_tokens + tokens_translate

    return {
        "group_a_tokens": tokens_a,
        "group_b_tokens": tokens_b,
        "translate_overhead": tokens_translate,
        "net_saved": tokens_a - tokens_b,
        "net_saved_ratio": (tokens_a - tokens_b) / tokens_a,
    }
```

## 预期结果（基于经验估算）

| 输入长度 | 语种 | 预期净节省比例 | 说明 |
|---|---|---|---|
| 短 | 中文 | 5-15% | 短输入对齐开销占比小，翻译自身开销相对大 |
| 中 | 中文 | 15-25% | 对齐开销显著，翻译开销占比下降 |
| 长 | 中文 | 25-35% | 长上下文语义漂移修正价值大于 token 节省 |
| 中 | 日文 | 15-25% | 与中文类似 |
| 中 | 韩文 | 15-25% | 与中文类似 |
| 中 | 俄文 | 10-20% | 西里尔字母 token 化效率高于 CJK，节省略低 |
| 中 | 阿拉伯文 | 15-25% | RTL 文字对齐开销大 |

## 注意事项

1. **翻译开销不可忽略**：Bridge 本身的翻译步骤消耗 token。短输入时翻译开销可能抵消节省，此时不建议触发。
2. **语义稳定性比 token 更重要**：长上下文里，Bridge 修正的语义漂移带来的质量提升，比 token 节省更有价值。
3. **不同模型差异大**：英语锚定型模型（GPT-4, Claude）节省明显；多语言原生模型（部分国产模型）节省较小。
4. **CJK 节省最明显**：中文字符 token 化效率低（1 个汉字常 = 1-2 token），英语更高效，所以 CJK → EN 的 token 节省最大。

## 何时不应使用 Bridge

- 输入 < 20 字：翻译开销 > 节省
- 纯情感陪伴对话：翻译破坏语气温度
- 用户明确要求"用我的母语思考"
- 输入已是英语
