## ADDED Requirements

### Requirement: 文章包含引言小节

文章 SHALL 包含引言小节作为第一个章节，建立"没有标签时如何学习"的思维框架。

#### Scenario: 引言建立无监督思维
- **WHEN** 读者阅读引言小节
- **THEN** 读者理解无监督学习的核心挑战：没有标签如何发现数据结构

### Requirement: 文章包含K-means原理讲解

文章 SHALL 包含K-means算法的完整原理，包括目标函数、迭代流程、收敛条件。

#### Scenario: K-means目标函数讲解清晰
- **WHEN** 读者学习目标函数部分
- **THEN** 读者理解K-means的优化目标：最小化簇内距离平方和

#### Scenario: K-means迭代流程讲解完整
- **WHEN** 读者学习迭代流程部分
- **THEN** 读者理解分配步骤和更新步骤的交替执行过程

#### Scenario: K-means收敛条件讲解
- **WHEN** 读者学习收敛部分
- **THEN** 读者理解算法何时停止迭代、可能收敛到局部最优的问题

### Requirement: 文章包含层次聚类思想讲解

文章 SHALL 包含层次聚类的基本思想介绍，包括凝聚式和分裂式方法。

#### Scenario: 凝聚式聚类思想讲解
- **WHEN** 读者学习凝聚式部分
- **THEN** 读者理解从单点逐步合并簇的过程

#### Scenario: 层次聚类可视化（树状图）
- **WHEN** 读者学习树状图部分
- **THEN** 读者理解如何用树状图表示聚类层次结构

### Requirement: 文章包含NumPy手写实现

文章 SHALL 包含K-means的NumPy手写实现代码。

#### Scenario: K-means实现可运行
- **WHEN** 读者执行K-means代码
- **THEN** 代码能完成聚类任务并输出聚类结果

#### Scenario: 实现展示迭代过程
- **WHEN** 读者阅读代码
- **THEN** 代码清晰展示初始化、分配、更新、收敛判断过程

### Requirement: 文章包含应用场景示例

文章 SHALL 包含聚类的具体应用示例。

#### Scenario: 应用场景具体可行
- **WHEN** 读者阅读应用场景部分
- **THEN** 场景示例能展示聚类在客户分群、异常检测等领域的应用