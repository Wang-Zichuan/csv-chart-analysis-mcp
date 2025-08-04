# 📊 CSV图表分析MCP服务器

一个基于MCP协议的高性能CSV数据可视化服务器，支持多种图表类型和统计分析。

## ✨ 特性

- **多图表支持**: 直方图、箱线图、小提琴图、散点图、热力图、双轴折线图等
- **统计分析**: 相关性分析、正态性检验、类别变量分析
- **MCP协议**: 基于FastMCP实现，支持标准化通信
- **中文友好**: 完整的中文文档和注释
- **易于扩展**: 模块化设计，易于添加新的图表类型

## 📦 安装

### 使用pip安装
```bash
pip install csv-chart-mcp
```

### 从源码安装
```bash
git clone https://github.com/yourusername/csv-chart-mcp.git
cd csv-chart-mcp
pip install -e .
```

### 使用uv安装
```bash
uv add csv-chart-mcp
```

## 🚀 快速开始

### 作为MCP服务器运行
```bash
python server.py
```

### 使用示例

#### 1. 单变量分析
```python
from function.单变量 import generate_single_column_plots

result = generate_single_column_plots(
    csv_path="data.csv",
    y_column="temperature",
    save_dir="./charts"
)
```

#### 2. 相关性分析
```python
from function.多变量相关性 import generate_scatter_plot

result = generate_scatter_plot(
    csv_path="data.csv",
    x_column="temperature",
    y_column="sales",
    save_dir="./charts"
)
```

#### 3. 类别变量分析
```python
from function.类别型变量 import analyze_categorical_column

result = analyze_categorical_column(
    csv_path="data.csv",
    y_column="position",
    save_dir="./charts"
)
```

## 📋 MCP工具列表

| 工具名称 | 功能描述 | 输入参数 |
|---------|----------|----------|
| `analyze_single_variable` | 单变量统计分析 | csv_path, y_column, save_dir |
| `analyze_correlation` | 双变量相关性分析 | csv_path, x_column, y_column, save_dir |
| `analyze_categorical` | 类别变量分析 | csv_path, y_column, save_dir |
| `generate_heatmap` | 相关系数热力图 | csv_path, numeric_columns, save_dir |
| `create_scatter_plot` | 散点图生成 | csv_path, y_column, x_column, save_dir |
| `analyze_numeric_categorical` | 数值vs类别分析 | csv_path, numeric_col, category_col, save_dir |
| `create_line_plot` | 折线图生成 | csv_path, column_name, save_dir |
| `create_dual_axis_plot` | 双轴折线图 | csv_path, y1_column, y2_column, x_column, save_dir |
| `create_qq_plot` | QQ图和正态性检验 | csv_path, y_column, save_dir |

## 🔧 配置

### 配置文件示例 (config.json)
```json
{
  "default_save_dir": "./charts",
  "figure_size": [12, 8],
  "color_palette": "Set2",
  "font_family": "SimHei"
}
```

## 📊 支持的图表类型

### 单变量分析
- 📈 直方图 (Histogram)
- 🎯 核密度估计图 (KDE)
- 📦 箱线图 (Boxplot)
- 🎻 小提琴图 (Violin plot)

### 双变量分析
- 📍 散点图 (Scatter plot)
- 📉 折线图 (Line plot)
- 🔄 双轴折线图 (Dual axis line plot)

### 多变量分析
- 🔥 相关系数热力图 (Correlation heatmap)
- 📊 数值vs类别变量分析

### 统计分析
- 📐 QQ图 (Q-Q plot)
- ✅ 正态性检验 (Normality test)

## 🧪 测试数据

项目包含多个测试数据集：
- `test_categorical.csv` - 类别变量测试数据
- `test_correlation.csv` - 相关性分析测试数据
- `test_dual_axis.csv` - 双轴图表测试数据
- `test_group_diff.csv` - 组间差异测试数据
- `test_scatter.csv` - 散点图测试数据

## 🤝 贡献

我们欢迎所有形式的贡献！

### 开发环境设置
```bash
git clone https://github.com/yourusername/csv-chart-mcp.git
cd csv-chart-mcp
pip install -e ".[dev]"
```

### 运行测试
```bash
pytest tests/
```

### 代码风格
我们使用black和isort进行代码格式化：
```bash
black .
isort .
```

## 📄 许可证

MIT License - 详见 [LICENSE](LICENSE) 文件

## 🙏 致谢

- [FastMCP](https://github.com/jlowin/fastmcp) - 优秀的MCP服务器框架
- [Pandas](https://pandas.pydata.org/) - 数据处理
- [Matplotlib](https://matplotlib.org/) - 图表绘制
- [Seaborn](https://seaborn.pydata.org/) - 统计图表

## 📞 联系方式

- 📧 邮箱: your.email@example.com
- 🐛 问题反馈: [GitHub Issues](https://github.com/yourusername/csv-chart-mcp/issues)
- 💡 功能建议: [GitHub Discussions](https://github.com/yourusername/csv-chart-mcp/discussions)