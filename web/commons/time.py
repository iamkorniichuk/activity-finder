from datetime import time as BaseTime, timedelta, datetime


class TimeWrapper(BaseTime):
    def __new__(cls, time):
        return super().__new__(
            cls,
            time.hour,
            time.minute,
            time.second,
            time.microsecond,
            tzinfo=time.tzinfo,
        )

    def __add__(self, other):
        if isinstance(other, timedelta):
            result = datetime.combine(datetime.today(), self) + other
            return TimeWrapper(result.time())

        raise TypeError("Unsupported type")

    def __sub__(self, other):
        if isinstance(other, timedelta):
            result = datetime.combine(datetime.today(), self) - other
            return TimeWrapper(result.time())
        elif isinstance(other, BaseTime):
            minuend = datetime.combine(datetime.today(), self)
            subtrahend = datetime.combine(datetime.today(), other)
            return minuend - subtrahend
        raise TypeError("Unsupported type")

    def total_seconds(self):
        hours = self.hour * 60 * 60
        minutes = self.minute * 60
        seconds = self.second
        return hours + minutes + seconds
