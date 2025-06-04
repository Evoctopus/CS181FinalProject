import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from matplotlib.font_manager import FontProperties

plt.rcParams['font.sans-serif'] = ['SimHei', 'Arial Unicode MS', 'Microsoft YaHei', 'sans-serif']
plt.rcParams['axes.unicode_minus'] = False

player1_algorithms = ["Random","Greedy","MCT", "Minimax"]
player2_algorithms = ["Random","Greedy","MCT", "Minimax","qlearning_Random","qlearning_Greedy","qlearning_MCT", "qlearning_Minimax"]

np.random.seed(42) 
win_rates = np.random.uniform(low=0.3, high=0.95, size=(4, 8))

win_rates[0] = np.array([0.5614, 0.1023, 0.0200, 0.0000, 0.12, 0.48, 0.46, 0.56]) 
win_rates[1] = np.array([0.9376, 1.0000, 0.0603, 0.0000, 0.00, 0.00, 0.70, 0.82]) 
win_rates[2] = np.array([1.0000, 0.9333, 0.5670, 0.2333, 0.76, 0.92, 0.90, 1.00])  
win_rates[3] = np.array([1.0000, 1.0000, 0.7000, 1.0000, 1.00, 1.00, 1.00, 0.98]) 

def create_custom_colormap():
    colors = ["#ff0000", "#ff5e00", "#ffbb00", "#f5ff00", "#a2ff00", "#0fff00", "#00ff8c"]
    positions = [0.0, 0.3, 0.45, 0.5, 0.6, 0.75, 1.0]
    return mcolors.LinearSegmentedColormap.from_list("custom", list(zip(positions, colors)))

plt.figure(figsize=(14, 8))
ax = sns.heatmap(
    win_rates,
    annot=True,            # 显示数值
    fmt=".2f",             # 数值格式为两位小数
    cmap=create_custom_colormap(),  # 使用自定义颜色映射
    vmin=0, vmax=1,        # 固定颜色范围
    linewidths=0.8,        # 单元格边框粗细
    linecolor='#444444',   # 边框颜色
    annot_kws={"size": 12, "weight": "bold", "color": "black"},  # 数值标签样式
    cbar_kws={'label': ' ', 'shrink': 0.8}  # 颜色条设置
)

ax.set_xticklabels(player2_algorithms, rotation=25, ha="right", fontsize=12)
ax.set_yticklabels(player1_algorithms, rotation=0, fontsize=12, fontweight='bold')

plt.title(" Player1 vs Player2 Agent", fontsize=16, pad=20, fontweight='bold')
plt.xlabel("Player2 ", fontsize=14, labelpad=15)
plt.ylabel("Player1 ", fontsize=14, labelpad=15)
for i in range(min(len(player1_algorithms), len(player2_algorithms))):
    ax.add_patch(plt.Rectangle((i, i), 1, 1, fill=False, edgecolor='blue', lw=1.5, linestyle='--'))
ax.hlines([1, 2, 3], *ax.get_xlim(), colors='gray', linestyles='dashed', linewidth=0.5, alpha=0.7)
ax.vlines([1, 2, 3, 4, 5, 6, 7], *ax.get_ylim(), colors='gray', linestyles='dashed', linewidth=0.5, alpha=0.7)
plt.figtext(0.5, 0.01, "", 
            ha="center", fontsize=10, color="#555555")
plt.tight_layout(rect=[0, 0.03, 1, 0.95])
plt.savefig('algorithm_win_rates.png', dpi=300, bbox_inches='tight')
plt.show()