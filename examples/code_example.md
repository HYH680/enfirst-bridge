# 场景：代码编程

## 示例 1：含函数名

**用户输入**（中文）：
> 在 handleSubmit 里加一个表单校验，邮箱不能为空

**Enfirst Bridge 流程**：
1. 语种检测：zh → 触发桥
2. 场景判定：code（含函数名 handleSubmit）
3. 直线翻译锚点：`add form validation in handleSubmit, email cannot be empty`
   - R2 规则：`handleSubmit` 标识符不译，原样保留
4. 主推理：模型理解"在 handleSubmit 函数中添加邮箱非空校验"
5. 输出（中文）：
   > 在 handleSubmit 函数里加一段：
   > ```js
   > if (!values.email) { ... }
   > ```

## 示例 2：含文件路径

**用户输入**：
> 把 src/utils/auth.ts 里的 token 刷新逻辑提出来

**锚点**：`extract the token refresh logic from src/utils/auth.ts`
- R2：`src/utils/auth.ts` 路径不译

## 示例 3：含错误信息

**用户输入**：
> 这个报错 TypeError: cannot read property 'x' of undefined 怎么解决

**锚点**：`how to fix this error TypeError: cannot read property 'x' of undefined`
- R2：报错信息原文保留

## 关键点

- 所有标识符（函数名、变量名、API名）原样保留
- 文件路径、错误信息原文不译
- 只翻译自然语言部分
- 技术术语（state, hook, promise）保留英语
