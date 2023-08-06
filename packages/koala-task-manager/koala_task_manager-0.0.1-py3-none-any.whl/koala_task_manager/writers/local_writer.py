import json

from koala_task_manager.writers.base_writer import BaseWriter


class LocalWriter(BaseWriter):
    def __init__(self, path: str = "report.json"):
        super().__init__(name="local_writer")
        self._path = path

    def write(self, report: dict):
        with open(self._path, "w+") as f:
            f.write(json.dumps(report))
