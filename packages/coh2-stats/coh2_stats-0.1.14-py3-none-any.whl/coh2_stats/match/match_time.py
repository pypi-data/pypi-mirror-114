from coh2_stats.utils.logger import Logger
import datetime

class MatchTime:
    def __init__(self, start_time, end_time):
        self.start_time = start_time
        self.end_time = end_time
        self.duration = end_time - start_time

        self.match_time = self.get_matchstart_datetime()

    def get_datetime_from_seconds(self, seconds):
        return datetime.datetime.fromtimestamp(seconds)

    def get_matchstart_datetime(self):
        return self.get_datetime_from_seconds(self.start_time)

    def date(self):
        return self.get_matchstart_datetime().strftime("%Y-%m-%d")

    def __repr__(self) -> str:
        return f"{self.date()},{datetime.timedelta(seconds=self.duration)}"

    def in_range(self, start: datetime.datetime, end: datetime.datetime)-> bool:
        if end < start:
            Logger("invalid matchtime range")
            return False

        time = self.get_matchstart_datetime()
        return time >= start and time <= end

    def in_range_date(self, start: tuple = (1, 1), end: tuple = (12, 31), year=2021):
        start_date = datetime.datetime(year, start[0], start[1], 0, 0)
        end_date   = datetime.datetime(year, end[0],   end[1], 23, 59)
        return self.in_range(start_date, end_date)


