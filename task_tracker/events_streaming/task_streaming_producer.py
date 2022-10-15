from py_lib import DataStreamingProducer

from task_tracker.task.models import Task
from task_tracker.events.task import (
    TaskEvent,
    TaskEventType,
)


def task_to_event_data(task: Task):
    data = {
        "public_id": str(task.public_id),
        "user_id": str(task.user_id),
        "title": task.title,
        "description": task.description,
        "status": task.status,
        "created_at": task.created_at.isoformat(),
        "updated_at": task.updated_at.isoformat(),
    }
    if task.meta:
        data["meta"] = task.meta
    return data


class TaskStreamingProducer(DataStreamingProducer):
    def send_event(self, task: Task, event_type: TaskEventType):
        event = TaskEvent(
            event_name=event_type,
            producer=self.name,
            data=task_to_event_data(task),
        )
        self.validate_event(event)
        self.produce_event(event)
        return
