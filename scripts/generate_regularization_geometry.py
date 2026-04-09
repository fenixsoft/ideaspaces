"""
生成正则化几何解释图
使用字体文件路径直接加载中文字体
"""
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import numpy as np

# 直接加载字体文件
font_path = '/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc'
chinese_font = fm.FontProperties(fname=font_path)

# 创建图形
fig, axes = plt.subplots(1, 2, figsize=(12, 5))

# 共用的参数设置
beta1_range = np.linspace(-2.5, 2.5, 100)
beta2_range = np.linspace(-2.5, 2.5, 100)
beta1, beta2 = np.meshgrid(beta1_range, beta2_range)

# 模拟损失函数的等高线（椭圆形状）
# 假设最优解在 (2, 1) 附近
loss_center = (2, 1)
loss = ((beta1 - loss_center[0])**2 + 0.5 * (beta2 - loss_center[1])**2)

# 约束半径（正则化强度）
constraint_radius = 1.5

# === 左图：L2正则化（圆形约束）===
ax1 = axes[0]

# 绘制等高线
contour1 = ax1.contour(beta1, beta2, loss, levels=[0.5, 1, 2, 4, 6, 8],
                        colors='steelblue', alpha=0.7, linewidths=1.5)
ax1.clabel(contour1, inline=True, fontsize=9, fmt='%.1f')

# 绘制圆形约束区域（L2范数约束）
theta = np.linspace(0, 2*np.pi, 100)
circle_x = constraint_radius * np.cos(theta)
circle_y = constraint_radius * np.sin(theta)
ax1.plot(circle_x, circle_y, 'r-', linewidth=2.5)
ax1.fill(circle_x, circle_y, color='red', alpha=0.15)

# 标记最优解（无约束）
ax1.plot(*loss_center, 'b*', markersize=15)

# 标记约束后的解
intersect_l2 = (1.2, 0.9)
ax1.plot(*intersect_l2, 'go', markersize=10)

# 绘制从最优解到约束解的"拉力"线
ax1.annotate('', xy=intersect_l2, xytext=loss_center,
             arrowprops=dict(arrowstyle='->', color='green', lw=2))

# 设置坐标轴 - 使用 LaTeX 渲染数学符号
ax1.set_xlim(-2.5, 3)
ax1.set_ylim(-2.5, 2.5)
ax1.set_xlabel(r'$\beta_1$', fontsize=14)
ax1.set_ylabel(r'$\beta_2$', fontsize=14)
ax1.set_title('L2正则化（Ridge）：圆形约束', fontproperties=chinese_font, fontsize=12)
ax1.grid(True, alpha=0.3)
ax1.axhline(y=0, color='k', linewidth=0.5)
ax1.axvline(x=0, color='k', linewidth=0.5)
ax1.set_aspect('equal')

# 添加图例（使用中文）
from matplotlib.patches import Patch
from matplotlib.lines import Line2D
legend_elements = [
    Patch(facecolor='red', alpha=0.15, edgecolor='red', linewidth=2, label='L2约束边界'),
    Line2D([0], [0], marker='*', color='w', markerfacecolor='blue', markersize=12, label='无约束最优解'),
    Line2D([0], [0], marker='o', color='w', markerfacecolor='green', markersize=8, label='L2正则化解')
]
ax1.legend(handles=legend_elements, loc='upper right', prop=chinese_font, fontsize=9)

# === 右图：L1正则化（菱形约束）===
ax2 = axes[1]

# 绘制等高线
contour2 = ax2.contour(beta1, beta2, loss, levels=[0.5, 1, 2, 4, 6, 8],
                        colors='steelblue', alpha=0.7, linewidths=1.5)
ax2.clabel(contour2, inline=True, fontsize=9, fmt='%.1f')

# 绘制菱形约束区域（L1范数约束）
diamond_x = [constraint_radius, 0, -constraint_radius, 0, constraint_radius]
diamond_y = [0, constraint_radius, 0, -constraint_radius, 0]
ax2.plot(diamond_x, diamond_y, 'r-', linewidth=2.5)
ax2.fill(diamond_x, diamond_y, color='red', alpha=0.15)

# 标记最优解（无约束）
ax2.plot(*loss_center, 'b*', markersize=15)

# 标记约束后的解（碰到顶点）
intersect_l1 = (1.5, 0)
ax2.plot(*intersect_l1, 'go', markersize=10)

# 绘制从最优解到约束解的"拉力"线
ax2.annotate('', xy=intersect_l1, xytext=loss_center,
             arrowprops=dict(arrowstyle='->', color='green', lw=2))

# 标记"顶点"位置
ax2.annotate('顶点\n(参数为0)', xy=(0, constraint_radius), xytext=(0.3, 2),
             fontproperties=chinese_font, fontsize=9, color='darkred',
             arrowprops=dict(arrowstyle='->', color='darkred', lw=1))

# 设置坐标轴
ax2.set_xlim(-2.5, 3)
ax2.set_ylim(-2.5, 2.5)
ax2.set_xlabel(r'$\beta_1$', fontsize=14)
ax2.set_ylabel(r'$\beta_2$', fontsize=14)
ax2.set_title('L1正则化（Lasso）：菱形约束', fontproperties=chinese_font, fontsize=12)
ax2.grid(True, alpha=0.3)
ax2.axhline(y=0, color='k', linewidth=0.5)
ax2.axvline(x=0, color='k', linewidth=0.5)
ax2.set_aspect('equal')

# 添加图例
legend_elements2 = [
    Patch(facecolor='red', alpha=0.15, edgecolor='red', linewidth=2, label='L1约束边界'),
    Line2D([0], [0], marker='*', color='w', markerfacecolor='blue', markersize=12, label='无约束最优解'),
    Line2D([0], [0], marker='o', color='w', markerfacecolor='green', markersize=8, label='L1正则化解（稀疏）')
]
ax2.legend(handles=legend_elements2, loc='upper right', prop=chinese_font, fontsize=9)

# 总标题
fig.suptitle('正则化的几何解释：等高线与约束区域的交点', fontproperties=chinese_font, fontsize=14, y=1.02)

plt.tight_layout()
plt.savefig('/root/devspaces/ideaspaces/docs/statistical-learning/linear-models/assets/regularization-geometry.png',
            dpi=150, bbox_inches='tight', facecolor='white')
print("图片已保存到 assets/regularization-geometry.png")