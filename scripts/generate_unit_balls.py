"""
生成不同 p 值下的单位球形状可视化图片（8个子图）
用于文档 docs/maths/linear/vectors.md 中关于范数的几何意义说明
"""

import numpy as np
import matplotlib.pyplot as plt

# 设置中文字体支持
plt.rcParams['font.sans-serif'] = ['Noto Sans CJK SC', 'WenQuanYi Zen Hei', 'SimHei', 'sans-serif']
plt.rcParams['axes.unicode_minus'] = False


def unit_ball_points(p, n_points=1000):
    """
    生成给定 p 值下的单位球边界点（二维情况）
    """
    if p == np.inf:
        x = np.array([-1, 1, 1, -1, -1])
        y = np.array([-1, -1, 1, 1, -1])
        return x, y
    elif p == 1:
        x = np.array([0, 1, 0, -1, 0])
        y = np.array([1, 0, -1, 0, 1])
        return x, y
    else:
        theta = np.linspace(0, 2*np.pi, n_points)
        x = np.cos(theta)
        y = np.sin(theta)

        for i in range(n_points):
            cos_t = abs(np.cos(theta[i]))
            sin_t = abs(np.sin(theta[i]))

            if cos_t < 1e-10 and sin_t < 1e-10:
                continue
            elif cos_t < 1e-10:
                r = 1.0 / sin_t if sin_t > 0 else 1.0
            elif sin_t < 1e-10:
                r = 1.0 / cos_t if cos_t > 0 else 1.0
            else:
                r = np.power(cos_t**p + sin_t**p, -1.0/p)

            x[i] = r * np.cos(theta[i])
            y[i] = r * np.sin(theta[i])

        return x, y


# 创建 2x4 子图布局
fig, axes = plt.subplots(2, 4, figsize=(16, 8))
axes = axes.flatten()

# 定义要绘制的 p 值列表
p_values = [0.25, 0.5, 1, 2, 3, 4, 6, np.inf]

# 为每个子图绘制对应 p 值的单位球
for ax, p in zip(axes, p_values):
    x, y = unit_ball_points(p)

    # 填充单位球内部
    ax.fill(x, y, color='steelblue', alpha=0.3)
    # 绘制边界
    ax.plot(x, y, color='steelblue', linewidth=2)

    # 绘制坐标轴
    ax.axhline(y=0, color='gray', linewidth=0.8, linestyle='--')
    ax.axvline(x=0, color='gray', linewidth=0.8, linestyle='--')

    # 设置图形属性
    ax.set_xlim(-1.3, 1.3)
    ax.set_ylim(-1.3, 1.3)
    ax.set_aspect('equal')
    ax.grid(True, alpha=0.3)

    # 设置标题
    if p == np.inf:
        title = 'p = ∞'
        subtitle = '正方形 (L∞)'
    elif p == 1:
        title = 'p = 1'
        subtitle = '菱形 (曼哈顿)'
    elif p == 2:
        title = 'p = 2'
        subtitle = '圆 (欧几里得)'
    elif p == 0.25:
        title = 'p = 0.25'
        subtitle = '星形 (非范数)'
    elif p == 0.5:
        title = 'p = 0.5'
        subtitle = '星形 (非范数)'
    else:
        title = f'p = {p}'
        subtitle = ''

    ax.set_title(f'{title}\n{subtitle}', fontsize=12)
    ax.set_xlabel('x', fontsize=10)
    ax.set_ylabel('y', fontsize=10)

# 添加整体标题
fig.suptitle('$L_p$ 范数的单位球形状（满足 $\\|\\mathbf{v}\\|_p = 1$ 的点集合）', fontsize=16, y=1.02)

# 调整布局
plt.tight_layout()

# 保存图片
output_path = '/root/devspaces/ideaspaces/docs/maths/linear/assets/unit_balls.png'
plt.savefig(output_path, dpi=150, bbox_inches='tight', facecolor='white')
plt.close()

print(f"图片已保存到: {output_path}")