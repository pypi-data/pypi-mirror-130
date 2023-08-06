# -*- coding: utf-8 -*-
from outflow.core.tasks import Task, TaskManager


class IOChecker(TaskManager):
    def run(self, task: Task, task_inputs):
        task.check_inputs(task_inputs)

    def post_process(self, task, task_return_value):
        return {key: None for key in task.outputs.keys()}
