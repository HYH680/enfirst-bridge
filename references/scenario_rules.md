# 5 场景翻译规则详解

本文件详细说明 Enfirst Bridge 在 5 类场景下的翻译规则与示例，供模型加载 skill 时参考。

## 通用核心规则（所有场景适用）

| 编号 | 规则 | 说明 |
|---|---|---|
| R1 | 直译优先 | 逐句直译，不意译、不润色、不做多版本对比 |
| R2 | 保留标识符 | 代码变量名、函数名、API名、文件路径不译 |
| R3 | 保留指令动词 | Agent 场景动词原样保留为英语 |
| R4 | 保留图片关键词 | 图片生成场景关键词保留为英语供模型直接用 |
| R5 | 量化词保留数字 | "三个"→"three", "百分之二十"→"twenty percent" |
| R6 | 不加解释 | 翻译结果只有译文，不加"翻译如下"等前缀 |

## 场景 A：普通对话

**翻译侧重**：语义忠实，保留语气。

**子规则**：
- A1 疑问句保留疑问结构：中文"…怎么样？" → 英语 "how about ...?"
- A2 命令句保留命令结构："帮我…" → "help me ..."
- A3 感叹语气保留："太好了" → "great" / "that's great"
- A4 语气词淡化但不删："吧/呢/啊" 用对应英语语气词或省略

**示例**：
| 输入 | 英语锚点 |
|---|---|
| 你觉得这个方案怎么样？ | what do you think of this plan? |
| 帮我看看这段代码有没有问题 | help me check if this code has problems |
| 太好了，就这么办 | great, let's do it this way |

## 场景 B：代码编程

**翻译侧重**：保留所有标识符、路径、错误信息原文。

**子规则**：
- B1 标识符不译：`fetchUserData`, `handleSubmit`, `API_KEY` 原样保留
- B2 文件路径不译：`src/components/Header.tsx` 原样保留
- B3 错误信息原文保留：`TypeError: cannot read property 'x' of undefined` 不译
- B4 注释文本可译：`// 用户登录` → `// user login`（但标识符不译）
- B5 技术术语保留英语：`state`, `hook`, `middleware`, `promise` 不译成中文

**示例**：
| 输入 | 英语锚点 |
|---|---|
| 在 handleSubmit 里加一个表单校验，邮箱不能为空 | add form validation in handleSubmit, email cannot be empty |
| 把 src/utils/auth.ts 里的 token 刷新逻辑提出来 | extract the token refresh logic from src/utils/auth.ts |
| 这个报错 TypeError: cannot read property 'x' of undefined 怎么解决 | how to fix this error TypeError: cannot read property 'x' of undefined |

## 场景 C：图片生成

**翻译侧重**：翻译成英语关键词短语（而非完整句子），因为图片模型吃关键词。

**子规则**：
- C1 输出格式：逗号分隔的关键词串，可直接作为 image prompt
- C2 风格名、艺术家名保留原文：`hanfu`, `ukiyo-e`, `cyberpunk`, `Studio Ghibli` 不译
- C3 量化描述保留数字：`三只猫` → `three cats`
- C4 构图词用英语：`特写` → `close-up`, `全景` → `wide shot`
- C5 光影词用英语：`逆光` → `backlit`, `柔光` → `soft lighting`

**示例**：
| 输入 | 英语锚点 |
|---|---|
| 画一个穿汉服的女孩在樱花树下读书，水彩风格 | a girl in hanfu reading under cherry blossom tree, watercolor style |
| 赛博朋克城市夜景，霓虹灯，雨天，广角 | cyberpunk city night, neon lights, rainy, wide angle |
| 三只橘猫在屋顶上晒太阳，Studio Ghibli 风格 | three orange cats sunbathing on a roof, Studio Ghibli style |

## 场景 D：文案生成

**翻译侧重**：翻译意图与受众，但保留品牌名、产品名、口号原文。

**子规则**：
- D1 品牌名/产品名保留原文：`云小宝`, `飞书`, `Notion` 不译
- D2 受众特征译出：`宝妈` → `young mothers`, `中小企业主` → `SME owners`
- D3 行业术语保留英语：`ROI`, `SaaS`, `B2B`, `GMV` 不译
- D4 译出"文案类型"：`slogan` → `slogan`, `产品介绍` → `product description`

**示例**：
| 输入 | 英语锚点 |
|---|---|
| 给我们的产品'云小宝'写一句slogan，面向宝妈群体 | write a slogan for our product '云小宝', targeting young mothers |
| 写一篇飞书的产品介绍，给中小企业主看 | write a product description for 飞书, for SME owners |
| 帮我想3个B2B SaaS的slogan | brainstorm 3 slogans for B2B SaaS |

## 场景 E：Agent 搭建 / 自动化

**翻译侧重**：翻译任务描述，但保留工具名、参数键、API 端点。

**子规则**：
- E1 工具名保留原文：`sendEmail`, `createTask`, `fetchWeather` 不译
- E2 参数键保留原文：`to`, `subject`, `apiKey` 不译
- E3 API 端点保留原文：`/api/v1/users` 不译
- E4 指令动词保留英语：`搜索` → `search`, `发送` → `send`, `创建` → `create`
- E5 时间表达式译为英语：`每天早上8点` → `every day at 8am`

**示例**：
| 输入 | 英语锚点 |
|---|---|
| 每天早上8点用 sendEmail 工具给团队发昨日报告 | every day at 8am use the sendEmail tool to send yesterday's report to the team |
| 监听 /api/v1/orders 端点，有新订单就调 createInvoice | listen to /api/v1/orders endpoint, call createInvoice on new order |
| 每周一9点搜索 GitHub trending 并创建任务 | every Monday at 9am search GitHub trending and create a task |

## 场景自动判定建议

当 `--scenario auto` 时，按以下线索判定：

| 输入特征 | 判定场景 |
|---|---|
| 含代码块/文件路径/报错信息 | code |
| 含"画/生成/设计图片" + 视觉描述词 | image |
| 含"slogan/文案/介绍/推文" + 品牌/产品名 | copy |
| 含工具名 + 时间/触发条件 | agent |
| 其他 | dialog |
