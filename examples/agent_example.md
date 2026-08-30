# 场景：Agent 搭建 / 自动化

## 示例 1：定时任务

**用户输入**（中文）：
> 每天早上8点用 sendEmail 工具给团队发昨日报告

**Enfirst Bridge 流程**：
1. 语种检测：zh → 触发桥
2. 场景判定：agent（含工具名 sendEmail + 时间"每天早上8点"）
3. 直线翻译锚点：`every day at 8am use the sendEmail tool to send yesterday's report to the team`
   - E1：`sendEmail` 工具名保留
   - E4：指令动词 `发` → `send`
   - E5：`每天早上8点` → `every day at 8am`
4. 主推理：模型理解"创建一个每日 8am 的定时任务，调 sendEmail 发报告"
5. 调用 automation_update 创建自动化：
   - rrule: `FREQ=DAILY;BYHOUR=8;BYMINUTE=0`
   - prompt: 锚点（或中文重新表述）

## 示例 2：事件监听

**用户输入**：
> 监听 /api/v1/orders 端点，有新订单就调 createInvoice

**锚点**：`listen to /api/v1/orders endpoint, call createInvoice on new order`
- E1：`createInvoice` 工具名保留
- E3：`/api/v1/orders` 端点保留

## 示例 3：周期+搜索+任务

**用户输入**：
> 每周一9点搜索 GitHub trending 并创建任务

**锚点**：`every Monday at 9am search GitHub trending and create a task`
- E4：`搜索` → `search`, `创建` → `create`
- E5：`每周一9点` → `every Monday at 9am`

## 关键点

- 工具名、参数键、API 端点保留原文
- 指令动词保留为英语（search, send, create, listen）
- 时间表达式译为英语（every day at 8am, every Monday at 9am）
- 翻译后的锚点可直接作为 automation prompt 的内部表示
