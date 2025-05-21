import os
from datetime import datetime, timedelta
from dotenv import load_dotenv
from notion_client import Client

# 加载环境变量
load_dotenv()

class NotionManager:
    def __init__(self):
        self.notion = Client(auth=os.getenv('NOTION_TOKEN'))
        self.database_id = os.getenv('DATABASE_ID')
        
        if not self.database_id:
            raise ValueError("DATABASE_ID not found in .env file")

    def create_task(self, title, status="Todo", priority="Medium", task_type="Development", 
                   assignee=None, due_date=None, labels=None):
        """在Notion数据库中创建新任务"""
        properties = {
            "Name": {"title": [{"text": {"content": title}}]},
            "Status": {"select": {"name": status}},
            "Priority": {"select": {"name": priority}},
            "Type": {"select": {"name": task_type}},
        }
        
        if due_date:
            properties["Due Date"] = {"date": {"start": due_date.isoformat()}}
            
        if labels:
            properties["Labels"] = {"multi_select": [{"name": label} for label in labels]}
            
        return self.notion.pages.create(
            parent={"database_id": self.database_id},
            properties=properties
        )

    def setup_initial_tasks(self):
        """设置初始任务列表"""
        today = datetime.now()
        tasks = [
            {"title": "项目初始化", "due_date": today + timedelta(days=1), "labels": ["Core", "Setup"], "status": "Todo"},
            {"title": "创建玩家角色", "due_date": today + timedelta(days=2), "labels": ["Core", "Gameplay"], "status": "Todo"},
            {"title": "实现基础移动控制", "due_date": today + timedelta(days=2), "labels": ["Core", "Gameplay"], "status": "Todo"},
            {"title": "设计游戏主界面", "due_date": today + timedelta(days=1), "labels": ["UI", "Design"], "status": "Todo", "task_type": "Design"},
            {"title": "设计玩家角色", "due_date": today + timedelta(days=1), "labels": ["Art", "Design"], "status": "Todo", "task_type": "Design"},
            {"title": "实现基础攻击机制", "due_date": today + timedelta(days=3), "labels": ["Gameplay", "Combat"], "status": "Todo"},
            {"title": "创建敌人AI", "due_date": today + timedelta(days=3), "labels": ["AI", "Gameplay"], "status": "Todo"},
            {"title": "设计敌人角色", "due_date": today + timedelta(days=2), "labels": ["Art", "Design"], "status": "Todo", "task_type": "Design"},
            {"title": "实现伤害系统", "due_date": today + timedelta(days=4), "labels": ["Gameplay", "Combat"], "status": "Todo"},
            {"title": "设计游戏图标", "due_date": today + timedelta(days=5), "labels": ["UI", "Art"], "status": "Todo", "task_type": "Design"},
            {"title": "添加音效系统", "due_date": today + timedelta(days=6), "labels": ["Audio", "Core"], "status": "Todo"},
            {"title": "设计游戏Logo", "due_date": today + timedelta(days=6), "labels": ["UI", "Art"], "status": "Todo", "task_type": "Design"},
        ]
        
        for task in tasks:
            self.create_task(
                title=task["title"],
                status=task.get("status", "Todo"),
                priority=task.get("priority", "Medium"),
                task_type=task.get("task_type", "Development"),
                due_date=task.get("due_date"),
                labels=task.get("labels", [])
            )
        print("✅ 初始任务已成功添加到Notion数据库")

if __name__ == "__main__":
    try:
        manager = NotionManager()
        print("正在连接到Notion...")
        manager.setup_initial_tasks()
    except Exception as e:
        print(f"❌ 发生错误: {str(e)}")
        print("\n请检查：")
        print("1. 是否已创建.env文件并设置了NOTION_TOKEN和DATABASE_ID")
        print("2. 集成是否有权限访问数据库")
        print("3. 网络连接是否正常")
        print("\n如需帮助，请参考README.md中的说明")
