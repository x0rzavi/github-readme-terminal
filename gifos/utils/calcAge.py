from datetime import datetime
from dateutil.relativedelta import relativedelta

def calcAge(day: int, month: int, year: int) -> tuple:
    birthDate = datetime(year, month, day)
    today = datetime.today()
    age = relativedelta(today, birthDate)
    return age.years, age.months, age.days