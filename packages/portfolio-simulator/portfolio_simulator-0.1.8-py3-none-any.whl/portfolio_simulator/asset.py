from dataclasses import dataclass
import pandas as pd


@dataclass
class Asset:
    name: int
    value: int
    purchase_date: str
    sale_date: str

    @property
    def date_index(self):
        return pd.date_range(self.purchase_date, self.sale_date, freq="MS")

    def to_series(self):
        return pd.Series(self.value, index=self.date_index, name="principal")

    def to_dataframe(self):
        return self.to_series().to_frame()

    def single_events(self):
        return pd.Series(
            data={self.purchase_date: self.value, self.sale_date: -self.value},
            index=[self.purchase_date, self.sale_date],
        )
