from confluent_kafka import Message

from py_lib import DataStreamingConsumer

from .task_streaming import TaskCUDEventType


class TaskStreamingConsumer(DataStreamingConsumer):
    def process_events(self, event: Message):
        if event.event_name == TaskCUDEventType.Updated:
            with self.app.app_context():
                task = self.app.task_repo.get_task(event.data["public_id"])
                self.app.task_repo.update_task(task, event.data)
        if event.event_name == TaskCUDEventType.Created:
            with self.app.app_context():
                self.app.task_repo.add_task(event.data)
        return
