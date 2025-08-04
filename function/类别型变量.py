import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
from typing import Dict, Any, Optional

def analyze_categorical_column(
    csv_path: str,
    y_column: str,
    save_dir: str = "./charts",
    top_n: Optional[int] = None,
    min_freq: int = 1
) -> Dict[str, Any]:
    """
    分析类别型变量的分布特征，生成条形图和饼图

    参数:
        csv_path: CSV文件路径
        y_column: 要分析的分类型列名
        save_dir: 图片保存目录，默认为'./charts'
        top_n: 仅显示频率最高的前n个类别（可选）
        min_freq: 显示最小频数阈值（可选）

    返回:
        包含图表路径和统计信息的字典
    """
    try:
        # 读取CSV文件
        df = pd.read_csv(csv_path)
        
        # 检查列是否存在
        if y_column not in df.columns:
            return {"error": f"列 '{y_column}' 不存在于CSV文件中", "success": False}
        
        # 确保保存目录存在
        os.makedirs(save_dir, exist_ok=True)
        
        # 设置中文字体支持
        plt.rcParams['font.sans-serif'] = ['SimHei', 'DejaVu Sans']
        plt.rcParams['axes.unicode_minus'] = False
        
        # 获取文件名用于命名
        file_name = os.path.splitext(os.path.basename(csv_path))[0]
        
        # 计算频数
        value_counts = df[y_column].value_counts()
        
        # 应用过滤条件
        if min_freq > 1:
            value_counts = value_counts[value_counts >= min_freq]
        
        if top_n is not None:
            value_counts = value_counts.head(top_n)
        
        # 创建图表
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 8))
        
        # 条形图
        bars = ax1.bar(value_counts.index, value_counts.values)
        ax1.set_title(f'{y_column} - 类别分布（条形图）')
        ax1.set_xlabel(y_column)
        ax1.set_ylabel('频数')
        ax1.tick_params(axis='x', rotation=45)
        
        # 添加数值标签
        for bar in bars:
            height = bar.get_height()
            ax1.text(bar.get_x() + bar.get_width()/2., height,
                    f'{int(height)}', ha='center', va='bottom')
        
        # 饼图
        ax2.pie(value_counts.values, labels=value_counts.index, autopct='%1.1f%%')
        ax2.set_title(f'{y_column} - 类别分布（饼图）')
        
        # 保存图表
        save_path = os.path.join(save_dir, f'{file_name}_{y_column}_categorical.png')
        plt.tight_layout()
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        plt.close()
        
        # 计算统计摘要
        total_count = len(df[y_column])
        unique_count = df[y_column].nunique()
        most_common = value_counts.index[0] if len(value_counts) > 0 else None
        most_common_count = value_counts.iloc[0] if len(value_counts) > 0 else 0
        
        summary_stats = f"""
        总样本数: {total_count}
        唯一类别数: {unique_count}
        最常见类别: {most_common} ({most_common_count}次, {most_common_count/total_count*100:.1f}%)
        缺失值数量: {df[y_column].isnull().sum()}
        """
        
        # 创建频数表
        frequency_table = value_counts.reset_index()
        frequency_table.columns = [y_column, '频数']
        frequency_table['百分比'] = (frequency_table['频数'] / total_count * 100).round(2)
        
        return {
            "success": True,
            "barplot_path": save_path,
            "piechart_path": save_path,
            "frequency_table": frequency_table.to_string(index=False),
            "summary_stats": summary_stats.strip(),
            "total_categories": unique_count,
            "most_frequent_category": most_common
        }
        
    except Exception as e:
        return {"error": str(e), "success": False}

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 2:
        result = analyze_categorical_column(sys.argv[1], sys.argv[2])
        print(result)
    else:
        print("用法: python 类别型变量.py <csv文件路径> <列名>")