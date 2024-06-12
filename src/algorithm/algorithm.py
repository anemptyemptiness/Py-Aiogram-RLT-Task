from datetime import datetime, timedelta

from typing import Tuple


def algorithm(
        dt_from: str,
        dt_upto: str,
        group_type: str,
) -> Tuple[list[datetime], dict]:
    dt_from: datetime = datetime.strptime(dt_from, "%Y-%m-%dT%H:%M:%S")
    dt_upto: datetime = datetime.strptime(dt_upto, "%Y-%m-%dT%H:%M:%S")

    dates: list = list()
    months: dict = {
        1: 31, 2: 28, 3: 31, 4: 30, 5: 31, 6: 30, 7: 31, 8: 31, 9: 30, 10: 31, 11: 30, 12: 31,
    }
    seconds_in_hour = 3600
    seconds_in_day = seconds_in_hour * 24

    total_needed_time = (dt_upto - dt_from).total_seconds()

    while total_needed_time > 0:
        dates.append(dt_from)

        if group_type == "hour":
            dt_from += timedelta(hours=1)

            if total_needed_time - seconds_in_hour == 0:
                total_needed_time -= seconds_in_hour
                dates.append(dt_from)

                dt_from += timedelta(hours=1)
                dates.append(dt_from)
            else:
                total_needed_time -= seconds_in_hour

        if group_type == "day":
            dt_from += timedelta(days=1)

            if total_needed_time - seconds_in_day < 0:
                total_needed_time -= total_needed_time
                dates.append(dt_from)
            else:
                total_needed_time -= seconds_in_day

        if group_type == "month":
            dt_from += timedelta(days=months[dt_from.month])
            seconds_in_month = seconds_in_day * months[dt_from.month]

            if total_needed_time - seconds_in_month < 0:
                total_needed_time -= total_needed_time
                dates.append(dt_from)
            else:
                total_needed_time -= seconds_in_month

    return dates, months
