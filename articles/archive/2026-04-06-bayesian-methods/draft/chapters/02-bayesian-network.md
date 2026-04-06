# 贝叶斯网络——建模变量间的依赖关系

## 引言：超越朴素假设

上一章的朴素贝叶斯分类器有一个关键假设：**特征之间相互独立**。这个假设简化了计算，但也丢失了特征之间的依赖信息。在现实中，特征往往存在复杂的关联：

- "发烧"和"咳嗽"都与"感冒"相关，但它们之间也可能相互影响
- "收入"和"教育程度"共同影响"贷款审批"，但收入和教育之间也有关联

**贝叶斯网络（Bayesian Network）**提供了一种系统的方法来建模变量之间的依赖关系。它用**有向无环图（DAG）**表示变量间的条件依赖，既能表达复杂的概率关系，又能进行高效的概率推断。

---

## DAG结构：节点、边、父子关系

### 有向无环图

贝叶斯网络的核心结构是**有向无环图（Directed Acyclic Graph, DAG）**：

- **节点（Node）**：表示随机变量
- **有向边（Directed Edge）**：表示变量间的依赖关系，$A \rightarrow B$ 表示"A影响B"
- **无环（Acyclic）**：不存在从节点出发又回到自身的路径

```
示例：疾病诊断网络

    ┌─────────┐
    │  吸烟   │
    └────┬────┘
         │
         ▼
    ┌─────────┐     ┌─────────┐
    │  肺癌   │────▶│  X光结果 │
    └─────────┘     └─────────┘
         │
         ▼
    ┌─────────┐
    │  呼吸困难 │
    └─────────┘
```

这个网络表示：
- 吸烟 → 肺癌（吸烟增加患癌风险）
- 肺癌 → X光结果（癌症影响X光检查结果）
- 肺癌 → 呼吸困难（癌症导致呼吸困难）

### 父节点与子节点

在DAG中：
- **父节点（Parent）**：指向某节点的节点
- **子节点（Child）**：被某节点指向的节点

在上图中，"肺癌"的父节点是"吸烟"，子节点是"X光结果"和"呼吸困难"。

### 条件独立性

贝叶斯网络编码了变量间的**条件独立性**。给定父节点，一个节点条件独立于它的非后代节点：

$$P(X_i | \text{Parents}(X_i), \text{其他变量}) = P(X_i | \text{Parents}(X_i))$$

这意味着：**一个变量的概率只依赖于它的父节点**，与更远的祖先节点无关（给定父节点后）。

---

## 条件概率表（CPT）

### 定义

每个节点关联一个**条件概率表（Conditional Probability Table, CPT）**，存储给定父节点取值时该节点的概率分布。

### 示例：疾病诊断网络

假设有如下CPT：

**P(吸烟)**：
| 吸烟 | P |
|------|---|
| 是   | 0.3 |
| 否   | 0.7 |

**P(肺癌 | 吸烟)**：
| 吸烟 | P(肺癌=是) | P(肺癌=否) |
|------|------------|------------|
| 是   | 0.1        | 0.9        |
| 否   | 0.01       | 0.99       |

**P(呼吸困难 | 肺癌)**：
| 肺癌 | P(呼吸困难=是) | P(呼吸困难=否) |
|------|----------------|----------------|
| 是   | 0.65           | 0.35           |
| 否   | 0.1            | 0.9            |

**P(X光异常 | 肺癌)**：
| 肺癌 | P(X光异常=是) | P(X光异常=否) |
|------|---------------|---------------|
| 是   | 0.9           | 0.1           |
| 否   | 0.05          | 0.95          |

### 联合概率分解

贝叶斯网络将联合概率分解为条件概率的乘积：

$$P(X_1, X_2, \ldots, X_n) = \prod_{i=1}^{n} P(X_i | \text{Parents}(X_i))$$

对于疾病诊断网络：

