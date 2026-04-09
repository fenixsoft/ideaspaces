"""
生成 L1 单位球与损失函数等值线相交的几何解释图片（修正版）
用于文档 docs/statistical-learning/linear-models/regularization-glm.md
展示稀疏解的几何来源：等值线刚好碰到菱形顶点，不穿过菱形
"""

import numpy as np
import matplotlib.pyplot as plt

# 设置中文字体支持
plt.rcParams['font.sans-serif'] = ['Noto Sans CJK SC', 'WenQuanYi Zen Hei', 'SimHei', 'sans-serif']
plt.rcParams['axes.unicode_minus'] = False


def l1_unit_ball(t=1.0):
    """
    生成 L1 单位球（菱形）边界点
    参数 t 控制菱形大小：|β₁| + |β₂| ≤ t
    """
    x = np.array([0, t, 0, -t, 0])
    y = np.array([t, 0, -t, 0, t])
    return x, y


def loss_contour(center_x, center_y, a, b, angle=0, n_points=200):
    """
    生成损失函数等值线（椭圆形）
    参数 center: 等值线中心（未正则化时的最优解）
    参数 a, b: 椭圆的两个半轴长度
    参数 angle: 椭圆旋转角度（弧度）
    """
    theta = np.linspace(0, 2*np.pi, n_points)
    # 生成未旋转的椭圆
    x_unrot = a * np.cos(theta)
    y_unrot = b * np.sin(theta)
    # 应用旋转
    cos_a = np.cos(angle)
    sin_a = np.sin(angle)
    x = center_x + x_unrot * cos_a - y_unrot * sin_a
    y = center_y + x_unrot * sin_a + y_unrot * cos_a
    return x, y


# 创建图形
fig, ax = plt.subplots(figsize=(8, 8))

# L1 单位球参数 t
t = 1.0

# 绘制 L1 单位球（菱形）
x_l1, y_l1 = l1_unit_ball(t)
ax.fill(x_l1, y_l1, color='steelblue', alpha=0.3, label='L1 约束区域')
ax.plot(x_l1, y_l1, color='steelblue', linewidth=2)

# 设计场景：椭圆中心在第一象限，等值线扩展时最先碰到顶点 (0, t) 即 (0, 1)
# 这会导致 β₁ = 0，β₂ = t（稀疏解）

center_x = 0.6  # β₁ 方向偏移较小
center_y = 1.8  # β₂ 方向偏移较大（无约束最优解在 y 方向更远）

# 椭圆形状：损失函数在 β₁ 方向更敏感（椭圆更窄）
a = 0.8  # β₁ 方向半轴（窄）
b = 1.2  # β₂ 方向半轴（宽）

# 椭圆旋转角度：使椭圆长轴指向从中心到顶点的方向，避免穿过菱形
# 从中心 (0.6, 1.8) 到顶点 (0, 1) 的方向
dx = 0 - center_x  # -0.6
dy = t - center_y  # -0.8
angle = np.arctan2(dy, dx)  # 约 -53度，椭圆长轴指向顶点方向

# 计算刚好通过顶点 (0, t) = (0, 1) 的椭圆缩放因子
# 顶点相对于椭圆中心的位置
target_x = 0 - center_x  # -0.6
target_y = t - center_y  # 1 - 1.8 = -0.8

# 反向旋转这个点，找到它在未旋转坐标系中的位置
cos_a = np.cos(-angle)
sin_a = np.sin(-angle)
x_unrot = target_x * cos_a - target_y * sin_a
y_unrot = target_x * sin_a + target_y * cos_a

# 椭圆方程: (x'/a)^2 + (y'/b)^2 = 1
# 缩放因子 scale 使椭圆刚好通过该点
scale = np.sqrt(x_unrot**2 / a**2 + y_unrot**2 / b**2)

# 最终椭圆参数
a_final = a * scale
b_final = b * scale

# 绘制较小的等值线（不接触菱形）
for s in [0.3, 0.5, 0.7, 0.85]:
    x_c, y_c = loss_contour(center_x, center_y, a_final * s, b_final * s, angle)
    ax.plot(x_c, y_c, color='orange', linewidth=1.5, linestyle='--', alpha=0.6)

# 绘制刚好接触顶点的等值线（重点展示）
x_contact, y_contact = loss_contour(center_x, center_y, a_final, b_final, angle)
ax.plot(x_contact, y_contact, color='red', linewidth=2.5, label='损失等值线')

# 标记最优解位置（菱形顶点 (0, t)）
ax.plot(0, t, 'ro', markersize=12, label='最优解 (稀疏点)')
ax.annotate('β₁ = 0\nβ₂ = t', xy=(0, t), xytext=(0.3, t+0.3),
            fontsize=11, ha='left', fontweight='bold',
            arrowprops=dict(arrowstyle='->', color='darkred', lw=1.5))

# 标记未正则化最优解
ax.plot(center_x, center_y, 'ko', markersize=10, label='未正则化最优解')
ax.annotate('无约束\n最优解', xy=(center_x, center_y), xytext=(center_x+0.15, center_y-0.1),
            fontsize=10, ha='left')

# 绘制坐标轴
ax.axhline(y=0, color='gray', linewidth=0.8, linestyle='--')
ax.axvline(x=0, color='gray', linewidth=0.8, linestyle='--')

# 设置图形属性
ax.set_xlim(-1.5, 2.0)
ax.set_ylim(-0.5, 2.5)
ax.set_aspect('equal')
ax.grid(True, alpha=0.3)

# 添加标签和标题
ax.set_xlabel('β₁', fontsize=14)
ax.set_ylabel('β₂', fontsize=14)
ax.set_title('L1 正则化的几何解释\n等值线首次碰到菱形顶点 → 稀疏解', fontsize=14)
ax.legend(loc='upper right', fontsize=10)

# 添加说明文字
ax.text(-1.3, 2.2,
        '约束区域：|β₁| + |β₂| ≤ t\n'
        '等值线从中心向外扩展\n'
        '首次碰到顶点 (0, t)\n'
        '→ β₁ = 0（稀疏解）',
        fontsize=10,
        verticalalignment='top',
        bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.8))

# 保存图片
output_path = '/root/devspaces/ideaspaces/docs/statistical-learning/linear-models/assets/l1_sparse_geometry_v2.png'
plt.savefig(output_path, dpi=150, bbox_inches='tight', facecolor='white')
plt.close()

print(f"图片已保存到: {output_path}")