# 共享模块与 Volume Mount 技术设计

## Context

当前 runnable code 插件在每个代码块执行时创建独立的 Docker 容器，容器之间完全隔离，无状态共享。这导致：

1. **代码复用困难**：第一个代码块定义的类，第二个代码块无法使用
2. **开发效率低**：修改 Python 代码需要重建 Docker 镜像（分钟级）

现有架构：
```
文档代码块 → 前端 → API Server → Docker 容器（独立、无共享）→ 执行 → 销毁
```

约束条件：
- 文档是类定义的"主源"，需要保留完整的教学代码
- 需要在多个文档间复用类定义
- 开发阶段需要快速迭代，不能每次都重建镜像

## Goals / Non-Goals

**Goals:**
- 实现跨代码块的类定义复用
- 保持文档作为代码主源，写作体验不变
- 开发阶段代码修改无需重建镜像（秒级生效）
- 提供自动化工具同步文档代码和共享模块

**Non-Goals:**
- 不实现 Kernel 持久化（会话级状态保持）
- 不实现复杂的依赖声明语法（`depends-on` 等）
- 不处理跨章节的类继承关系

## Decisions

### 决策 1: 共享模块目录位置

**选择**：`local-server/shared_modules/`

**理由**：
- 与 `kernel_runner.py` 同级，构建逻辑一致
- 语义清晰：沙箱专用的共享模块
- 独立于 Node.js 服务代码（`src/`）

**替代方案**：
- `src/shared_modules/` - 与 Node.js 代码混淆
- 项目根目录 `shared_modules/` - 顶层目录过多

### 决策 2: 模块组织方式

**选择**：按章节扁平化组织

```
shared_modules/
├── __init__.py
├── linear/
│   ├── __init__.py
│   ├── logistic_regression.py
│   ├── linear_regression.py
│   └── regularization.py
├── bayesian/
├── svm/
├── tree/
└── unsupervised/
```

**理由**：
- 与文档结构对应，易于查找
- 两层目录结构适中
- 同章节相关类可合并（如 `RidgeRegression` + `LassoRegression`）

### 决策 3: 同步策略

**选择**：文档为主源 + 自动提取脚本

**语法标记**：
```python
# 文档中
```python runnable extract-class="LogisticRegression"
class LogisticRegression:
    ...
```

**提取规则**：
- 自动识别 `class ClassName:` 开始
- 通过 AST 或缩进分析识别类结束位置
- 根据文档路径自动映射到目标模块

**理由**：
- 保持文档写作体验
- 自动化减少手动错误
- 可在 CI/CD 中集成

### 决策 4: Volume Mount 实现方式

**选择**：开发环境默认启用，通过环境变量控制

```javascript
// sandbox.js
const useMount = process.env.MOUNT_SHARED_MODULES !== 'false'

if (useMount) {
  containerConfig.HostConfig.Binds = [
    `${projectRoot}/local-server/shared_modules:/usr/local/lib/python3.11/site-packages/shared:ro`
  ]
}
```

**理由**：
- 开发环境默认挂载，实时生效
- 生产环境可通过环境变量禁用，使用 COPY
- 只读挂载更安全

**Dockerfile 修改**：
- 开发环境：移除 COPY 指令，依赖挂载
- 生产环境：保留 COPY 作为 fallback

## Risks / Trade-offs

### 风险 1: 挂载路径在不同环境可能不一致

**风险**：Windows/Mac/Linux 路径格式差异，或项目根目录获取失败

**缓解措施**：
- 使用 `path.resolve()` 处理路径
- 提供环境变量 `SHARED_MODULES_PATH` 作为 override
- 启动时检测并打印挂载路径

### 风险 2: 类定义提取边界识别错误

**风险**：复杂类定义（嵌套类、多行字符串）可能提取不完整

**缓解措施**：
- 使用 Python AST 解析而非正则，提高准确性
- 提取后运行语法检查验证
- 提供手动 override 语法：`extract-end` 标记

### 风险 3: 开发与生产环境行为不一致

**风险**：Volume Mount 在某些云平台不支持

**缓解措施**：
- Dockerfile 保留 COPY 作为 fallback
- 提供环境检测脚本验证挂载是否生效
- 文档明确说明两种模式差异

## Migration Plan

### 阶段 1: 基础设施搭建
1. 创建 `shared_modules/` 目录结构
2. 实现提取脚本 `scripts/extract-shared-modules.js`
3. 修改 `sandbox.js` 添加 Volume Mount

### 阶段 2: 示例文档改造
1. 修改 `logistic-regression.md` 添加标记语法
2. 第二个代码块改用 import
3. 验证执行正常

### 阶段 3: 扩展应用
1. 用户自行添加其他文档的标记
2. 运行提取脚本生成全部共享模块

### 回滚策略
- 移除 Volume Mount 配置
- 删除 `shared_modules/` 目录
- 恢复文档中代码块为原始复制模式

## Open Questions

1. **提取脚本触发时机**：
   - **手动执行**：`npm run extract:shared` - 开发时按需手动运行
   - **构建时自动执行**：`npm run build:sandbox` 在 docker build 前自动运行提取脚本
   - 实现方式：在 package.json 的 build:sandbox 命令中添加预执行步骤

2. **类定义更新时文档如何同步**：如果修改了共享模块，如何反向同步到文档？
   - 当前设计：文档是主源，不支持反向同步
   - 修改流程：改文档 → 重新提取