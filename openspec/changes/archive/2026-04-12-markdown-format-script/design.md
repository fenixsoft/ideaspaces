## Context

项目中 docs 目录包含 35+ 个 Markdown 文件，涵盖数学基础和统计学习内容。这些文档中存在中英文排版格式不一致的问题：
- 中英文之间缺少空格（如 "K-means目标函数"）
- 全角引号混用（"..." 与 "..."）
- 加粗格式不规范（如 "**概念（English）**" 包含英文在加粗范围内）

项目已有 Node.js 脚本传统（`scripts/extract-shared-modules.js`），采用 ES Module 格式，使用 fs 模块进行文件操作。

## Goals / Non-Goals

**Goals:**
- 创建格式化脚本，自动处理中英文空格、引号替换、加粗格式统一
- 智能排除公式块、代码块、frontmatter 等特殊区域
- 提供检查模式（只报告）和修复模式（自动修正）
- 集成到 npm scripts，方便日常使用

**Non-Goals:**
- 不处理文件名，只处理内容
- 不处理 .vuepress/ 目录下的文件
- 不处理 HTML 标签内的内容
- 不引入新的 npm 依赖包（如 pangu.js、textlint）

## Decisions

### D1: 使用正则表达式而非 AST 解析

**选择**: 使用正则表达式进行文本匹配和替换

**理由**:
- 项目不需要引入 markdown-it 等解析器依赖
- 正则方案足够处理当前的边界情况
- 与现有脚本风格一致（`extract-shared-modules.js` 也使用正则）
- 实现简单，维护成本低

**替代方案**:
- 使用 markdown-it 解析 AST → 过重依赖，边界情况处理复杂
- 使用 pangu.js → 不处理代码块/公式，需二次封装

### D2: 占位符策略处理排除区域

**选择**: 使用唯一占位符替换排除区域，处理后还原

**理由**:
- 避免复杂的嵌套正则匹配
- 保证排除区域内容不被意外修改
- 实现简单可靠

**占位符格式**:
```
$$公式块$$ → {{MATH_BLOCK_0}}
$行内公式$ → {{MATH_INLINE_0}}
```代码块``` → {{CODE_BLOCK_0}}
`行内代码` → {{CODE_INLINE_0}}
```

### D3: 检查模式输出格式

**选择**: 输出差异报告，显示原文 → 修正后的文本

**理由**:
- 用户可以预览所有修改
- 便于确认修改是否符合预期
- 与 prettier、eslint 等工具风格一致

### D4: npm scripts 命令设计

**选择**:
```json
{
  "format:md": "node scripts/format-markdown.js",
  "format:md:check": "node scripts/format-markdown.js --check",
  "format:md:fix": "node scripts/format-markdown.js --fix"
}
```

**理由**:
- `format:md` 默认检查模式，安全第一
- `:check` 和 `:fix` 后缀明确语义
- 与项目现有 `cdn:refresh` 命名风格一致

## Risks / Trade-offs

### R1: 正则边界情况遗漏
**风险**: 复杂嵌套场景可能遗漏处理
**缓解**: 充分测试现有文档，建立测试用例库

### R2: 意外修改公式/代码内容
**风险**: 占位符还原失败导致内容损坏
**缓解**: 每个占位符使用唯一索引，还原时严格匹配

### R3: 已有空格重复添加
**风险**: "中文 English 中文" 可能变成 "中文  English  中文"
**缓解**: 添加空格前检查前后是否已有空白字符

## Open Questions

无待解决的问题。