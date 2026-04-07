import numpy as np
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties

# 直接指定中文字体文件路径
font_path = '/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc'
font = FontProperties(fname=font_path)

# 创建图形
fig, ax = plt.subplots(figsize=(10, 8))

# 定义向量起点
origin = np.array([0, 0])

# 定义X的列空间方向
x_col = np.array([1, 0.3])

# 定义y向量（真实值）
y = np.array([2, 3])

# 计算y在X列空间的投影
projection_coeff = np.dot(y, x_col) / np.dot(x_col, x_col)
y_hat = projection_coeff * x_col

# 计算残差向量
e = y - y_hat

# 绘制X的列空间
col_space_start = np.array([-3, -0.9])
col_space_end = np.array([5, 1.5])
ax.plot([col_space_start[0], col_space_end[0]],
        [col_space_start[1], col_space_end[1]],
        'b-', linewidth=2.5, alpha=0.6)
ax.fill_between([col_space_start[0], col_space_end[0]],
                [col_space_start[1]-0.3, col_space_end[1]-0.3],
                [col_space_start[1]+0.3, col_space_end[1]+0.3],
                alpha=0.12, color='blue')
ax.text(3.2, 1.3, 'X 的列空间', fontproperties=font, fontsize=11, color='#3366cc', style='italic')

# 绘制y向量
ax.quiver(origin[0], origin[1], y[0], y[1],
          angles='xy', scale_units='xy', scale=1,
          color='#2ca02c', width=0.025)
ax.annotate('y\n（真实值）', xy=y, xytext=(y[0]+0.3, y[1]+0.1), fontproperties=font, fontsize=11, color='#2ca02c', ha='left')

# 绘制投影向量 Xβ
ax.quiver(origin[0], origin[1], y_hat[0], y_hat[1],
          angles='xy', scale_units='xy', scale=1,
          color='#1f77b4', width=0.025)
ax.annotate('Xβ\n（预测值）', xy=y_hat, xytext=(y_hat[0]-0.6, y_hat[1]-0.6), fontproperties=font, fontsize=11, color='#1f77b4', ha='right')

# 绘制残差向量
ax.quiver(y_hat[0], y_hat[1], e[0], e[1],
          angles='xy', scale_units='xy', scale=1,
          color='#d62728', width=0.025)
ax.annotate('e = y - Xβ\n（残差向量）', xy=y_hat + e/2, xytext=(y_hat[0] + e[0]/2 - 1.4, y_hat[1] + e[1]/2 + 0.4),
            fontproperties=font, fontsize=11, color='#d62728', ha='left')

# 绘制虚线连接
ax.plot([y_hat[0], y[0]], [y_hat[1], y[1]], 'r--', linewidth=1.5, alpha=0.7)

# 绘制直角标记（表示正交）
corner_size = 0.25
corner_x = y_hat[0]
corner_y = y_hat[1]
ax.plot([corner_x, corner_x + corner_size * x_col[0]/np.linalg.norm(x_col)],
        [corner_y, corner_y + corner_size * x_col[1]/np.linalg.norm(x_col)],
        'gray', linewidth=1.5)
ax.plot([corner_x + corner_size * x_col[0]/np.linalg.norm(x_col),
         corner_x + corner_size * x_col[0]/np.linalg.norm(x_col) + corner_size * e[0]/np.linalg.norm(e)],
        [corner_y + corner_size * x_col[1]/np.linalg.norm(x_col),
         corner_y + corner_size * x_col[1]/np.linalg.norm(x_col) + corner_size * e[1]/np.linalg.norm(e)],
        'gray', linewidth=1.5)

# 设置坐标轴
ax.set_xlim(-1, 4)
ax.set_ylim(-1, 5)
ax.set_xlabel('特征维度 1', fontproperties=font, fontsize=12)
ax.set_ylabel('特征维度 2', fontproperties=font, fontsize=12)
ax.set_title('OLS 的几何直觉：投影', fontproperties=font, fontsize=14, fontweight='bold')
ax.grid(True, alpha=0.3, linestyle='--')
ax.set_aspect('equal')

# 添加说明文字
ax.text(0.2, -0.8, '残差向量 e 与 X 的列空间正交时，‖e‖ 最小',
        fontproperties=font, fontsize=10, style='italic', color='#666666')

# 添加图例
from matplotlib.lines import Line2D
legend_elements = [
    Line2D([0], [0], color='#2ca02c', linewidth=3, label='y（真实值）'),
    Line2D([0], [0], color='#1f77b4', linewidth=3, label='Xβ（预测值）'),
    Line2D([0], [0], color='#d62728', linewidth=3, label='e（残差向量）'),
    Line2D([0], [0], color='#3366cc', linewidth=2.5, alpha=0.6, label='X 的列空间'),
]
ax.legend(handles=legend_elements, prop=font, loc='upper right', fontsize=10, framealpha=0.9)

plt.tight_layout()
plt.savefig('docs/statistical-learning/linear-models/assets/ols-projection.png', dpi=150, bbox_inches='tight', facecolor='white')
print("图片已保存")