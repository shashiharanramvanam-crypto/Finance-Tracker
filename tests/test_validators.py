import unittest
from src.validators import Amount, Transactioncheck, DateAndTime, ValidCategory, is_iso_date
from src.exceptions import ValidationError
from src.models import Transaction

class TestAmount(unittest.TestCase):
    def test_positive_amount(self):
        t = Transaction(amount=100)
        self.assertTrue(Amount(t))

    def test_zero_amount(self):
        t = Transaction(amount=0)
        with self.assertRaises(ValidationError):
            Amount(t)

    def test_negative_amount(self):
        t = Transaction(amount=-50)
        with self.assertRaises(ValidationError):
            Amount(t)

    def test_float_amount(self):
        t = Transaction(amount=12.5)
        self.assertTrue(Amount(t))

    def test_bool_amount(self):
        t = Transaction(amount=True)
        with self.assertRaises(ValidationError):
            Amount(t)


    def test_large_amount(self):
        t = Transaction(amount=10**6)
        self.assertTrue(Amount(t))

    def test_small_positive(self):
        t = Transaction(amount=1)
        self.assertTrue(Amount(t))

    def test_decimal_amount(self):
        t = Transaction(amount=0.01)
        self.assertTrue(Amount(t))


class TestTransactioncheck(unittest.TestCase):
    def test_income_type(self):
        t = Transaction(type="INCOME")
        self.assertTrue(Transactioncheck(t))

    def test_expense_type(self):
        t = Transaction(type="EXPENSE")
        self.assertTrue(Transactioncheck(t))

    def test_lowercase_income(self):
        t = Transaction(type="income")
        self.assertTrue(Transactioncheck(t))

    def test_lowercase_expense(self):
        t = Transaction(type="expense")
        self.assertTrue(Transactioncheck(t))

    def test_invalid_type(self):
        t = Transaction(type="TRANSFER")
        with self.assertRaises(ValidationError):
            Transactioncheck(t)

    def test_empty_type(self):
        t = Transaction(type="")
        with self.assertRaises(ValidationError):
            Transactioncheck(t)


    def test_whitespace_type(self):
        t = Transaction(type=" ")
        with self.assertRaises(ValidationError):
            Transactioncheck(t)


class TestDateAndTime(unittest.TestCase):
    def test_valid_date(self):
        t = Transaction(date="2026-08-31")
        self.assertTrue(DateAndTime(t))

    def test_invalid_format(self):
        t = Transaction(date="31-08-2026")
        with self.assertRaises(ValidationError):
            DateAndTime(t)

    def test_empty_date(self):
        t = Transaction(date="")
        with self.assertRaises(ValidationError):
            DateAndTime(t)


    def test_whitespace_date(self):
        t = Transaction(date=" ")
        with self.assertRaises(ValidationError):
            DateAndTime(t)

    def test_valid_leap_year(self):
        t = Transaction(date="2024-02-29")
        self.assertTrue(DateAndTime(t))

    def test_invalid_leap_year(self):
        t = Transaction(date="2023-02-29")
        with self.assertRaises(ValidationError):
            DateAndTime(t)

    def test_valid_month_end(self):
        t = Transaction(date="2026-01-31")
        self.assertTrue(DateAndTime(t))

    def test_invalid_month_end(self):
        t = Transaction(date="2026-04-31")
        with self.assertRaises(ValidationError):
            DateAndTime(t)

    def test_valid_iso_date(self):
        self.assertTrue(is_iso_date("2026-08-31"))


class TestValidCategory(unittest.TestCase):
    def test_non_empty_category(self):
        t = Transaction(category="Food")
        self.assertTrue(ValidCategory(t))

    def test_empty_category(self):
        t = Transaction(category="")
        with self.assertRaises(ValidationError):
            ValidCategory(t)

    def test_whitespace_category(self):
        t = Transaction(category="   ")
        with self.assertRaises(ValidationError):
            ValidCategory(t)

    def test_valid_category_with_spaces(self):
        t = Transaction(category=" Grocery ")
        self.assertTrue(ValidCategory(t))

    def test_long_category(self):
        t = Transaction(category="VeryLongCategoryNameThatIsStillValid")
        self.assertTrue(ValidCategory(t))

    def test_special_characters(self):
        t = Transaction(category="Food&Drink")
        self.assertTrue(ValidCategory(t))

    def test_single_char_category(self):
        t = Transaction(category="A")
        self.assertTrue(ValidCategory(t))

    def test_valid_category_case(self):
        t = Transaction(category="income")
        self.assertTrue(ValidCategory(t))


if __name__ == "__main__":
    unittest.main()
