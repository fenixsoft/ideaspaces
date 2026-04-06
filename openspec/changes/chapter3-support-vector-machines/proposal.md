## Why

作为"经典统计学习方法"系列的第三章，支持向量机（SVM）是核方法的代表，曾在2000年代占据机器学习主流地位。对于已掌握线性代数（向量空间）和微积分（优化理论）的IT程序员读者，需要系统介绍最大间隔原理、核技巧、SMO算法等核心内容，建立几何直觉与优化方法的结合。

## What Changes

新增3篇文章，构成"支持向量机"章节：

1. **《SVM基础——最大间隔分类的艺术》**
   - 引言小节：从几何直觉到最优分类
   - 最大间隔原理（几何间隔、支持向量）
   - 软间隔与松弛变量
   - NumPy实现：硬间隔SVM（简化版）
   - 应用场景示例

2. **《核技巧——非线性问题的线性解法》**
   - 核函数原理（特征空间映射、核技巧）
   - 常见核函数（线性核、多项式核、RBF核）
   - NumPy实现：核SVM
   - 应用场景：非线性分类

3. **《SVM进阶——优化与扩展》**
   - SMO算法思想（分解优化）
   - SVM用于回归（SVR思想）
   - 多分类扩展
   - 与深度学习对比：SVM在深度时代的位置

## Capabilities

### New Capabilities

- `svm-max-margin-article`: 最大间隔原理、几何间隔、支持向量、软间隔、NumPy实现
- `kernel-methods-article`: 核函数原理、核技巧、常见核函数、NumPy实现、非线性分类应用
- `svm-advanced-article`: SMO算法思想、SVR回归、多分类扩展、与深度学习对比

### Modified Capabilities

无

## Impact

- 新增文档目录：`docs/statistical-learning/support-vector-machines/`
- 新增归档目录：`articles/archive/2026-04-XX-support-vector-machines/`
- 前置知识依赖：`docs/linear/`（向量空间）、`docs/calculus/`（拉格朗日乘数）