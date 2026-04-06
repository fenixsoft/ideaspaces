---
title: 决策树与集成——从单一模型到群体智慧
---

# 决策树与集成——从单一模型到群体智慧

本章节介绍决策树算法及其集成方法，展示"群体智慧"如何提升模型性能。

## 章节内容

- [决策树——从数据学习规则](./01-decision-tree.md)
  - 分裂准则（信息增益、Gini指数）
  - ID3、C4.5、CART算法
  - 手写CART实现

- [随机森林——Bagging的艺术](./02-random-forest.md)
  - Bootstrap采样与聚合
  - 特征随机性
  - 特征重要性评估

- [Boosting——从弱到强的迭代提升](./03-boosting.md)
  - AdaBoost原理
  - GBDT核心思想
  - 与深度学习对比

## 前置知识

- [概率统计](/probability/introduction)：熵、信息论基础
- [线性模型](/statistical-learning/linear-models/)：分类器基础

## 学习目标

完成本章节后，你将能够：

1. 理解决策树的分裂准则和构建过程
2. 掌握Bagging和Boosting的核心思想
3. 实现简化的决策树和随机森林
4. 理解集成方法在工业界的应用价值
5. 理解集成方法与深度学习的对比