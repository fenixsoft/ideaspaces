## Why

设计文档规划了完整的 GitHub Issues 评论系统，但当前实现存在断裂：评论组件已开发完成却未集成到页面、插件未注册、Issue 创建后编号未回写到文章 frontmatter。导致用户无法在页面上看到或参与讨论，违背了"系统构建时自动生成 GitHub Issues 作为留言讨论"的设计初衷。

## What Changes

- **集成评论组件到页面布局**：在 Layout.vue 的 `#page-content-bottom` slot 中添加 Comments 组件
- **注册评论插件到 VuePress 配置**：在 config.js 中注册 commentsPlugin，传入仓库信息和 OAuth 配置
- **完善 Issue 同步脚本回写逻辑**：sync-issues.js 创建 Issue 后自动更新文章 frontmatter 的 issue.number 字段
- **补充现有文章的 issue 字段**：为已发布的文章添加 issue 编号关联

## Capabilities

### New Capabilities

- `article-comments`: 文章评论功能，允许用户在文章页面底部查看和发表 GitHub Issues 评论

### Modified Capabilities

- `issue-sync`: Issue 同步功能需求变更，从"仅创建 Issue"改为"创建 Issue 并回写编号到文章 frontmatter"

## Impact

**代码影响**：
- `docs/.vuepress/theme/layouts/Layout.vue` - 添加 Comments 组件
- `docs/.vuepress/config.js` - 注册 commentsPlugin
- `scripts/sync-issues.js` - 添加 frontmatter 回写逻辑
- `docs/**/*.md` - 补充 issue.number 字段

**依赖影响**：
- 无新增外部依赖
- 需要 GitHub OAuth Client ID 配置（可选，用于登录发表评论）

**API 影响**：
- 无 API 变更，纯前端集成

**用户体验影响**：
- 文章页面底部将显示评论区
- 用户可查看现有评论
- 登录 GitHub 后可发表评论