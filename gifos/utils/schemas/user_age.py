from dataclasses import dataclass


@dataclass
class UserAge:
    """A class to represent a user's age.

    This class represents a user's age in years, months, and days.

    Attributes:
        years: An integer that represents the number of full years of the user's age.
        months: An integer that represents the number of full months of the user's age, not included in the years.
        days: An integer that represents the number of days of the user's age, not included in the years and months.
    """

    __slots__ = ["years", "months", "days"]
    years: int
    months: int
    days: int
