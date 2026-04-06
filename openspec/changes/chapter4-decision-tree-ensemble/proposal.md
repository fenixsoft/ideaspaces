## Why

作为"经典统计学习方法"系列的第四章，决策树与集成方法展示了从单一模型到群体智慧的演进。对于已掌握统计学习基础的IT程序员读者，需要系统介绍决策树算法、Bagging（随机森林）、Boosting（AdaBoost、GBDT）等核心内容，建立"集成学习"的完整思维框架。

## What Changes

新增3篇文章，构成"决策树与集成"章节：

1. **《决策树——从数据学习规则》**
   - 引言小节：规则学习的直观性
   - ID3、C4.5、CART算法原理
   - 信息增益、增益率、Gini指数
   - NumPy实现：手写决策树
   - 应用场景示例

2. **《随机森林——Bagging的艺术》**
   - Bagging思想（bootstrap、聚合）
   - 随机森林原理（特征随机、投票）
   - 特征重要性评估
   - NumPy实现：手写随机森林
   - 应用场景示例

3. **《Boosting——从弱到强的迭代提升》**
   - Boosting思想（加权训练、序列学习）
   - AdaBoost原理与实现
   - GBDT核心思想（残差拟合）
   - NumPy实现：手写AdaBoost
   - 与深度学习对比：集成方法在深度时代的位置

## Capabilities

### New Capabilities

- `decision-tree-article`: 决策树原理、ID3/C4.5/CART算法、分裂准则、NumPy实现
- `random-forest-article`: Bagging思想、随机森林原理、特征重要性、NumPy实现
- `boosting-article`: Boosting思想、AdaBoost原理、GBDT思想、NumPy实现、与深度学习对比

### Modified Capabilities

无

## Impact

- 新增文档目录：`docs/statistical-learning/decision-tree-ensemble/`
- 新增归档目录：`articles/archive/2026-04-XX-decision-tree-ensemble/`
- 前置知识依赖：`docs/probability/`（熵、信息论基础）