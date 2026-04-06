## Why

作为"经典统计学习方法"系列的第五章，无监督学习展示在没有标签时如何发现数据的内在结构。对于已掌握统计学习基础的IT程序员读者，需要系统介绍聚类（K-means、层次聚类）、降维（PCA、LDA）等核心内容，建立"无标签学习"的思维框架，并说明无监督方法在深度学习时代的发展（如自监督学习）。

## What Changes

新增3篇文章，构成"无监督学习"章节：

1. **《聚类——发现数据的自然分组》**
   - 引言小节：没有标签时如何学习
   - K-means原理与算法流程
   - 层次聚类思想
   - NumPy实现：手写K-means
   - 应用场景示例

2. **《降维——压缩数据的维度空间》**
   - PCA原理（方差最大化、协方差矩阵）
   - LDA（线性判别分析）思想
   - NumPy实现：手写PCA
   - 应用场景：数据可视化、特征压缩

3. **《无监督学习进阶》**
   - 聚类评估指标（轮廓系数、Calinski-Harabasz）
   - K-means++初始化改进
   - 聚类与降维的综合应用
   - 与深度学习对比：无监督方法在深度时代的位置

## Capabilities

### New Capabilities

- `clustering-article`: K-means原理、层次聚类思想、NumPy实现、应用场景
- `dimensionality-reduction-article`: PCA原理、LDA思想、NumPy实现、可视化应用
- `unsupervised-advanced-article`: 聚类评估、K-means++改进、综合应用、与深度学习对比

### Modified Capabilities

无

## Impact

- 新增文档目录：`docs/statistical-learning/unsupervised-learning/`
- 新增归档目录：`articles/archive/2026-04-XX-unsupervised-learning/`
- 前置知识依赖：`docs/linear/`（矩阵分解）、`docs/probability/`（分布概念）