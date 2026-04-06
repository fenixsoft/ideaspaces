## Why

作为"经典统计学习方法"系列的第二章，贝叶斯方法将前置概率统计知识转化为具体的机器学习实践。对于已掌握贝叶斯定理、条件概率等概念的IT程序员读者，需要系统介绍朴素贝叶斯分类器、贝叶斯网络、EM算法等核心内容，建立概率性思维在机器学习中的具体应用能力。

## What Changes

新增3篇文章，构成"贝叶斯方法"章节：

1. **《朴素贝叶斯——最简单的概率分类器》**
   - 引言小节：贝叶斯思维在机器学习中的实践
   - 条件独立性假设与推导
   - NumPy实现：手写朴素贝叶斯
   - 应用场景：文本分类

2. **《贝叶斯网络——建模变量间的依赖关系》**
   - 贝叶斯网络结构（DAG、条件概率表）
   - 推断方法（精确推断、近似推断思想）
   - NumPy实现：简单贝叶斯网络
   - 应用场景示例

3. **《EM算法——隐变量模型的参数估计》**
   - 隐变量问题与EM思想
   - EM算法推导（E步、M步、收敛性）
   - GMM（高斯混合模型）原理
   - NumPy实现：手写GMM
   - 与深度学习对比：贝叶斯方法在深度时代的位置

## Capabilities

### New Capabilities

- `naive-bayes-article`: 朴素贝叶斯原理、条件独立性假设、NumPy手写实现、文本分类应用
- `bayesian-network-article`: 贝叶斯网络结构、DAG与条件概率表、推断方法、NumPy实现
- `em-algorithm-article`: EM算法原理、E步M步推导、GMM模型、NumPy实现、与深度学习对比

### Modified Capabilities

无

## Impact

- 新增文档目录：`docs/statistical-learning/bayesian-methods/`
- 新增归档目录：`articles/archive/2026-04-XX-bayesian-methods/`
- 前置知识依赖：`docs/probability/`（贝叶斯定理、条件概率）