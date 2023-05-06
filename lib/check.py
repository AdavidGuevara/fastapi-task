from models.task import Task
from conn.connection import SessionLocal

db = SessionLocal()

def check_title(title):
    respuesta = False
    task_list = db.query(Task).all()
    for task in task_list:
        if task.title == title:
            respuesta = True
            break
    return respuesta