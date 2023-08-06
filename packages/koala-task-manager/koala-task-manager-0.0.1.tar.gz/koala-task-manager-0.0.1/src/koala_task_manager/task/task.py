from datetime import datetime, timedelta
from dataclasses import dataclass, field


@dataclass
class Task:
    function: callable
    task_id: str
    kwargs: dict = None
    start_datetime: datetime = field(init=False)
    end_datetime: datetime = field(init=False)
    duration: timedelta = field(init=False)
    success: bool = field(init=False)
    msg: str = field(init=False)

    def run(self) -> dict:
        self.start_datetime = datetime.now()

        try:
            if self.kwargs:
                self.function(**self.kwargs)
            else:
                self.function()
        except Exception as err:
            self.success = False
            self.msg = f"{self.task_id} failed! Error: {str(err)}"
        else:
            self.success = True
            self.msg = f"{self.task_id} a was success!"

        self.end_datetime = datetime.now()
        self.duration = self.end_datetime - self.start_datetime

        return {
            "task_id": self.task_id,
            "success": self.success,
            "message": self.msg,
            "start_datetime": self.start_datetime.strftime("%Y-%m-%d %H:%M:%S"),
            "end_datetime": self.end_datetime.strftime("%Y-%m-%d %H:%M:%S"),
            "duration": self.duration.seconds}