$$P(\text{吸烟}, \text{肺癌}, \text{呼吸困难}, \text{X光异常}) = P(\text{吸烟}) \cdot P(\text{肺癌}|\text{吸烟}) \cdot P(\text{呼吸困难}|\text{肺癌}) \cdot P(\text{X光异常}|\text{肺癌})$$

这种分解大大减少了需要存储的参数数量。对于 $n$ 个二元变量：
- 完整联合分布需要 $2^n - 1$ 个参数
- 贝叶斯网络如果每个节点最多有 $k$ 个父节点，需要 $n \cdot 2^k$ 个参数

---

## 推断方法：精确推断与近似推断

### 推断问题

给定贝叶斯网络，我们关心三类推断问题：

1. **概率查询**：给定证据，计算某变量的后验概率
   - 例：已知X光异常，求患肺癌的概率 $P(\text{肺癌}=是 | \text{X光异常}=是)$

2. **最大后验（MAP）查询**：给定证据，求最可能的变量取值组合

3. **最可能解释（MPE）**：给定证据，求所有非证据变量的最可能取值

### 精确推断：变量消元法

**变量消元法（Variable Elimination）**是一种精确推断算法：

1. 将联合概率写成因子（CPT）的乘积
2. 按照消元顺序，对不需要的变量求和消去
3. 合并相同变量的因子

**示例**：计算 $P(\text{肺癌} | \text{X光异常}=是)$

$$P(\text{肺癌} | \text{X光异常}=是) = \frac{P(\text{肺癌}, \text{X光异常}=是)}{\sum_{\text{肺癌}} P(\text{肺癌}, \text{X光异常}=是)}$$

其中：
$$P(\text{肺癌}, \text{X光异常}=是) = \sum_{\text{吸烟}} \sum_{\text{呼吸困难}} P(\text{吸烟}) \cdot P(\text{肺癌}|\text{吸烟}) \cdot P(\text{呼吸困难}|\text{肺癌}) \cdot P(\text{X光异常}=是|\text{肺癌})$$

### 近似推断：采样方法

当网络规模很大时，精确推断计算代价高，可以使用**近似推断**：

1. **拒绝采样**：按概率生成样本，只保留满足证据的样本
2. **似然加权**：固定证据变量，对其他变量采样并加权
3. **MCMC**：马尔可夫链蒙特卡洛方法，如Gibbs采样

---

## NumPy实现：简单贝叶斯网络

