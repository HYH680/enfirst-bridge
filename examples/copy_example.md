# 场景：文案生成

## 示例 1：含品牌名

**用户输入**（中文）：
> 给我们的产品'云小宝'写一句 slogan，面向宝妈群体

**Enfirst Bridge 流程**：
1. 语种检测：zh → 触发桥
2. 场景判定：copy（含 slogan + 品牌名）
3. 直线翻译锚点：`write a slogan for our product '云小宝', targeting young mothers`
   - D1：品牌名 `云小宝` 保留原文
   - D2：受众 `宝妈` → `young mothers`
4. 主推理：模型用英语理解"为产品云小宝写面向年轻母亲的 slogan"
5. 输出（中文 slogan）：
   > 云小宝，妈妈的贴心小帮手。

## 示例 2：含行业术语

**用户输入**：
> 写一篇飞书的产品介绍，给中小企业主看，强调 ROI 提升

**锚点**：`write a product description for 飞书, for SME owners, emphasize ROI improvement`
- D1：`飞书` 保留
- D2：`中小企业主` → `SME owners`
- D3：`ROI` 保留

## 示例 3：多语言口号

**用户输入**：
> 帮我想 3 个 B2B SaaS 的 slogan

**锚点**：`brainstorm 3 slogans for B2B SaaS`
- R5：`3 个` → `3`
- D3：`B2B SaaS` 保留

## 关键点

- 品牌名、产品名、口号原文保留（不译，因为它们是品牌资产）
- 受众特征译出（宝妈 → young mothers）
- 行业术语保留英语（ROI, SaaS, B2B, GMV）
- 译出"文案类型"（slogan, 产品介绍, 推文）
