from datetime import datetime
from dateutil.relativedelta import relativedelta
from .schemas.userAge import userAge

def calcAge(day: int, month: int, year: int) -> userAge:
    birthDate = datetime(year, month, day)
    today = datetime.today()
    age = relativedelta(today, birthDate)
    return userAge(age.years, age.months, age.days)
