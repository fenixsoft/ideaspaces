## ADDED Requirements

### Requirement: 文章页面底部显示评论区

系统 SHALL 在每篇文章页面底部显示 GitHub Issues 评论区组件。

评论区组件位于文章内容下方、ArticleFooter 组件之后。

组件显示内容包括：
- 标题区域：💬 讨论 + 评论数量徽章 + "在 GitHub 上查看"链接
- 登录提示/评论输入区域
- 评论列表区域

#### Scenario: 文章有关联 Issue
- **WHEN** 文章 frontmatter 包含有效的 `issue.number` 字段
- **THEN** 评论区组件显示该 Issue 的所有评论
- **AND** 提供"在 GitHub 上查看"链接指向该 Issue

#### Scenario: 文章无关联 Issue
- **WHEN** 文章 frontmatter 不包含 `issue.number` 字段
- **THEN** 评论区组件显示空状态或加载提示
- **AND** 提供"在 GitHub 上查看"链接指向仓库 Issues 列表

#### Scenario: 评论加载失败
- **WHEN** GitHub API 请求失败（限流或网络错误）
- **THEN** 显示错误提示和"在 GitHub 上查看讨论"备用链接

---

### Requirement: 用户登录后可发表评论

系统 SHALL 支持 GitHub OAuth 登录，登录用户可在页面内发表评论。

未登录用户显示"使用 GitHub 登录参与讨论"按钮。

已登录用户显示 Markdown 输入框和"发表评论"按钮。

#### Scenario: 未登录用户点击登录
- **WHEN** 未登录用户点击"使用 GitHub 登录"按钮
- **THEN** 重定向到 GitHub OAuth 授权页面
- **AND** 授权成功后返回原页面并存储 token

#### Scenario: 已登录用户发表评论
- **WHEN** 已登录用户在输入框输入内容并点击"发表评论"
- **THEN** 评论通过 GitHub API 发布到关联的 Issue
- **AND** 评论列表自动刷新显示新评论

#### Scenario: 无 OAuth 配置时的降级
- **WHEN** 系统未配置 GitHub OAuth Client ID
- **THEN** 点击登录按钮直接跳转到 GitHub Issue 页面

---

### Requirement: 评论数据多层缓存

系统 SHALL 实现多层缓存机制减少 GitHub API 请求次数。

缓存层级：
- 第一层：内存缓存（Session），TTL 30 秒
- 第二层：localStorage 缓存，TTL 5 分钟
- 数据源：GitHub API（带 ETag 条件请求）

#### Scenario: 内存缓存命中
- **WHEN** 30 秒内重复请求同一 Issue 的评论
- **THEN** 使用内存缓存数据，不发起 API 请求

#### Scenario: localStorage 缓存命中
- **WHEN** 5 分钟内重复请求同一 Issue 的评论
- **THEN** 使用 localStorage 缓存数据，不发起 API 请求

#### Scenario: ETag 条件请求
- **WHEN** 缓存过期但存在 ETag
- **THEN** 发送 `If-None-Match` 头部
- **AND** 若返回 304 Not Modified 则使用缓存数据

---

### Requirement: 评论区懒加载

系统 SHALL 使用 IntersectionObserver 实现评论区懒加载。

仅当用户滚动到评论区附近（rootMargin: 100px）时才加载评论数据。

#### Scenario: 评论区进入视口
- **WHEN** 用户滚动页面使评论区组件进入视口附近 100px
- **THEN** 触发评论数据加载
- **AND** 断开 IntersectionObserver 观察

#### Scenario: 页面加载时评论区已在视口
- **WHEN** 页面初始加载时评论区已可见
- **THEN** 立即触发评论数据加载