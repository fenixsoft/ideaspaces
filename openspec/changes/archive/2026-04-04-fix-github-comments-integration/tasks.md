## 1. 插件注册与配置

- [x] 1.1 在 config.js 中导入 commentsPlugin
- [x] 1.2 在 plugins 数组中注册 commentsPlugin，配置 repo 参数
- [x] 1.3 验证插件全局变量 __COMMENTS_REPO__ 正常注入

## 2. 评论组件集成到页面

- [x] 2.1 在 Layout.vue 的 `#page-content-bottom` slot 中添加 Comments 组件
- [x] 2.2 传入 repo 和 clientId props 到 Comments 组件
- [x] 2.3 调整 ArticleFooter 和 Comments 的样式间距
- [x] 2.4 启动开发服务器验证评论区显示正常

## 3. Issue 同步脚本完善

- [x] 3.1 实现 frontmatter 解析和修改函数
- [x] 3.2 在 createIssue 成功后调用 frontmatter 修改函数回写编号
- [x] 3.3 实现 searchIssue 函数搜索已存在的 Issue
- [x] 3.4 修改主流程：先搜索，找到则回写，未找到则创建并回写
- [x] 3.5 添加错误处理：Issue 创建失败不回写，回写失败记录警告
- [x] 3.6 运行 npm run sync:issues 测试脚本功能

## 4. 验证与测试

- [x] 4.1 检查文章页面评论区加载正常（有 issue.number 的文章）
- [x] 4.2 检查文章页面评论区降级显示（无 issue.number 的文章）
- [x] 4.3 验证多层缓存机制生效（内存缓存、localStorage 缓存）
- [x] 4.4 验证懒加载机制生效（IntersectionObserver）
- [x] 4.5 构建生产版本 npm run build 验证无编译错误
- [x] 4.6 本地模式 npm run local 验证完整功能