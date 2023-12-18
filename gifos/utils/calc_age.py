from datetime import datetime
from dateutil.relativedelta import relativedelta

from gifos.utils.schemas.user_age import UserAge

"""This module contains a utility function for calculating a person's age."""


def calc_age(day: int, month: int, year: int) -> UserAge:
    """Calculate the age of a person given their birth date.

    :param day: The day of the month the person was born (1-31).
    :type day: int
    :param month: The month the person was born (1-12).
    :type month: int
    :param year: The year the person was born.
    :type year: int
    :return: An object containing the person's age in years, months, and days.
    :rtype: UserAge
    """
    birth_date = datetime(year, month, day)
    today = datetime.today()
    age = relativedelta(today, birth_date)
    return UserAge(age.years, age.months, age.days)
