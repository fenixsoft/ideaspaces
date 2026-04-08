# 共享模块规范

## ADDED Requirements

### Requirement: 按章节组织的共享模块目录结构

系统 SHALL 在 `local-server/shared_modules/` 目录下按章节组织可复用的 Python 类定义，目录结构与文档结构对应。

#### Scenario: 查看共享模块目录结构

- **WHEN** 检查 `local-server/shared_modules/` 目录
- **THEN** 存在按章节划分的子目录：`linear/`、`bayesian/`、`svm/`、`tree/`、`unsupervised/`
- **AND** 每个子目录包含 `__init__.py` 文件

### Requirement: 从文档提取标记的类定义

系统 SHALL 通过提取脚本从文档中提取标记为 `extract-class="ClassName"` 的类定义，并写入共享模块目录。

#### Scenario: 提取单个类定义

- **WHEN** 文档包含 `extract-class="LogisticRegression"` 标记
- **THEN** 提取脚本提取 `class LogisticRegression:` 的完整定义
- **AND** 根据文档路径写入对应模块文件

#### Scenario: 自动识别类结束位置

- **WHEN** 提取类定义时
- **THEN** 系统通过 AST 分析或缩进检测正确识别类结束位置
- **AND** 不包含类定义后的立即执行代码

### Requirement: 文档路径到模块路径的自动映射

系统 SHALL 根据文档所在路径自动确定目标模块路径。

#### Scenario: 线性模型文档映射

- **WHEN** 文档位于 `docs/statistical-learning/linear-models/`
- **THEN** 提取的类定义写入 `shared_modules/linear/`

#### Scenario: 贝叶斯方法文档映射

- **WHEN** 文档位于 `docs/statistical-learning/bayesian-methods/`
- **THEN** 提取的类定义写入 `shared_modules/bayesian/`

### Requirement: 共享模块可被沙箱代码导入

系统 SHALL 确保共享模块挂载到沙箱容器的 Python 路径中，可通过标准 import 语法使用。

#### Scenario: 导入共享模块中的类

- **WHEN** 代码块执行 `from shared.linear.logistic_regression import LogisticRegression`
- **THEN** 成功导入类定义
- **AND** 可正常实例化和使用该类

### Requirement: 模块命名规范

系统 SHALL 遵循以下模块命名规范：
- 目录名使用小写下划线（如 `linear_models` → `linear`）
- 文件名使用下划线分隔（如 `logistic_regression.py`）
- 类名使用 PascalCase（如 `LogisticRegression`）

#### Scenario: 导入路径示例

- **WHEN** 用户需要使用 `LogisticRegression` 类
- **THEN** 导入路径为 `from shared.linear.logistic_regression import LogisticRegression`