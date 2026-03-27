#!/usr/bin/env python3
"""
生成向量示意图
用于线性代数系列文章第1章：引言
"""

import matplotlib.pyplot as plt
import numpy as np

# 使用默认字体（英文）
plt.rcParams['axes.unicode_minus'] = False

# 创建图形
fig, ax = plt.subplots(figsize=(8, 6), dpi=150)

# 定义向量 v = (3, 2)
v = np.array([3, 2])
origin = np.array([0, 0])

# 绘制坐标轴
ax.axhline(y=0, color='gray', linewidth=0.8, linestyle='-')
ax.axvline(x=0, color='gray', linewidth=0.8, linestyle='-')

# 绘制向量（带箭头）
ax.annotate('', xy=v, xytext=origin,
            arrowprops=dict(arrowstyle='->', color='#2E86AB', lw=2.5))

# 绘制投影虚线（显示分量）
ax.plot([0, v[0]], [v[1], v[1]], 'k--', alpha=0.5, linewidth=1)
ax.plot([v[0], v[0]], [0, v[1]], 'k--', alpha=0.5, linewidth=1)

# 标记向量终点
ax.plot(v[0], v[1], 'o', color='#2E86AB', markersize=8)

# 添加标签
ax.text(v[0] + 0.15, v[1] + 0.15, r'$\mathbf{v} = (3, 2)$', fontsize=12, color='#2E86AB')
ax.text(v[0], -0.4, '3', fontsize=10, ha='center')
ax.text(-0.3, v[1], '2', fontsize=10, ha='right', va='center')

# 设置坐标轴标签
ax.set_xlabel('x', fontsize=12)
ax.set_ylabel('y', fontsize=12)

# 设置坐标轴范围
ax.set_xlim(-0.5, 4)
ax.set_ylim(-0.5, 3)

# 设置等比例
ax.set_aspect('equal')

# 添加网格
ax.grid(True, alpha=0.3, linestyle=':')

# 设置标题
ax.set_title('Vector in 2D Space', fontsize=14, pad=15)

# 调整布局
plt.tight_layout()

# 保存图片
plt.savefig('/root/devspaces/ideaspaces/articles/linear-algebra-vectors-matrices/draft/assets/vector_2d.png',
            dpi=150, bbox_inches='tight', facecolor='white')
print("向量示意图已保存到: assets/vector_2d.png")

plt.close()
