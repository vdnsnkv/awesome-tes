from py_lib import DataStreamingConsumer, Event

from accounting_service.accounting import (
    deposit_money_to_user_account,
    withdraw_money_from_user_account,
)

from .task import TaskEventType


class TaskConsumer(DataStreamingConsumer):
    def process_events(self, event: Event):
        print(event.event_name)
        # data streaming
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

        # business events
        if (
            event.event_name == TaskEventType.TaskAdded
            or event.event_name == TaskEventType.TaskAssigned
        ):
            with self.app.app_context():
                task = self.app.task_repo.get_task(event.data["public_id"])
                if task is None:
                    task = self.app.task_repo.add_task(event.data)

                print(task)

                user = self.app.user_repo.get_user(event.data["user_id"])
                if user is None:
                    user = self.app.user_repo.add_user(
                        {"public_id": event.data["user_id"]}
                    )

                print(user)

                withdraw_money_from_user_account(
                    user, task.assign_price, task.public_id
                )

            return

        if event.event_name == TaskEventType.TaskDone:
            with self.app.app_context():
                task = self.app.task_repo.get_task(event.data["public_id"])

                user = self.app.user_repo.get_user(event.data["user_id"])

                deposit_money_to_user_account(user, task.done_price, task.public_id)

            return

        return
