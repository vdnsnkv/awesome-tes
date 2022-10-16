from py_lib import DataStreamingProducer

from task_tracker.task.models import Task
from task_tracker.events.task import (
    TaskEvent,
    TaskEventType,
)


def task_to_event_data(task: Task, event_type: TaskEventType):
    if event_type == TaskEventType.TaskAdded:
        return {
            "public_id": str(task.public_id),
            "user_id": str(task.user_id),
            "title": task.title,
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
    def send_event(self, task: Task, event_type: TaskEventType):
        event = TaskEvent(
            event_name=event_type,
            producer=self.name,
            data=task_to_event_data(task, event_type),
        )
        self.validate_event(event)
        self.produce_event(event)
        return
