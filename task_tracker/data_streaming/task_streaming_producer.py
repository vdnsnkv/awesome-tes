from py_lib import DataStreamingProducer

from task_tracker.task.models import Task
from task_tracker.events.task_streaming import (
    TaskStreamingEvent,
    TaskStreamingEventType,
)


class TaskStreamingProducer(DataStreamingProducer):
    def send_event(self, task: Task, event_type: TaskStreamingEventType):
        event = TaskStreamingEvent(
            event_name=event_type,
            data=task.to_dict(),
        )
        self.produce_event(event)
        return
