# 共享模块与 Volume Mount 方案

## Why

文档中多个 runnable code 块需要复用类定义（如 `LogisticRegression`），但每个代码块在独立的 Docker 容器中执行，状态完全隔离，导致第二个代码块无法使用第一个代码块定义的类。当前解决方案是将类定义复制到每个代码块，造成代码冗余和维护困难。同时，每次修改代码都需要重建 Docker 镜像，开发效率低下。

## What Changes

- **新增共享模块目录**：`local-server/shared_modules/`，按章节组织可复用的 Python 类定义
- **新增提取脚本**：从文档中自动提取标记的类定义，同步到共享模块
- **新增标记语法**：`extract-class="ClassName"` 标记需要提取的类定义
- **修改容器配置**：使用 Volume Mount 挂载共享模块，无需每次重建镜像
- **修改示例文档**：`logistic-regression.md` 作为首个应用案例

## Capabilities

### New Capabilities

- `shared-modules`: 可复用的 Python 类定义模块，按章节组织，支持从文档自动提取和同步
- `volume-mount-execution`: 开发环境下通过 Volume Mount 挂载共享模块，实现代码实时更新无需重建镜像

### Modified Capabilities

- `sandbox-execution`: 执行环境新增共享模块挂载能力，容器内可通过 `from shared.xxx import Yyy` 导入预定义类

## Impact

**新增文件：**
- `local-server/shared_modules/__init__.py`
- `local-server/shared_modules/linear/__init__.py`
- `local-server/shared_modules/linear/logistic_regression.py`（自动生成）
- `scripts/extract-shared-modules.js`

**修改文件：**
- `local-server/src/sandbox.js` - 添加 Volume Mount 配置
- `docs/statistical-learning/linear-models/logistic-regression.md` - 添加标记语法，第二个代码块改用 import

**工作流变更：**
- 开发阶段：修改文档 → 运行提取脚本 → 直接测试（无需重建镜像）
- 生产阶段：可选择 Volume Mount 或 COPY 到镜像