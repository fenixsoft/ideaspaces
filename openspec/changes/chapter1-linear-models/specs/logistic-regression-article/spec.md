## ADDED Requirements

### Requirement: 文章包含Sigmoid与交叉熵讲解

文章 SHALL 包含Sigmoid函数的数学定义和性质，以及交叉熵损失函数的推导与解释。

#### Scenario: Sigmoid函数讲解完整
- **WHEN** 读者学习Sigmoid部分
- **THEN** 读者理解Sigmoid的数学定义、导数性质、概率解释

#### Scenario: 交叉熵损失推导清晰
- **WHEN** 读者学习交叉熵部分
- **THEN** 读者能从最大似然估计推导出交叉熵损失函数

### Requirement: 文章包含概率解释与多分类扩展

文章 SHALL 包含逻辑回归的概率解释（为何输出是概率），以及多分类问题的扩展方法（如softmax）。

#### Scenario: 概率解释建立直觉
- **WHEN** 读者学习概率解释部分
- **THEN** 读者理解逻辑回归输出为何代表概率，而非简单分类

#### Scenario: 多分类扩展讲解清晰
- **WHEN** 读者学习多分类部分
- **THEN** 读者理解softmax回归如何扩展二分类逻辑回归

### Requirement: 文章包含NumPy手写实现

文章 SHALL 包含逻辑回归的NumPy手写实现代码，包括梯度下降优化过程。

#### Scenario: 实现包含完整训练流程
- **WHEN** 读者执行NumPy实现代码
- **THEN** 代码包含初始化、梯度计算、参数更新、迭代优化完整流程

#### Scenario: 实现对应数学推导
- **WHEN** 读者对照数学推导和代码实现
- **THEN** 代码结构与公式推导步骤对应清晰

### Requirement: 文章包含应用场景示例

文章 SHALL 包含至少一个具体应用场景示例，说明逻辑回归的实际应用价值。

#### Scenario: 应用场景适合分类问题
- **WHEN** 读者阅读应用场景部分
- **THEN** 场景为典型分类问题（如二分类或多分类）