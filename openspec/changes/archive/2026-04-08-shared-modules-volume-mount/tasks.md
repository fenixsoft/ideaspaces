# 实现任务清单

## 1. 创建共享模块目录结构

- [x] 1.1 创建 `local-server/shared_modules/__init__.py`
- [x] 1.2 创建 `local-server/shared_modules/linear/__init__.py`
- [x] 1.3 创建其他章节子目录的 `__init__.py`（bayesian、svm、tree、unsupervised）

## 2. 实现提取脚本

- [x] 2.1 创建 `scripts/extract-shared-modules.js` 脚本文件
- [x] 2.2 实现扫描文档目录查找 `extract-class` 标记的功能
- [x] 2.3 实现提取类定义的核心逻辑（AST 或缩进分析）
- [x] 2.4 实现文档路径到模块路径的映射逻辑
- [x] 2.5 实现写入共享模块文件的功能
- [x] 2.6 在 `package.json` 中添加 `extract:shared` 脚本命令（手动执行）
- [x] 2.7 修改 `npm run build:sandbox`，在 docker build 前自动执行提取脚本

## 3. 修改沙箱配置支持 Volume Mount

- [x] 3.1 在 `local-server/src/sandbox.js` 中添加项目根目录解析逻辑
- [x] 3.2 在容器配置中添加 `HostConfig.Binds` 挂载配置
- [x] 3.3 添加环境变量 `MOUNT_SHARED_MODULES` 支持
- [x] 3.4 添加环境变量 `SHARED_MODULES_PATH` 覆盖支持
- [x] 3.5 添加挂载路径日志输出和错误提示

## 4. 修改示例文档（logistic-regression.md）

- [x] 4.1 在第一个代码块的 `runnable` 标记后添加 `extract-class="LogisticRegression"`
- [x] 4.2 运行提取脚本生成 `shared_modules/linear/logistic_regression.py`
- [x] 4.3 修改第二个代码块，移除类定义前的演示代码，添加 `from shared.linear.logistic_regression import LogisticRegression`
- [x] 4.4 验证两个代码块都能正常执行

## 5. 测试与文档

- [x] 5.1 测试 Volume Mount 在开发环境正常工作
- [x] 5.2 测试 `MOUNT_SHARED_MODULES=false` 时禁用挂载
- [x] 5.3 更新 `CLAUDE.md` 或相关文档说明共享模块使用方式