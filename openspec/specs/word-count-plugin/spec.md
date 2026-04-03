## ADDED Requirements

### Requirement: 构建时计算文章字数

系统 SHALL 在 VuePress 构建过程中计算每篇文章的字数。

字数计算通过 VuePress 插件的 `onInitialized` 钩子实现，计算结果存入 `$page.wordCount`。

#### Scenario: 有内容的文章
- **WHEN** 文章 Markdown 内容不为空
- **THEN** `$page.wordCount` 包含计算后的字数

#### Scenario: 无内容的文章
- **WHEN** 文章 Markdown 内容为空或仅包含 frontmatter
- **THEN** `$page.wordCount` 为 0

---

### Requirement: 字数统计支持中英文混合

系统 SHALL 正确统计中英文混合内容的字数。

统计算法：
1. 预处理 Markdown 内容（移除语法标记，保留实际内容）
2. 将空白符（空格、换行、全角空格）替换为占位符
3. 英文字符（ASCII）标记为单词单位，连续英文视为一个单词
4. 中文字符按单个字符计数
5. 移除占位符后计算总长度

#### Scenario: 纯中文文章
- **WHEN** 文章内容为纯中文（如"线性代数是机器学习的语言"）
- **THEN** 每个汉字计为 1 字，上述示例应返回 10

#### Scenario: 纯英文文章
- **WHEN** 文章内容为纯英文（如"Linear algebra is the language of ML"）
- **THEN** 连续英文单词计为单词数，上述示例应返回 7（7 个单词）

#### Scenario: 中英文混合文章
- **WHEN** 文章内容包含中英文混合（如"理解 Vector 和 Matrix 是 ML 的基础"）
- **THEN** 中文按字符计，英文按单词计

---

### Requirement: 字数统计包含代码和公式内容

系统 SHALL 在统计字数时包含代码块和 LaTeX 公式的实际内容。

统计规则如下：

| 内容类型 | 处理方式 | 示例 |
|---------|---------|------|
| 代码块 `\`\`\`...\`\`\`` | 移除语法标记，保留代码内容 | `print("hello")` 计入字数 |
| 行内代码 `\`...\`` | 移除 `\` 符号，保留内容 | `numpy` 计入字数 |
| 行内公式 `$...$` | 移除 `$` 符号，保留公式内容 | `E[X]` 计入字数 |
| 块级公式 `$$...$$` | 移除 `$$` 符号，保留公式内容 | `f(x) = x^2` 计入字数 |

#### Scenario: 包含代码块的文章
- **WHEN** 文章包含代码块（如 Python 示例代码）
- **THEN** 代码块内的代码内容计入字数，语法标记不计入

#### Scenario: 包含数学公式的文章
- **WHEN** 文章包含 LaTeX 公式（如 `$\mathbf{v} = (3, 2)$`）
- **THEN** 公式符号（如 `\mathbf{v}` 和 `(3, 2)`）计入字数，`$` 标记不计入

---

### Requirement: 字数统计排除链接图片等非文字内容

系统 SHALL 在统计字数时排除以下非文字内容：

| 内容类型 | 处理方式 |
|---------|---------|
| 图片 `![...](...)` | 完全不计入 |
| HTML 标签 `<tagname>...</tagname>` | 完全不计入（仅匹配字母开头的真正标签） |
| Frontmatter (YAML头部) | 完全不计入 |
| Markdown 标题标记 `#` | 移除标记，保留标题文字 |
| Markdown 粗体/斜体标记 | 移除标记，保留文字 |
| 链接 `[文字](url)` | 保留显示文字，移除 URL |

**重要**：HTML 标签正则表达式必须只匹配真正的 HTML 标签（如 `<details>`、`<summary>`），不能匹配数学符号 `<` 和 `>`。正则应为 `/<[a-zA-Z\/][^>]*>/g`。

#### Scenario: 包含图片的文章
- **WHEN** 文章包含图片（如 `![正态分布图](./assets/pdf.png)`）
- **THEN** 图片不计入字数，alt 文字也不计入

#### Scenario: 包含链接的文章
- **WHEN** 文章包含链接（如 `[引言](introduction.md)`）
- **THEN** 链接显示文字（如"引言"）计入字数，URL 不计入

---

### Requirement: 字数统计在构建时计算

系统 SHALL 在 VuePress 构建过程中计算字数，而非每次页面访问时计算。

计算时机：VuePress 插件的 `onInitialized` 钩子，遍历所有页面并计算字数。

数据存储：
- 临时文件：`docs/.vuepress/.temp/word-count/data.js`
- 数据结构：`{path: {title, wordCount}}`

#### Scenario: 构建时计算
- **WHEN** 执行 `npm run build`
- **THEN** 所有页面的字数被计算并写入临时文件

#### Scenario: 页面访问时读取
- **WHEN** 用户访问文章页面
- **THEN** 前端组件从已构建的数据中读取字数，不重新计算

---

### Requirement: 字数统计插件数据结构

系统 SHALL 通过插件提供字数统计数据供前端组件使用。

数据结构：
- `page.data.wordCount`: 当前页面的字数
- `page.data.readingTime.words`: 当前页面的字数（同 wordCount）
- `page.data.readingTime.minutes`: 预计阅读时间（字数 / 500）
- `page.data.readingTime.globalWords`: 所有页面的字数映射表

前端组件可通过 `usePageData()` 获取 `page.value.wordCount`。