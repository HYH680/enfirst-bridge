# 场景：图片生成

## 示例 1：含风格名

**用户输入**（中文）：
> 画一个穿汉服的女孩在樱花树下读书，水彩风格

**Enfirst Bridge 流程**：
1. 语种检测：zh → 触发桥
2. 场景判定：image（含"画"+"水彩风格"）
3. 直线翻译锚点：`a girl in hanfu reading under cherry blossom tree, watercolor style`
   - R4：风格关键词保留英语；`hanfu` 保留原文
   - C1：输出为逗号分隔关键词串，可直接喂给 ImageGen
4. 调用 ImageGen，prompt = 锚点
5. 输出：生成的图片

## 示例 2：赛博朋克

**用户输入**：
> 赛博朋克城市夜景，霓虹灯，雨天，广角

**锚点**：`cyberpunk city night, neon lights, rainy, wide angle`
- `cyberpunk` 保留原文

## 示例 3：含艺术家名

**用户输入**：
> 三只橘猫在屋顶上晒太阳，Studio Ghibli 风格

**锚点**：`three orange cats sunbathing on a roof, Studio Ghibli style`
- R5：`三只` → `three`
- R4：`Studio Ghibli` 保留原文

## 关键点

- 输出格式为逗号分隔的关键词串（不是完整句子），可直接作为 image prompt
- 风格名、艺术家名保留原文
- 构图词、光影词译为英语（close-up, backlit, soft lighting）
- 量化描述保留数字
