from py_lib import DataStreamingProducer

from task_tracker.task.models import Task
from task_tracker.events.task import (
    TaskEvent,
    TaskEventType,
)


def task_to_event_data_v1(task: Task):
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


def task_to_event_data_v2(task: Task):
    data = {
        "public_id": str(task.public_id),
        "user_id": str(task.user_id),
        "title": task.title,
        "jira_id": task.jira_id,
        "description": task.description,
        "status": task.status,
        "created_at": task.created_at.isoformat(),
        "updated_at": task.updated_at.isoformat(),
    }
    if task.meta:
        data["meta"] = task.meta
    return data


class TaskStreamingProducer(DataStreamingProducer):
    def send_event(self, task: Task, event_type: TaskEventType, event_version: int = 1):
        if event_version == 1:
            task_to_event_data = task_to_event_data_v1
        if event_version == 2:
            task_to_event_data = task_to_event_data_v2

        event = TaskEvent(
            event_name=event_type,
            event_version=event_version,
            producer=self.name,
            data=task_to_event_data(task),
        )
        self.validate_event(event)
        self.produce_event(event)
        return
