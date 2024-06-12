from datetime import datetime


def format_date(date: datetime) -> str:
    """Format date for table

    Args:
        date (datetime): date to format

    Returns:
        str: date in format `12:34`
    """

    return date.strftime("%H:%M")


def format_duration(start: datetime, end: datetime) -> str:
    start = format_date(start)
    end = format_date(end)
    duration = f"{start} - {end}"
    return duration


def datetime_from_time(time: str) -> datetime:
    hour, minute = time.split(":")
    hour, minute = int(hour), int(minute)

    now = datetime.now()
    dt = datetime(now.year, now.month, now.day, hour=hour, minute=minute)

    return dt
