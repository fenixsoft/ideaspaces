## Why

作为"经典统计学习方法"系列的第一章，线性模型是统计学习的基石。对于已掌握线性代数、微积分、概率统计的IT程序员读者，需要系统介绍线性回归、逻辑回归、正则化方法等核心内容，建立从数学基础到机器学习算法的桥梁，并说明这些方法在深度学习时代的价值与局限。

## What Changes

新增3篇文章，构成"线性模型"章节：

1. **《线性回归——从OLS到闭式解》**
   - 引言：线性假设的力量与局限
   - OLS原理推导（损失函数、闭式解）
   - NumPy实现：手写线性回归
   - 应用场景示例

2. **《逻辑回归——分类问题的概率解法》**
   - Sigmoid与交叉熵损失
   - 概率解释与多分类扩展
   - NumPy实现：手写逻辑回归
   - 应用场景示例

3. **《正则化与广义线性模型》**
   - 过拟合问题与正则化思想
   - 岭回归、Lasso原理与实现
   - GLM框架：连接函数与分布族
   - NumPy实现：正则化线性模型
   - 与深度学习对比：线性模型在深度时代的位置

## Capabilities

### New Capabilities

- `linear-regression-article`: 线性回归原理推导、OLS闭式解、NumPy手写实现、应用场景
- `logistic-regression-article`: 逻辑回归原理、Sigmoid函数、交叉熵损失、多分类扩展、NumPy实现
- `regularization-article`: 正则化思想、岭回归与Lasso、GLM框架、与深度学习对比

### Modified Capabilities

无

## Impact

- 新增文档目录：`docs/statistical-learning/linear-models/`
- 新增归档目录：`articles/archive/2026-04-XX-linear-models/`
- 更新 VuePress 配置以包含新章节导航
- 前置知识依赖：`docs/linear/`、`docs/calculus/`、`docs/probability/`