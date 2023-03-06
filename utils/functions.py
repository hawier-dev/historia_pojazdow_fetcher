import datetime


def get_all_dates(year: int) -> list:
    start_date = datetime.date(year, 1, 1)
    end_date = datetime.date(year, 12, 31)

    delta = datetime.timedelta(days=1)
    dates = []

    while start_date <= end_date:
        dates.append(start_date.strftime("%d.%m.%Y"))
        start_date += delta

    return dates
