import uuid

from .models import Task


def _filter_data(data: dict):
    return {k: v for k, v in data.items() if k in Task.__table__.c}


class TaskRepo:
    def __init__(self, db):
        self.db = db

    def add_task(self, data: dict):
        task = Task(**_filter_data(data))
        self.db.session.add(task)
        self.db.session.commit()
        return task

    def get_task(self, public_id: str):
        return self.db.session.query(Task).get(uuid.UUID(public_id))

    def get_all_tasks(self):
        return self.db.session.query(Task).all()

    def get_tasks(self, task_ids: list[str]):
        return (
            self.db.session.query(Task)
            .filter(
                Task.public_id.in_([uuid.UUID(tid) for tid in task_ids]),
            )
            .all()
        )

    def update_task(self, task, data: dict):
        for k, v in _filter_data(data).items():
            setattr(task, k, v)
        self.db.session.add(task)
        self.db.session.commit()
        return task
