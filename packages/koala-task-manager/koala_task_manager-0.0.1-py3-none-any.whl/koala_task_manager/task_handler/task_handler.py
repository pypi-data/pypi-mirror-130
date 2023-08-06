from typing import List
from datetime import datetime, timedelta
from dataclasses import dataclass, field

from koala_task_manager.task import Task
from koala_task_manager.writers import BaseWriter


@dataclass
class TaskHandler:
    name: str
    writer: BaseWriter
    tasks: List[Task] = None
    reports: List[dict] = field(init=False)
    task_ids: List[str] = field(init=False)
    start_datetime: datetime = field(init=False)
    end_datetime: datetime = field(init=False)
    duration: timedelta = field(init=False)
    success: bool = field(init=False)

    def __post_init__(self):
        self.success = True
        self.reports = []
        self.task_ids = []
        if not self.tasks:
            self.tasks = []

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb, *args):
        self.run_tasks()

    def run_tasks(self) -> None:
        self.start_datetime = datetime.now()
        self._run_tasks()
        self.end_datetime = datetime.now()

        self.duration = self.end_datetime - self.start_datetime

        report = self._generate_report()
        self.writer.write(report=report)

    def add_task(self, function: callable, task_id: str,  kwargs: dict = None):
        task = Task(function=function, task_id=task_id, kwargs=kwargs)
        self.tasks.append(task)

    def _run_tasks(self):
        for task in self.tasks:
            current_report = task.run()
            self.task_ids.append(task.task_id)
            self.reports.append(current_report)
            if not task.success:
                self.success = False

    def _generate_report(self):
        return {
            "name": self.name,
            "task_ids": self.task_ids,
            "success": self.success,
            "start_datetime": self.start_datetime.strftime("%Y-%m-%d %H:%M:%S"),
            "end_datetime": self.end_datetime.strftime("%Y-%m-%d %H:%M:%S"),
            "duration": self.duration.seconds,
            "reports": self.reports
        }
