"""TODO: add unit tests for other mortgage types."""
from mortgage import BaseMortgage
from mortgage import FixedPaymentMortgage
import unittest


class TestBaseMortgage(unittest.TestCase):
    def test_base_fails(self):
        mortgage = BaseMortgage(100, 0.001, "2011-01-01", 12)
        with self.assertRaises(NotImplementedError):
            mortgage.to_dataframe()


class TestFixedPaymentMortgage(unittest.TestCase):
    def test_has_expected_amount_of_terms(self):
        mortgage = FixedPaymentMortgage(100, 0.001, "2011-01-01", 12, 100)
        terms = list(mortgage)
        self.assertEquals(len(terms), 12)

    def test_date_format_issue(self):
        with self.assertRaises(TypeError):
            FixedPaymentMortgage(100, 0.001, "foo", 12, 100)


if __name__ == "__main__":
    unittest.main()
