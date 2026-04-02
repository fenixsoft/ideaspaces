#!/usr/bin/env python3
"""
生成泰勒展开示意图
展示不同阶数的泰勒展开对 sin(x) 的近似效果
"""

import numpy as np
import matplotlib.pyplot as plt

plt.rcParams['figure.dpi'] = 150

# 定义函数
def f(x):
    return np.sin(x)

# 泰勒展开各阶近似（在 a=0 处展开）
def taylor_0(x):
    """零阶泰勒展开：常数近似"""
    return 0

def taylor_1(x):
    """一阶泰勒展开：线性近似"""
    return x

def taylor_3(x):
    """三阶泰勒展开"""
    return x - x**3 / 6

def taylor_5(x):
    """五阶泰勒展开"""
    return x - x**3 / 6 + x**5 / 120

def taylor_7(x):
    """七阶泰勒展开"""
    return x - x**3 / 6 + x**5 / 120 - x**7 / 5040

# 绘图范围
x = np.linspace(-3, 3, 200)
y_exact = f(x)
y_t0 = taylor_0(x)
y_t1 = taylor_1(x)
y_t3 = taylor_3(x)
y_t5 = taylor_5(x)
y_t7 = taylor_7(x)

# 创建图形
fig, axes = plt.subplots(1, 2, figsize=(14, 5))

# 左图：全局视图
ax1 = axes[0]
ax1.plot(x, y_exact, 'k-', linewidth=3, label='$\\sin(x)$ (exact)')
ax1.plot(x, y_t1, 'r--', linewidth=2, label='1st order: $x$')
ax1.plot(x, y_t3, 'g--', linewidth=2, label='3rd order: $x - x^3/6$')
ax1.plot(x, y_t5, 'b--', linewidth=2, label='5th order')
ax1.plot(x, y_t7, 'm--', linewidth=2, label='7th order')

ax1.axhline(y=0, color='gray', linestyle='-', linewidth=0.5)
ax1.axvline(x=0, color='gray', linestyle='-', linewidth=0.5)
ax1.set_xlabel('$x$', fontsize=14)
ax1.set_ylabel('$y$', fontsize=14)
ax1.set_title('Taylor Expansion of $\\sin(x)$ at $x=0$', fontsize=14)
ax1.legend(loc='upper right', fontsize=10)
ax1.grid(True, alpha=0.3)
ax1.set_ylim(-2, 2)

# 右图：局部放大（展示近似精度）
ax2 = axes[1]
x_zoom = np.linspace(-0.5, 0.5, 200)
y_exact_zoom = f(x_zoom)
y_t1_zoom = taylor_1(x_zoom)
y_t3_zoom = taylor_3(x_zoom)
y_t5_zoom = taylor_5(x_zoom)

ax2.plot(x_zoom, y_exact_zoom, 'k-', linewidth=3, label='$\\sin(x)$ (exact)')
ax2.plot(x_zoom, y_t1_zoom, 'r--', linewidth=2, label='1st order')
ax2.plot(x_zoom, y_t3_zoom, 'g--', linewidth=2, label='3rd order')
ax2.plot(x_zoom, y_t5_zoom, 'b--', linewidth=2, label='5th order')

ax2.axhline(y=0, color='gray', linestyle='-', linewidth=0.5)
ax2.axvline(x=0, color='gray', linestyle='-', linewidth=0.5)
ax2.set_xlabel('$x$', fontsize=14)
ax2.set_ylabel('$y$', fontsize=14)
ax2.set_title('Zoomed View: Near $x=0$', fontsize=14)
ax2.legend(loc='upper left', fontsize=10)
ax2.grid(True, alpha=0.3)

# 标注近似点
ax2.annotate('Approximation\nimproves with\nhigher order', xy=(0.3, 0.295), fontsize=10,
             xytext=(0.35, 0.4), arrowprops=dict(arrowstyle='->', color='gray'))

plt.tight_layout()
plt.savefig('/root/devspaces/ideaspaces/docs/calculus/assets/taylor_expansion.png',
            dpi=150, bbox_inches='tight', facecolor='white')
plt.close()

print("图片已保存至 docs/calculus/assets/taylor_expansion.png")