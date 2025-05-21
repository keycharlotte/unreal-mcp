import os
from datetime import datetime, timedelta
from notion_client import Client
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

class NotionDailyUpdate:
    def __init__(self):
        self.notion = Client(auth=os.getenv('NOTION_TOKEN'))
        self.database_id = os.getenv('DATABASE_ID')
        
        if not self.database_id:
            raise ValueError("DATABASE_ID not found in .env file")

    def get_today_tasks(self):
        """获取今天的任务"""
        today = datetime.now().date()
        tomorrow = today + timedelta(days=1)
        
        # 查询今天到期的任务
        response = self.notion.databases.query(
            **{
                "database_id": self.database_id,
                "filter": {
                    "and": [
                        {"property": "Due Date", "date": {"on_or_after": today.isoformat()}},
                        {"property": "Due Date", "date": {"before": tomorrow.isoformat()}}
                    ]
                }
            }
        )
        return response.get('results', [])

    def update_task_status(self, task_id, status):
        """更新任务状态"""
        self.notion.pages.update(
            page_id=task_id,
            properties={
                "Status": {"select": {"name": status}}
            }
        )

def main():
    try:
        print("开始每日任务更新...")
        updater = NotionDailyUpdate()
        
        # 获取今天的任务
        tasks = updater.get_today_tasks()
        print(f"找到 {len(tasks)} 个今日任务")
        
        for task in tasks:
            task_id = task['id']
            task_name = task['properties']['Name']['title'][0]['plain_text']
            print(f"处理任务: {task_name}")
            
            # 这里可以添加更多自动化逻辑
            # 例如：自动将到期的任务状态更新为"进行中"
            # updater.update_task_status(task_id, "进行中")
        
        print("每日任务更新完成！")
        
    except Exception as e:
        print(f"发生错误: {str(e)}")
        raise

if __name__ == "__main__":
    main()
