## ADDED Requirements

### Requirement: 中英文自动添加空格

系统 SHALL 在中文汉字与半角字母数字之间自动添加一个空格。

**字符范围定义**:
- 中文汉字: `\u4e00-\u9fff`（CJK统一汉字，不含标点符号）
- 半角字符: 英文字母 A-Z、a-z 和数字 0-9

**规则**:
- 汉字 + 半角字符 → 汉字 空格 半角字符
- 半角字符 + 汉字 → 半角字符 空格 汉字
- 已有空格的不再添加（避免重复）

#### Scenario: 中文后接英文
- **WHEN** 文本内容为 "K-means目标函数"
- **THEN** 输出为 "K-means 目标函数"

#### Scenario: 英文后接中文
- **WHEN** 文本内容为 "使用Sigmoid函数"
- **THEN** 输出为 "使用 Sigmoid 函数"

#### Scenario: 已有空格不重复
- **WHEN** 文本内容为 "中文 English 中文"
- **THEN** 输出为 "中文 English 中文"（保持原样）

#### Scenario: 中文标点不处理
- **WHEN** 文本内容为 "线性模型，如OLS"
- **THEN** 输出为 "线性模型，如 OLS"（逗号后空格，逗号前不处理）

### Requirement: 全角引号替换

系统 SHALL 将全角双引号替换为半角双引号。

#### Scenario: 全角引号替换
- **WHEN** 文本内容包含 "中文内容"
- **THEN** 输出为 "中文内容"

#### Scenario: 代码块内不替换
- **WHEN** 代码块内包含 "print("hello")"
- **THEN** 代码块内容保持不变

### Requirement: 加粗格式统一

系统 SHALL 将 "**中文概念（English Name）**" 格式统一为 "**中文概念**（English Name）"。

#### Scenario: 全角括号加粗统一
- **WHEN** 文本内容为 "**无监督学习（Unsupervised Learning）**"
- **THEN** 输出为 "**无监督学习**（Unsupervised Learning）"

#### Scenario: 半角括号加粗统一
- **WHEN** 文本内容为 "**决策树(Decision Tree)**"
- **THEN** 输出为 "**决策树**(Decision Tree)"

#### Scenario: 无英文括号不处理
- **WHEN** 文本内容为 "**损失对概率的导数**"
- **THEN** 输出保持不变（无英文括号）

#### Scenario: 包含公式不处理
- **WHEN** 文本内容为 "**值域 $(0,1)$**"
- **THEN** 输出保持不变（括号内包含公式）

### Requirement: 排除区域保护

系统 SHALL 保护以下区域不被处理：
- 公式块（`$$...$$`）
- 行内公式（`$...$`）
- 代码块（` ```...``` `）
- 行内代码（`...`）
- Frontmatter（`---...---`）

#### Scenario: 公式块不处理
- **WHEN** 文本包含 `$$\sum_{i=1}^{n} x_i$$`
- **THEN** 公式内容保持不变

#### Scenario: 代码块不处理
- **WHEN** 文本包含 `` ```python\nprint("hello")\n``` ``'
- **THEN** 代码块内容保持不变

#### Scenario: 行内代码不处理
- **WHEN** 文本包含 "`KMeans(n_clusters=3)`"
- **THEN** 行内代码内容保持不变

### Requirement: 检查模式

系统 SHALL 提供检查模式，输出差异报告而不修改文件。

#### Scenario: 检查模式输出
- **WHEN** 使用 `--check` 参数运行脚本
- **THEN** 输出每个需要修改的位置和修正建议，文件内容不变

### Requirement: 修复模式

系统 SHALL 提供修复模式，自动修正并写入文件。

#### Scenario: 修复模式执行
- **WHEN** 使用 `--fix` 参数运行脚本
- **THEN** 自动修正所有格式问题并写入原文件

### Requirement: 目录排除

系统 SHALL 排除 `.vuepress/` 目录下的文件。

#### Scenario: VuePress目录排除
- **WHEN** 扫描 docs 目录
- **THEN** 不处理 docs/.vuepress/ 下的任何文件