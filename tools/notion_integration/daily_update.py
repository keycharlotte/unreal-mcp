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
        print(f"正在更新任务 {task_id} 状态为: {status}")
        try:
            self.notion.pages.update(
                page_id=task_id,
                properties={
                    "Status": {"select": {"name": status}}
                }
            )
            print(f"成功更新任务状态: {task_id}")
        except Exception as e:
            print(f"更新任务状态时出错: {str(e)}")
            raise

def mark_completed_tasks(updater, task_titles):
    """标记指定标题的任务为已完成"""
    print(f"开始标记已完成的任务: {task_titles}")
    for title in task_titles:
        print(f"\n处理任务: {title}")
        try:
            # 查找任务
            response = updater.notion.databases.query(
                **{
                    "database_id": updater.database_id,
                    "filter": {
                        "and": [
                            {"property": "Name", "title": {"equals": title}},
                            {"property": "Status", "select": {"does_not_equal": "Done"}}
                        ]
                    }
                }
            )
            
            tasks = response.get('results', [])
            print(f"找到 {len(tasks)} 个匹配的任务")
            
            # 更新找到的任务
            for task in tasks:
                task_id = task['id']
                print(f"标记任务为已完成 - 标题: {title}, ID: {task_id}")
                updater.update_task_status(task_id, "Done")
        except Exception as e:
            print(f"处理任务 '{title}' 时出错: {str(e)}")
            continue

def main():
    try:
        print("开始每日任务更新...")
        updater = NotionDailyUpdate()
        
        # 5月21日已完成的任务
        completed_tasks = [
            "项目初始化",
            "创建玩家角色",
            "实现基础移动控制"
        ]
        
        # 标记已完成的任务
        mark_completed_tasks(updater, completed_tasks)
        
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
