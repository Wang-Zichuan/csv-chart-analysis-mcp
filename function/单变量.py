import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
from typing import Dict, Any

def generate_single_column_plots(
    csv_path: str,
    y_column: str,
    save_dir: str = "./charts"
) -> str:
    """
    从CSV文件中读取指定列数据，并生成四种统计图表：
    1. 直方图
    2. 核密度估计图
    3. 箱线图
    4. 小提琴图

    参数:
        csv_path: CSV文件路径
        y_column: 需要分析的数值列名
        save_dir: 图片保存目录，默认为'./charts'

    返回:
        成功信息字符串
    """
    try:
        # 读取CSV文件
        df = pd.read_csv(csv_path)
        
        # 检查列是否存在
        if y_column not in df.columns:
            return f"错误：列 '{y_column}' 不存在于CSV文件中"
        
        # 确保保存目录存在
        os.makedirs(save_dir, exist_ok=True)
        
        # 设置中文字体支持
        plt.rcParams['font.sans-serif'] = ['SimHei', 'DejaVu Sans']
        plt.rcParams['axes.unicode_minus'] = False
        
        # 获取文件名（不含扩展名）用于命名
        file_name = os.path.splitext(os.path.basename(csv_path))[0]
        
        # 1. 直方图
        plt.figure(figsize=(12, 8))
        plt.subplot(2, 2, 1)
        plt.hist(df[y_column], bins=30, edgecolor='black', alpha=0.7)
        plt.title(f'{y_column} - 直方图')
        plt.xlabel(y_column)
        plt.ylabel('频数')
        
        # 2. 核密度估计图
        plt.subplot(2, 2, 2)
        sns.kdeplot(data=df[y_column], fill=True)
        plt.title(f'{y_column} - 核密度估计图')
        plt.xlabel(y_column)
        
        # 3. 箱线图
        plt.subplot(2, 2, 3)
        plt.boxplot(df[y_column])
        plt.title(f'{y_column} - 箱线图')
        plt.ylabel(y_column)
        
        # 4. 小提琴图
        plt.subplot(2, 2, 4)
        sns.violinplot(y=df[y_column])
        plt.title(f'{y_column} - 小提琴图')
        plt.ylabel(y_column)
        
        # 调整布局并保存
        plt.tight_layout()
        save_path = os.path.join(save_dir, f'{file_name}_{y_column}_analysis.png')
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        plt.close()
        
        # 计算基本统计信息
        stats = df[y_column].describe()
        
        # 计算额外统计量
        skewness = df[y_column].skew()
        kurtosis = df[y_column].kurtosis()
        
        # 创建统计信息字符串
        stats_str = f"""
        基本统计信息:
        {stats}
        
        偏度: {skewness:.4f}
        峰度: {kurtosis:.4f}
        
        图表已保存至: {save_path}
        """
        
        return stats_str.strip()
        
    except Exception as e:
        return f"错误: {str(e)}"

if __name__ == "__main__":
    # 测试代码
    import sys
    if len(sys.argv) > 2:
        result = generate_single_column_plots(sys.argv[1], sys.argv[2])
        print(result)
    else:
        print("用法: python 单变量.py <csv文件路径> <列名>")