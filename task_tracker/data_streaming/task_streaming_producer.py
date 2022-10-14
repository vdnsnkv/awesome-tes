from py_lib import DataStreamingProducer

from task_tracker.task.models import Task
from task_tracker.events.task_streaming import TaskCUDEvent, TaskCUDEventType


class TaskStreamingProducer(DataStreamingProducer):
    def send_event(self, task: Task, event_type: TaskCUDEventType):
        event = TaskCUDEvent(
            event_name=event_type,
            data=task.to_dict(),
        )
        super().produce_event(event)
        return