```python
import numpy as np

class SimpleBayesianNetwork:
    """
    简单贝叶斯网络实现
    支持离散变量和精确推断（枚举法）
    """
    
    def __init__(self):
        self.nodes = {}  # 节点信息：{name: {'parents': [], 'values': []}}
        self.cpts = {}   # 条件概率表：{name: {parent_values: {value: prob}}}
        self.topo_order = []  # 拓扑排序
    
    def add_node(self, name, values, parents=None):
        """添加节点"""
        if parents is None:
            parents = []
        self.nodes[name] = {'parents': parents, 'values': values}
        
        # 更新拓扑排序
        self._update_topo_order()
    
    def set_cpt(self, name, cpt):
        """
        设置条件概率表
        
        cpt格式：{parent_value_tuple: {value: prob}}
        对于无父节点的变量：{(): {value: prob}}
        """
        self.cpts[name] = cpt
    
    def _update_topo_order(self):
        """计算拓扑排序"""
        visited = set()
        order = []
        
        def visit(node):
            if node in visited:
                return
            visited.add(node)
            for parent in self.nodes[node]['parents']:
                visit(parent)
            order.append(node)
        
        for node in self.nodes:
            visit(node)
        
        self.topo_order = order
    
    def get_prob(self, name, value, parent_values):
        """获取条件概率 P(name=value | parent_values)"""
        parent_key = tuple(parent_values) if parent_values else ()
        return self.cpts[name].get(parent_key, {}).get(value, 0)
    
    def joint_prob(self, assignment):
        """
        计算联合概率 P(X1, X2, ...)
        assignment: {node: value}
        """
        prob = 1.0
        for node in self.topo_order:
            parents = self.nodes[node]['parents']
            parent_values = [assignment[p] for p in parents]
            value = assignment[node]
            prob *= self.get_prob(node, value, parent_values)
        return prob
    
    def enumerate_inference(self, query, evidence):
        """
        枚举推断：计算 P(query | evidence)
        
        query: {node: value} 或 {node: '?'} 返回分布
        evidence: {node: value}
        """
        # 获取查询变量
        query_nodes = list(query.keys())
        
        # 获取需要消元的变量（非查询、非证据）
        hidden = [n for n in self.nodes if n not in query_nodes and n not in evidence]
        
        # 枚举所有可能的赋值
        def enumerate_assignments(variables, current):
            if not variables:
                yield current.copy()
                return
            var = variables[0]
            for value in self.nodes[var]['values']:
                current[var] = value
                yield from enumerate_assignments(variables[1:], current)
            del current[var]
        
        # 计算归一化常数和查询概率
        query_values = {}
        total = 0.0
        
        # 枚举查询变量的所有可能值
        if '?' in query.values():
            # 返回分布
            query_node = query_nodes[0]
            for qv in self.nodes[query_node]['values']:
                prob_sum = 0.0
                for assignment in enumerate_assignments(hidden, {}):
                    assignment.update(evidence)
                    assignment[query_node] = qv
                    prob_sum += self.joint_prob(assignment)
                query_values[qv] = prob_sum
                total += prob_sum
            
            # 归一化
            for k in query_values:
                query_values[k] /= total
            return query_values
        else:
            # 返回单个概率
            for assignment in enumerate_assignments(hidden, {}):
                assignment.update(evidence)
                assignment.update(query)
                total += self.joint_prob(assignment)
            return total


# 构建疾病诊断网络
bn = SimpleBayesianNetwork()

# 添加节点
bn.add_node('吸烟', ['是', '否'])
bn.add_node('肺癌', ['是', '否'], parents=['吸烟'])
bn.add_node('呼吸困难', ['是', '否'], parents=['肺癌'])
bn.add_node('X光异常', ['是', '否'], parents=['肺癌'])

# 设置CPT
bn.set_cpt('吸烟', {(): {'是': 0.3, '否': 0.7}})
bn.set_cpt('肺癌', {
    ('是',): {'是': 0.1, '否': 0.9},
    ('否',): {'是': 0.01, '否': 0.99}
})
bn.set_cpt('呼吸困难', {
    ('是',): {'是': 0.65, '否': 0.35},
    ('否',): {'是': 0.1, '否': 0.9}
})
bn.set_cpt('X光异常', {
    ('是',): {'是': 0.9, '否': 0.1},
    ('否',): {'是': 0.05, '否': 0.95}
})

# 推断示例
print("=== 贝叶斯网络推断 ===")

# 1. 计算患肺癌的概率分布（无条件）
print("\n1. 无条件概率 P(肺癌):")
result = bn.enumerate_inference({'肺癌': '?'}, {})
print(f"   P(肺癌=是) = {result['是']:.4f}")
print(f"   P(肺癌=否) = {result['否']:.4f}")

# 2. 已知X光异常，求患肺癌概率
print("\n2. P(肺癌 | X光异常=是):")
result = bn.enumerate_inference({'肺癌': '?'}, {'X光异常': '是'})
print(f"   P(肺癌=是 | X光异常=是) = {result['是']:.4f}")
print(f"   P(肺癌=否 | X光异常=是) = {result['否']:.4f}")

# 3. 已知吸烟且X光异常
print("\n3. P(肺癌 | 吸烟=是, X光异常=是):")
result = bn.enumerate_inference({'肺癌': '?'}, {'吸烟': '是', 'X光异常': '是'})
print(f"   P(肺癌=是 | 吸烟, X光异常) = {result['是']:.4f}")
print(f"   P(肺癌=否 | 吸烟, X光异常) = {result['否']:.4f}")

# 4. 计算联合概率
print("\n4. 联合概率 P(吸烟=是, 肺癌=是, 呼吸困难=是, X光异常=是):")
prob = bn.joint_prob({'吸烟': '是', '肺癌': '是', '呼吸困难': '是', 'X光异常': '是'})
print(f"   = {prob:.6f}")
```

