## ADDED Requirements

### Requirement: 创建 Issue 后回写编号到文章 frontmatter

系统 SHALL 在成功创建 GitHub Issue 后，自动更新文章 Markdown 文件的 frontmatter，添加 `issue.number` 字段。

#### Scenario: 新文章创建 Issue
- **WHEN** sync-issues.js 为新文章创建 GitHub Issue
- **THEN** 文章 frontmatter 添加 `issue.number: <新创建的编号>`
- **AND** frontmatter 保持其他字段不变

#### Scenario: Issue 创建失败不回写
- **WHEN** GitHub Issue 创建请求失败
- **THEN** 不修改文章 frontmatter
- **AND** 记录错误日志

---

### Requirement: 搜索已存在 Issue 并回写编号

系统 SHALL 在创建 Issue 前搜索已存在的同名 Issue，若找到则回写编号而不重复创建。

搜索条件：标题匹配 `[Comments] {文章标题}` 且标签包含 `comments`。

#### Scenario: 找到已存在的 Issue
- **WHEN** 搜索到标题匹配且标签正确的 Issue
- **THEN** 回写该 Issue 编号到文章 frontmatter
- **AND** 不创建新 Issue

#### Scenario: 未找到 Issue 创建新的
- **WHEN** 搜索结果为空
- **THEN** 创建新 Issue 并回写编号

#### Scenario: 文章已有 issue.number 跳过
- **WHEN** 文章 frontmatter 已包含 `issue.number` 字段
- **THEN** 跳过该文章的处理
- **AND** 输出日志显示 "已存在 Issue #N"

---

### Requirement: Issue 命名约定

系统 SHALL 按约定格式创建 Issue：

- 标题格式：`[Comments] {文章标题}`
- 标签：`comments`, `article`
- 内容模板：包含文章标题和欢迎讨论的提示

#### Scenario: Issue 标题格式正确
- **WHEN** 创建新 Issue
- **THEN** 标题为 `[Comments] {文章的实际标题}`

#### Scenario: Issue 标签正确
- **WHEN** 创建新 Issue
- **THEN** Issue 自动添加 `comments` 和 `article` 标签

---

### Requirement: 跳过特定类型的文件

系统 SHALL 跳过以下类型的 Markdown 文件：

- README.md（目录索引页）
- design.md（设计文档）

#### Scenario: 遇到 README.md 文件
- **WHEN** sync-issues.js 扫描到 README.md 文件
- **THEN** 跳过该文件，不创建 Issue

#### Scenario: 遇到 design.md 文件
- **WHEN** sync-issues.js 扫描到 design.md 文件
- **THEN** 跳过该文件，不创建 Issue

#### Scenario: 文章缺少 title 字段
- **WHEN** Markdown 文件 frontmatter 不包含 title 字段
- **THEN** 跳过该文件，不创建 Issue