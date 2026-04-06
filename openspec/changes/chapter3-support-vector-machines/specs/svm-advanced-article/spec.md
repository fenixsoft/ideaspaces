## ADDED Requirements

### Requirement: 文章包含SMO算法思想讲解

文章 SHALL 包含SMO（序列最小优化）算法的核心思想介绍。

#### Scenario: SMO分解优化思想讲解
- **WHEN** 读者学习SMO部分
- **THEN** 读者理解为何分解优化、每次只优化两个变量的原因

#### Scenario: SMO迭代流程讲解
- **WHEN** 读者学习SMO流程
- **THEN** 读者理解SMO的基本迭代步骤（不深入实现细节）

### Requirement: 文章包含SVR回归思想讲解

文章 SHALL 包含支持向量回归（SVR）的核心思想介绍。

#### Scenario: SVR与SVM对比讲解
- **WHEN** 读者学习SVR部分
- **THEN** 读者理解SVR如何将间隔思想应用于回归问题

#### Scenario: SVR损失函数讲解
- **WHEN** 读者学习SVR损失部分
- **THEN** 读者理解ε-不敏感损失函数的定义和意义

### Requirement: 文章包含多分类扩展讲解

文章 SHALL 包含SVM多分类问题的扩展方法介绍。

#### Scenario: 一对多方法讲解
- **WHEN** 读者学习一对多部分
- **THEN** 读者理解如何将二分类SVM扩展为多分类

#### Scenario: 一对一方法讲解
- **WHEN** 读者学习一对一部分
- **THEN** 读者理解一对一方法的原理和区别

### Requirement: 文章包含与深度学习对比

文章 SHALL 包含SVM与深度学习的对比分析。

#### Scenario: 对比说明SVM价值
- **WHEN** 读者阅读对比部分
- **THEN** 读者理解SVM在小样本、理论保证、可解释性方面的优势

#### Scenario: 对比说明SVM局限
- **WHEN** 读者阅读对比部分
- **THEN** 读者理解SVM在大数据、特征自动学习方面的局限