# Volume Mount 执行规范

## ADDED Requirements

### Requirement: 开发环境默认启用 Volume Mount

系统 SHALL 在开发环境默认使用 Volume Mount 挂载共享模块，实现代码实时更新无需重建镜像。

#### Scenario: 创建容器时挂载共享模块

- **WHEN** 创建沙箱容器执行代码
- **AND** 环境变量 `MOUNT_SHARED_MODULES` 不等于 `false`
- **THEN** 容器配置包含 Binds 挂载共享模块目录
- **AND** 挂载目标为 Python site-packages 路径

#### Scenario: 禁用 Volume Mount

- **WHEN** 环境变量 `MOUNT_SHARED_MODULES=false`
- **THEN** 容器不挂载共享模块目录
- **AND** 依赖镜像内已 COPY 的模块（如有）

### Requirement: 只读挂载确保安全

系统 SHALL 以只读模式挂载共享模块目录，防止容器内代码修改宿主机文件。

#### Scenario: 验证只读挂载

- **WHEN** 共享模块被挂载到容器
- **THEN** 挂载选项包含 `:ro`（read-only）
- **AND** 容器内尝试修改模块文件时返回错误

### Requirement: 正确解析项目根目录

系统 SHALL 自动解析项目根目录，生成正确的挂载源路径。

#### Scenario: 自动解析项目根目录

- **WHEN** 启动沙箱服务
- **THEN** 系统自动检测项目根目录
- **AND** 挂载路径为 `{projectRoot}/local-server/shared_modules`

#### Scenario: 环境变量覆盖根目录

- **WHEN** 环境变量 `SHARED_MODULES_PATH` 被设置
- **THEN** 使用该路径作为挂载源
- **AND** 打印日志提示使用了自定义路径

### Requirement: 挂载失败时的友好提示

系统 SHALL 在挂载失败时提供清晰的错误提示。

#### Scenario: 共享模块目录不存在

- **WHEN** `shared_modules/` 目录不存在
- **THEN** 启动时打印警告日志
- **AND** 提示运行提取脚本或检查路径配置