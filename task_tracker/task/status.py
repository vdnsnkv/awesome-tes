from .models import Task


def is_task_done(task: Task):
    return Task.Status(task.status) == Task.Status.DONE
