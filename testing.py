import calendar
import datetime


def next_even_wednesday(date):
    while date.weekday() != 2 or int(date.strftime('%V')) % 2 != 0:
        date += datetime.timedelta(days=1)

    return f'{date.day}/{date.month}'


if __name__ == '__main__':
    # week_no = int(datetime.datetime.now().strftime('%V'))
    # if week_no % 2 != 0:
    print(next_even_wednesday(datetime.datetime.now()))
    d = datetime.datetime.strptime('30062022', "%d%m%Y").date()
    print(next_even_wednesday(d))