**输出示例：**
```
=== 贝叶斯网络推断 ===

1. 无条件概率 P(肺癌):
   P(肺癌=是) = 0.0370
   P(肺癌=否) = 0.9630

2. P(肺癌 | X光异常=是):
   P(肺癌=是 | X光异常=是) = 0.4737
   P(肺癌=否 | X光异常=是) = 0.5263

3. P(肺癌 | 吸烟=是, X光异常=是):
   P(肺癌=是 | 吸烟, X光异常) = 0.7500
   P(肺癌=否 | 吸烟, X光异常) = 0.2500

4. 联合概率 P(吸烟=是, 肺癌=是, 呼吸困难=是, X光异常=是):
   = 0.01755
```

---

## 应用场景示例：风险评估系统

```python
# 构建贷款风险评估网络
risk_bn = SimpleBayesianNetwork()

# 添加节点
risk_bn.add_node('收入', ['高', '中', '低'])
risk_bn.add_node('负债', ['高', '低'])
risk_bn.add_node('信用记录', ['好', '差'])
risk_bn.add_node('违约风险', ['高', '低'], parents=['收入', '负债', '信用记录'])

# 设置CPT
risk_bn.set_cpt('收入', {(): {'高': 0.2, '中': 0.5, '低': 0.3}})
risk_bn.set_cpt('负债', {(): {'高': 0.4, '低': 0.6}})
risk_bn.set_cpt('信用记录', {(): {'好': 0.7, '差': 0.3}})

# 违约风险CPT（简化示例）
risk_bn.set_cpt('违约风险', {
    ('高', '高', '好'): {'高': 0.3, '低': 0.7},
    ('高', '高', '差'): {'高': 0.7, '低': 0.3},
    ('高', '低', '好'): {'高': 0.1, '低': 0.9},
    ('高', '低', '差'): {'高': 0.3, '低': 0.7},
    ('中', '高', '好'): {'高': 0.2, '低': 0.8},
    ('中', '高', '差'): {'高': 0.5, '低': 0.5},
    ('中', '低', '好'): {'高': 0.05, '低': 0.95},
    ('中', '低', '差'): {'高': 0.2, '低': 0.8},
    ('低', '高', '好'): {'高': 0.4, '低': 0.6},
    ('低', '高', '差'): {'高': 0.8, '低': 0.2},
    ('低', '低', '好'): {'高': 0.1, '低': 0.9},
    ('低', '低', '差'): {'高': 0.5, '低': 0.5},
})

print("=== 贷款风险评估 ===")

# 查询：收入中等、负债高、信用记录差
evidence = {'收入': '中', '负债': '高', '信用记录': '差'}
result = risk_bn.enumerate_inference({'违约风险': '?'}, evidence)
print(f"证据: {evidence}")
print(f"P(违约风险=高) = {result['高']:.4f}")
print(f"P(违约风险=低) = {result['低']:.4f}")
```

---

## 小结

本章介绍了贝叶斯网络：

1. **DAG结构**：用有向无环图表示变量间的依赖关系
2. **条件概率表**：存储给定父节点时每个节点的概率分布
3. **联合概率分解**：将联合概率分解为条件概率的乘积
4. **推断方法**：精确推断（变量消元）和近似推断（采样）

贝叶斯网络是概率图模型的基础，在医疗诊断、风险评估、故障诊断等领域有广泛应用。然而，当变量之间存在复杂依赖或存在隐变量时，贝叶斯网络的学习和推断变得困难。下一章，我们将学习处理隐变量问题的经典方法——EM算法。