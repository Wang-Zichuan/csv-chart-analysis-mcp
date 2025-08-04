# 贡献指南

感谢您对我们CSV图表分析MCP服务器项目的兴趣！我们欢迎所有形式的贡献，包括代码、文档、测试和反馈。

## 如何贡献

### 报告问题
如果您发现了bug或有功能建议，请通过以下方式提交：

1. 访问项目的[Issues页面](https://github.com/Wang-Zichuan/csv-chart-analysis-mcp/issues)
2. 点击"New Issue"创建新问题
3. 选择合适的issue模板（Bug报告或功能请求）
4. 提供尽可能详细的信息

### 代码贡献

#### 开发环境设置
1. 克隆仓库：
   ```bash
   git clone https://github.com/Wang-Zichuan/csv-chart-analysis-mcp.git
   cd csv-chart-analysis-mcp
   ```

2. 创建虚拟环境：
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   venv\Scripts\activate     # Windows
   ```

3. 安装依赖：
   ```bash
   pip install -e .
   ```

#### 开发流程
1. 创建功能分支：
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. 进行开发并添加测试
3. 确保代码通过测试：
   ```bash
   python -m pytest tests/
   ```

4. 提交代码：
   ```bash
   git add .
   git commit -m "描述性的提交信息"
   ```

5. 推送并创建Pull Request

#### 代码规范
- 遵循PEP 8 Python编码规范
- 添加适当的函数和类注释
- 为新功能编写测试用例
- 保持代码的可读性和可维护性

### 添加新图表类型
如果您想添加新的图表类型：

1. 在`function/`目录下创建新的Python文件
2. 实现标准化的函数接口：
   ```python
   def generate_new_chart_type(
       csv_path: str,
       columns: List[str],
       save_dir: str = "./charts",
       **kwargs
   ) -> Dict[str, Any]:
       # 实现代码
       return {"success": True, "plot_path": "path/to/chart.png"}
   ```

3. 在`server.py`中注册新工具
4. 更新README.md文档
5. 添加示例用法

### 文档贡献
我们欢迎以下文档改进：
- README.md的完善
- 代码注释的补充
- 使用教程的编写
- API文档的更新

### 测试贡献
- 添加单元测试
- 添加集成测试
- 测试不同数据格式的兼容性

## 行为准则

### 我们的承诺
我们致力于为所有人提供一个友好、包容的环境，无论其经验水平、教育背景、性别、性别认同和表达、年龄、国籍、外貌、残疾、种族或宗教。

### 我们的标准
正面行为示例包括：
- 使用欢迎和包容的语言
- 尊重不同的观点和经验
- 优雅地接受建设性批评
- 关注对社区最有利的事情
- 对其他社区成员表示同情

不可接受的行为包括：
- 使用性化语言或图像以及不受欢迎的性关注或性挑逗
- 挑衅、侮辱/贬损评论以及个人或政治攻击
- 公开或私下骚扰
- 未经明确许可发布他人的私人信息，如物理或电子地址
- 其他可以被合理地认为不适当的行为

## 联系信息

如果您有任何问题或需要帮助，请通过以下方式联系我们：
- 创建GitHub Issue
- 发送邮件到：Zichuantju@qq.com

## 致谢

感谢所有为这个项目做出贡献的开发者！

## 许可证

本项目采用MIT许可证，详见[LICENSE](LICENSE)文件。