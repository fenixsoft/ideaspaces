---
name: writer-republish
description: 从归档中恢复文章，编辑后重新发布到文档目录。用于更新已发布的文章。
license: MIT
compatibility: None
metadata:
  author: ideaspaces
  version: "1.0"
---

从归档中恢复文章，编辑后重新发布。

**输入**: 文章名称（可选，从归档列表选择）

**输出**: 更新后的发布目录，归档目录中的新版本

---

## 使用场景

- 已发布的文章需要修正错误
- 已发布的文章需要添加新内容
- 已发布的文章需要更新代码示例

---

## 步骤

### 1. 列出归档文章

检查 `articles/archive/` 目录：
```bash
ls -la articles/archive/
```

如果指定了文章名称，直接定位。否则显示列表让用户选择。

### 2. 检查当前发布状态

读取归档目录中的 `.article.yaml`：
- 确认 `status: published`
- 记录 `publishedDate`
- 记录 `path`（发布路径）

### 3. 选择操作模式

使用 AskUserQuestion 询问用户要执行的操作：

**选项 A: 恢复到工作区编辑**
- 将归档目录复制回 `articles/{name}/`
- 更新状态为 `status: editing`
- 用户可以运行 `/writer:compose` 进行编辑

**选项 B: 直接修改发布版本**
- 保持归档不变
- 直接编辑 `docs/{article-name}/` 中的文件
- 完成后同步更新归档

**选项 C: 完全重新发布**
- 删除当前发布目录
- 从归档恢复到工作区
- 重新执行完整发布流程

### 4. 执行选定操作

#### 选项 A: 恢复到工作区

```bash
# 复制归档到工作区
cp -r articles/archive/{date}-{name} articles/{name}

# 更新状态
# 编辑 .article.yaml: status: editing
```

显示提示：
```
文章已恢复到工作区: articles/{name}/

下一步：
1. 编辑章节文件或大纲
2. 运行 /writer:compose 进行校审
3. 运行 /writer:publish 重新发布
```

#### 选项 B: 直接修改

```bash
# 进入发布目录
cd docs/{article-name}/

# 用户可以编辑任何文件
```

编辑完成后：
```bash
# 同步到归档
cp docs/{article-name}/*.md articles/archive/{date}-{name}/draft/chapters/
```

#### 选项 C: 完全重新发布

```bash
# 1. 备份当前发布（可选）
mv docs/{article-name} docs/{article-name}.bak

# 2. 恢复到工作区
cp -r articles/archive/{date}-{name} articles/{name}

# 3. 更新状态为 editing
```

然后提示用户：
```
文章已恢复到工作区。

下一步：
1. 运行 /writer:compose 编辑和校审
2. 运行 /writer:publish 重新发布
```

### 5. 更新版本信息

无论哪种操作，完成后更新 `.article.yaml`：

```yaml
status: published  # 或 editing
updated: {YYYY-MM-DD}
version: {递增版本号，如 1.1}
changeLog:
  - date: {YYYY-MM-DD}
    changes: "{变更描述}"
```

---

## 输出示例

### 选择操作

```
## 归档文章：linear-algebra-vectors-matrices

**标题**: 向量与矩阵运算基础
**发布日期**: 2026-03-26
**版本**: 1.0
**归档位置**: articles/archive/2026-03-26-linear-algebra-vectors-matrices/
**发布位置**: docs/linear-algebra-vectors-matrices/

请选择操作：
A. 恢复到工作区编辑（推荐用于大改动）
B. 直接修改发布版本（推荐用于小修正）
C. 完全重新发布（删除当前版本）
```

### 恢复成功

```
## 文章已恢复到工作区

**文章**: linear-algebra-vectors-matrices
**工作目录**: articles/linear-algebra-vectors-matrices/
**状态**: editing

**章节文件**:
- draft/chapters/01-introduction.md
- draft/chapters/02-vectors.md
- draft/chapters/03-matrices.md
- draft/chapters/04-numpy.md
- draft/chapters/05-applications.md
- draft/chapters/06-summary.md
- draft/experiments.md

**下一步**:
1. 编辑需要修改的文件
2. 运行 `/writer:compose` 进行校审
3. 运行 `/writer:publish` 重新发布
```

### 直接修改模式

```
## 进入直接修改模式

**发布目录**: docs/linear-algebra-vectors-matrices/

您可以：
- 直接编辑任何 .md 文件
- 修改完成后告知我，我会同步到归档

**注意**: 此模式不会触发校审流程，请自行确保内容正确。
```

---

## Guardrails

- 归档目录不会被删除，只复制
- 直接修改模式跳过校审，需要用户自行确保质量
- 版本号递增，保留变更历史
- 如果文章在 `articles/` 中已存在（非归档），询问用户如何处理
- 发布目录的旧版本在重新发布前会备份（可选）