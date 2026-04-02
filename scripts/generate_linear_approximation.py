#!/usr/bin/env python3
"""
生成线性近似示意图
展示 f(x) = sqrt(x) 在 x=4 处的切线近似
"""

import numpy as np
import matplotlib.pyplot as plt

plt.rcParams['figure.dpi'] = 150

# 定义函数和导数
def f(x):
    return np.sqrt(x)

def df(x):
    return 1 / (2 * np.sqrt(x))

# 基准点
x0 = 4
y0 = f(x0)

# 切线方程: y = f(x0) + f'(x0) * (x - x0)
def tangent(x):
    return y0 + df(x0) * (x - x0)

# 绘图范围
x = np.linspace(3.5, 4.5, 200)
y_curve = f(x)
y_tangent = tangent(x)

# 创建图形
fig, ax = plt.subplots(figsize=(10, 6))

# 绘制函数曲线
ax.plot(x, y_curve, 'b-', linewidth=2.5, label='$f(x) = \\sqrt{x}$')

# 绘制切线
ax.plot(x, y_tangent, 'r--', linewidth=2, label='Tangent: $y = 2 + \\frac{1}{4}(x - 4)$')

# 标记基准点
ax.plot(x0, y0, 'ko', markersize=10, zorder=5)
ax.annotate('$(4, 2)$', xy=(x0, y0), xytext=(4.05, 2.1), fontsize=12)

# 标记近似点和真实点
dx = 0.01  # Δx
x_approx = x0 + dx  # x = 4.01

# 切线上的近似值
y_approx = tangent(x_approx)  # 线性近似值 ≈ 2.0025

# 真实函数值
y_exact = f(x_approx)  # 真实值 ≈ 2.002498

# 标记近似点（切线上）
ax.plot(x_approx, y_approx, 'rs', markersize=8, zorder=5, label='Linear approx. point')

# 标记真实点（曲线上）
ax.plot(x_approx, y_exact, 'b^', markersize=8, zorder=5, label='Exact function value')

# 绘制垂直线显示 Δx
ax.annotate('', xy=(x_approx, y0), xytext=(x0, y0),
            arrowprops=dict(arrowstyle='<->', color='green', lw=1.5))
ax.text(4.005, 1.95, '$\\Delta x = 0.01$', fontsize=11, color='green')

# 绘制误差标注
ax.annotate('', xy=(x_approx, y_exact), xytext=(x_approx, y_approx),
            arrowprops=dict(arrowstyle='<->', color='purple', lw=1.5))
ax.text(4.015, 2.0015, 'Error', fontsize=10, color='purple')

# 添加图例和标签
ax.set_xlabel('$x$', fontsize=14)
ax.set_ylabel('$y$', fontsize=14)
ax.set_title('Linear Approximation: Approximating Curve with Tangent Line\n$f(x+\\Delta x) \\approx f(x) + f\'(x) \\Delta x$', fontsize=14)
ax.legend(loc='upper left', fontsize=11)
ax.grid(True, alpha=0.3)

# 设置坐标轴范围
ax.set_xlim(3.9, 4.1)
ax.set_ylim(1.95, 2.05)

# 添加文本说明
textstr = 'Linear approx: $\\sqrt{4.01} \\approx 2.0025$\nExact value: $\\sqrt{4.01} \\approx 2.002498$\nError: $\\approx 2 \\times 10^{-6}$'
props = dict(boxstyle='round', facecolor='wheat', alpha=0.8)
ax.text(0.98, 0.02, textstr, transform=ax.transAxes, fontsize=11,
        verticalalignment='bottom', horizontalalignment='right', bbox=props)

plt.tight_layout()
plt.savefig('/root/devspaces/ideaspaces/docs/calculus/assets/linear_approximation.png',
            dpi=150, bbox_inches='tight', facecolor='white')
plt.close()

print("图片已保存至 docs/calculus/assets/linear_approximation.png")