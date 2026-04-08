# 沙箱执行功能规范（变更）

## ADDED Requirements

### Requirement: 容器支持 Volume Mount 挂载外部模块

系统 SHALL 支持通过 Volume Mount 将宿主机的共享模块目录挂载到容器内的 Python site-packages 路径。

#### Scenario: 挂载共享模块目录

- **WHEN** 创建沙箱容器
- **AND** `MOUNT_SHARED_MODULES` 未设置为 `false`
- **THEN** 容器 `HostConfig.Binds` 包含共享模块目录的挂载配置
- **AND** 挂载目标为 `/usr/local/lib/python3.11/site-packages/shared`

#### Scenario: 容器内导入共享模块

- **WHEN** 代码执行 `from shared.linear.logistic_regression import LogisticRegression`
- **THEN** Python 成功导入模块
- **AND** 类可正常实例化使用

### Requirement: 开发与生产环境配置切换

系统 SHALL 通过环境变量支持开发环境（Volume Mount）和生产环境（COPY 到镜像）的切换。

#### Scenario: 开发环境使用 Volume Mount

- **WHEN** `MOUNT_SHARED_MODULES=true` 或未设置（默认）
- **THEN** 使用 Volume Mount 方式
- **AND** 代码修改立即生效无需重建镜像

#### Scenario: 生产环境使用镜像内模块

- **WHEN** `MOUNT_SHARED_MODULES=false`
- **THEN** 不使用 Volume Mount
- **AND** 依赖 Dockerfile 中 COPY 的共享模块