# Notion 项目管理集成

这个工具用于将Code Rogue项目的任务自动同步到Notion数据库。

## 准备工作

1. 在Notion中创建集成：
   - 访问 [Notion Integrations](https://www.notion.so/my-integrations)
   - 点击"New integration"
   - 填写名称（如"CodeRogue Dev"）
   - 复制"Internal Integration Token"（以`secret_`开头）

2. 创建数据库：
   - 在Notion中创建新页面
   - 选择"Table"视图
   - 添加以下列：
     - Name (Title)
     - Status (Select: Todo, In Progress, Review, Done)
     - Priority (Select: High, Medium, Low)
     - Type (Select: Design, Development, Art, Sound, UI/UX)
     - Due Date (Date)
     - Labels (Multi-select)

3. 分享数据库给集成：
   - 点击数据库右上角的"..."
   - 选择"Add connections"
   - 选择您创建的集成

## 安装

1. 克隆仓库（如果尚未克隆）
2. 安装依赖：
   ```bash
   pip install -r requirements.txt
   ```
3. 配置环境变量：
   - 复制`.env.example`文件并重命名为`.env`
   - 在`.env`中填入您的Notion集成token和数据库ID

## 使用

1. 运行以下命令初始化任务：
   ```bash
   python notion_manager.py
   ```

## 命令

- `python notion_manager.py` - 初始化默认任务列表
- 您也可以导入`NotionManager`类到自己的脚本中使用

## 故障排除

- 如果遇到权限错误，请确保：
  - 集成已被添加到数据库
  - 集成具有正确的权限
  - 数据库ID和token输入正确

## 注意事项

- 请勿将`.env`文件提交到版本控制
- 定期备份您的Notion数据
