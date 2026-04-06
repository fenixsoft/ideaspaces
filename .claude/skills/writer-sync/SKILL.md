---
name: writer:sync
description: 将docs目录下被修改过的文章同步回articles/archive目录。只同步修改内容，不修改docs目录。
license: MIT
compatibility: None
metadata:
  author: ideaspaces
  version: "1.0"
---

将docs目录下被修改过的文章同步回articles/archive目录。

**输入**: 无（自动检测所有已发布的文章）

**输出**: 更新后的archive目录，版本信息更新

---

## 使用场景

- 在docs目录直接修改了已发布的文章后，需要同步回归档
- 保持archive与docs的一致性
- 记录文章版本历史

---

## 核心原则

**只读docs目录，只写archive目录**：
- 本skill不修改docs目录下的任何文件
- 只将docs中的修改复制到archive
- 保持docs为权威来源，archive为备份记录

---

## 步骤

### 1. 扫描已发布文章

从articles/archive目录获取所有已发布的文章列表：

```bash
ls articles/archive/
```

读取每个归档目录的 `.article.yaml`，确认 `status: published` 并获取 `path`（docs路径）。

### 2. 检测修改

对每个已发布文章，检测docs目录是否被修改：

**检测方法 A（推荐）：Git状态检测**
```bash
# 检查docs目录下的修改状态
git status docs/{article-name}/
```

如果有 `modified` 状态的文件，说明文章被修改过。

**检测方法 B：内容比较**
```bash
# 比较docs和archive中的章节文件
diff docs/{article-name}/{chapter}.md articles/archive/{date}-{name}/draft/chapters/{chapter}.md
```

或者使用md5校验：
```bash
md5sum docs/{article-name}/*.md
md5sum articles/archive/{date}-{name}/draft/chapters/*.md
```

### 3. 列出修改清单

汇总所有被修改的文章，显示修改详情：

```
## 检测到的修改

### 文章: linear-algebra-vectors-matrices
**归档位置**: articles/archive/2026-03-26-linear-algebra-vectors-matrices/
**发布位置**: docs/linear-algebra-vectors-matrices/

修改的文件:
- introduction.md (内容变更)
- vectors.md (内容变更)

### 文章: calculus-series-01
**归档位置**: articles/archive/2026-04-01-calculus-series/
**发布位置**: docs/calculus-series/01-limits.md

修改的文件:
- 01-limits.md (内容变更)
```

### 4. 用户确认

使用 AskUserQuestion 确认同步操作：

```
检测到 2 篇文章有修改，共 4 个文件需要同步。

是否执行同步？
- 是，同步所有修改（推荐）
- 否，跳过本次操作
- 选择性同步（手动选择）
```

### 5. 执行同步

对于每个需要同步的文章：

**同步章节文件**：
```bash
# 注意：archive中的文件可能有编号前缀，需要匹配
# docs/introduction.md -> archive/draft/chapters/introduction.md 或 01-introduction.md

# 匹配规则：
# - 如果archive中有编号前缀的文件，去掉前缀后匹配docs文件名
# - 例如：archive的 01-introduction.md 对应 docs的 introduction.md
```

**具体操作**：
1. 读取archive中的draft/chapters目录，获取文件列表
2. 对于docs中的每个.md文件（排除README.md）：
   - 去掉docs文件名可能的编号前缀（如果有）
   - 在archive中查找对应文件（匹配去掉编号前缀后的名称）
   - 如果找到，复制docs内容到archive文件
   - 如果找不到，说明是新增文件，添加到archive

**同步资源文件**（如果docs有新增assets）：
```bash
# 复制docs中新增的assets到archive
cp -r docs/{article-name}/assets/* articles/archive/{date}-{name}/draft/assets/ 2>/dev/null || true
```

### 6. 更新版本信息

同步完成后，更新每个被修改文章的 `.article.yaml`：

```yaml
# 更新版本和变更记录
updated: {YYYY-MM-DD}
version: {递增版本号}
changeLog:
  - date: {YYYY-MM-DD}
    changes: "从docs同步修改内容"
    files:
      - {文件名1}
      - {文件名2}
```

### 7. 验证同步结果

检查同步后的文件是否一致：
```bash
# 验证内容一致性
diff docs/{article-name}/{file}.md articles/archive/{date}-{name}/draft/chapters/{matched-file}.md
```

确保输出为空（内容一致）。

---

## 文件名匹配规则

docs和archive中的文件名可能不同：

| docs文件名 | archive文件名 | 匹配方式 |
|------------|---------------|----------|
| introduction.md | 01-introduction.md | 去掉编号前缀匹配 |
| vectors.md | 02-vectors.md | 去掉编号前缀匹配 |
| experiments.md | experiments.md | 直接匹配 |

匹配算法：
```javascript
// 匹配逻辑
function matchFiles(docsFile, archiveFiles) {
  // 去掉docs文件可能的编号前缀
  const docsBase = docsFile.replace(/^\d+-/, '');

  // 在archive中查找匹配文件
  for (const archiveFile of archiveFiles) {
    const archiveBase = archiveFile.replace(/^\d+-/, '');
    if (docsBase === archiveBase) {
      return archiveFile;
    }
  }

  return null; // 未找到匹配
}
```

---

## 输出示例

### 检测阶段

```
## 文章修改检测

扫描 3 篇已发布文章，检测修改状态...

### linear-algebra-vectors-matrices
- 状态: 有修改
- 修改文件: introduction.md, vectors.md

### calculus-series
- 状态: 无修改

### probability
- 状态: 有修改
- 修改文件: 01-basics.md

---

共检测到 2 篇文章有修改，需要同步 3 个文件。
```

### 同步完成

```
## 同步完成

### linear-algebra-vectors-matrices
- 已同步: introduction.md → draft/chapters/01-introduction.md
- 已同步: vectors.md → draft/chapters/02-vectors.md
- 版本更新: 1.1 → 1.2
- 更新时间: 2026-04-06

### probability
- 已同步: 01-basics.md → draft/chapters/01-basics.md
- 版本更新: 1.0 → 1.1
- 更新时间: 2026-04-06

---

验证结果: 所有文件内容一致 ✅
```

---

## Guardrails

- **只读docs目录**：绝不修改docs目录下的任何文件
- **保持docs权威**：docs是最新版本，archive是备份
- **保留编号前缀**：archive中保留原有的编号前缀格式
- **版本递增**：每次同步都要更新版本号和changelog
- **完整性验证**：同步后验证内容一致性
- **README.md不同步**：docs的README.md是发布入口，通常不同步到archive
- **资源同步可选**：如果有新增assets资源，同步到archive