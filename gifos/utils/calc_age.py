from datetime import datetime
from dateutil.relativedelta import relativedelta

from gifos.utils.schemas.user_age import UserAge


def calc_age(day: int, month: int, year: int) -> UserAge:
    birth_date = datetime(year, month, day)
    today = datetime.today()
    age = relativedelta(today, birth_date)
    return UserAge(age.years, age.months, age.days)
