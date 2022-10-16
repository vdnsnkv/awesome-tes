import uuid

from .models import Task


class TaskRepo:
    def __init__(self, db):
        self.db = db

    def add_task(
        self,
        title: str,
        desc: str,
        user_id: uuid.UUID,
    ):
        task = Task(
            title=title,
            description=desc,
            user_id=user_id,
        )
        self.db.session.add(task)
        self.db.session.commit()
        return task

    def get_task(self, public_id: str):
        return (
            self.db.session.query(Task)
            .filter(
                Task.public_id == uuid.UUID(public_id),
            )
            .first()
        )

    def get_all_tasks(self):
        return self.db.session.query(Task).all()

    def update_task(self, task: Task, status: str = None, user_id: uuid.UUID = None):
        if status is not None:
            status = Task.Status(status)
            task.status = status.value
        if user_id is not None:
            task.user_id = user_id
        self.db.session.add(task)
        self.db.session.commit()
        return task
