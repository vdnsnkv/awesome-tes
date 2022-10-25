from py_lib import DataStreamingProducer

from task_tracker.task.models import Task
from task_tracker.events.task import (
    TaskEvent,
    TaskEventType,
)


def task_to_event_data(task: Task, event_type: TaskEventType, event_version: int):
    if (event_type, event_version) == (TaskEventType.TaskAdded, 1):
        return {
            "public_id": str(task.public_id),
            "user_id": str(task.user_id),
            "title": task.title,
        }
    if (event_type, event_version) == (TaskEventType.TaskAdded, 2):
        return {
            "public_id": str(task.public_id),
            "user_id": str(task.user_id),
            "title": task.title,
            "jira_id": task.jira_id,
        }

    if event_type == TaskEventType.TaskAssigned:
        return {
            "public_id": str(task.public_id),
            "user_id": str(task.user_id),
        }
    if event_type == TaskEventType.TaskDone:
        return {
            "public_id": str(task.public_id),
            "user_id": str(task.user_id),
        }
    return


class TaskProducer(DataStreamingProducer):
    def send_event(self, task: Task, event_type: TaskEventType, event_version: int = 1):
        event = TaskEvent(
            event_name=event_type,
            event_version=event_version,
            producer=self.name,
            data=task_to_event_data(task, event_type, event_version),
        )
        self.validate_event(event)
        self.produce_event(event)
        return
