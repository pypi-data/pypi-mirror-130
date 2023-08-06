from dataclasses import dataclass
from datetime import datetime, timedelta


@dataclass
class Pilot(object):
    racer_name: str = None
    start_time: datetime = None
    company: str = None
    end_time: datetime = None

    @property
    def lap_time(self):

        if self.start_time and self.end_time and self.end_time >= self.start_time:
            return self.end_time - self.start_time
