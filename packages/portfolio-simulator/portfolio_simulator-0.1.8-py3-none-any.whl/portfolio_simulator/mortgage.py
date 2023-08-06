from dataclasses import dataclass
from datetime import date, datetime
import pandas as pd


@dataclass
class Term:
    period: int
    day: date
    principal_left_start: float
    interests: float
    principal_paid: float
    principal_left_end: float


@dataclass
class BaseMortgage:
    """Holds parameters about a given mortgage and provides
    properties and method to access future cashflows and other
    realated information.

    Args:
        principal (int): original amount borrowed.
        rate (float): yearly rate (e.g. 0.01 for a 1% yearly rate).
        start_date (str): format YYYY-MM-DD (e.g. 2021-12-31)
        months (int): number of months this mortgage runs for.
    """

    principal: int
    rate: float
    start_date: date
    months: int

    def __post_init__(self):
        self.start_date = pd.to_datetime(self.start_date, errors="ignore")
        if not isinstance(self.start_date, date):
            raise TypeError("Wrong start_date format")

    @property
    def date_index(self):
        return pd.date_range(self.start_date, periods=self.months, freq="MS")

    # Expects a fully defined term (except for the princpal_paid portion)
    def update_term_with_principal_paid(self, term: Term) -> None:
        raise NotImplementedError

    def __iter__(self):
        principal_left = self.principal
        for index, day in enumerate(self.date_index):
            term = Term(
                index, day, principal_left, principal_left * self.rate / 12, 0, 0
            )
            self.update_term_with_principal_paid(term)
            principal_left -= term.principal_paid
            term.principal_left_end = principal_left
            yield term

    def to_dataframe(self):
        return pd.DataFrame.from_dict(iter(self)).set_index("day")


@dataclass
class FixedPaymentMortgage(BaseMortgage):
    fixed_payment: float

    # Expects a fully defined term (except for the princpal_paid portion)
    def update_term_with_principal_paid(self, term: Term) -> None:
        term.principal_paid = min(
            term.principal_left_start, self.fixed_payment - term.interests
        )


@dataclass
class EndOfYearAmortizedMortgage(BaseMortgage):
    amotization_pa: float

    # Expects a fully defined term (except for the princpal_paid portion)
    def update_term_with_principal_paid(self, term: Term) -> None:
        if term.day.month == 12:
            term.principal_paid = min(term.principal_left_start, self.amotization_pa)


@dataclass
class GermanMortgage(BaseMortgage):
    initial_amortization_rate: float

    # Expects a fully defined term (except for the princpal_paid portion)
    def update_term_with_principal_paid(self, term: Term) -> None:
        initial_amotization_pm = self.principal * self.initial_amortization_rate / 12
        initial_interests_pm = self.principal * self.rate / 12
        monthly_payment = initial_amotization_pm + initial_interests_pm
        term.principal_paid = min(
            term.principal_left_start, monthly_payment - term.interests
        )


@dataclass
class MortgageFactory:
    principal: int
    rate: float
    start_date: str
    months: int

    def MakeFixedPaymentMortgage(self, fixed_payment: float) -> BaseMortgage:
        return FixedPaymentMortgage(
            self.principal,
            self.rate,
            self.start_date,
            self.months,
            fixed_payment,
        )

    def MakeEndOfYearAmortizedMortgage(self, amotization_pa: float) -> BaseMortgage:
        return EndOfYearAmortizedMortgage(
            self.principal, self.rate, self.start_date, self.months, amotization_pa
        )

    def MakeGermanMortgage(self, initial_amortization_rate: float) -> BaseMortgage:
        return GermanMortgage(
            self.principal,
            self.rate,
            self.start_date,
            self.months,
            initial_amortization_rate,
        )
