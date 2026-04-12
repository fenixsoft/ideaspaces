## Why

docs 目录下的 Markdown 文件存在中英文排版格式不一致的问题：
1. 中文与英文字母/数字之间缺少空格，影响阅读体验（如 "K-means目标函数" 应为 "K-means 目标函数")
2. 全角双引号（""）使用不统一，部分文档混用全角和半角引号
3. 概念名词的加粗格式不规范，如 "**中文概念（English Name）**" 应为 "**中文概念**（English Name）"

这些排版问题不仅影响文档的视觉一致性，也降低了专业文档的可读性。现在需要创建一个自动化格式化脚本来统一解决这些问题，避免手动逐文件修正的繁琐工作。

## What Changes

- 新增 Markdown 格式化脚本（Node.js），用于自动处理 docs 目录下的 Markdown 文件
- 实现中英文自动添加空格功能（汉字与英文字母/数字之间）
- 实现全角双引号替换为半角引号功能
- 实现加粗格式统一功能（将 "**中文（English）**" 改为 "**中文**（English）"）
- 提供检查模式（只报告问题，不修改文件）和修复模式（自动修正）
- 集成到 npm scripts，支持 `npm run format:md:check` 和 `npm run format:md:fix`
- 智能排除：公式块（$$）、代码块（```）、行内代码（`）、frontmatter（---）

## Capabilities

### New Capabilities

- `markdown-format`: Markdown 文件格式化能力，包括中英文空格添加、引号替换、加粗格式统一

### Modified Capabilities

无现有能力需要修改。

## Impact

- **新增文件**: `scripts/format-markdown.js`
- **修改文件**: `package.json`（新增 npm scripts）
- **影响范围**: `docs/` 目录下所有 `.md` 文件（排除 `.vuepress/` 目录）
- **无破坏性变更**: 所有修改仅涉及排版格式，不影响文档内容语义