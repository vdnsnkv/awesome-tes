from py_lib import DataStreamingConsumer, Event

from .task import TaskEventType


class TaskConsumer(DataStreamingConsumer):
    def process_events(self, event: Event):

        if event.event_name == TaskEventType.Updated:
            with self.app.app_context():
                task = self.app.task_repo.get_task(event.data["public_id"])
                self.app.task_repo.update_task(task, event.data)
            return

        if event.event_name == TaskEventType.Created:
            with self.app.app_context():
                task = self.app.task_repo.get_task(event.data["public_id"])
                if task is not None:
                    self.app.task_repo.update_task(task, event.data)
                    return
                self.app.task_repo.add_task(event.data)
            return

        return
