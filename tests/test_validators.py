import unittest
from src.validators import Amount,DateaAndTime,Transactioncheck,ValidCategory,is_iso_date,Transaction
from src.exceptions import ValidationError

T1 = Transaction.from_dict({
    "id":123,
    "amount":123,
    "category":"",
    "date":"",
    "type":"",
    "description":""
})

T2 = Transaction.from_dict({
    "id":123,
    "amount":-123,
    "category":"",
    "date":"",
    "type":"",
    "description":""
})


T3 = Transaction.from_dict({
    "id":123,
    "amount":" ",
    "category":"",
    "date":"",
    "type":"",
    "description":""
})


class TestValidator(unittest.TestCase):
    def test_valid(self):
        self.assertTrue(Amount(T1))

    def test_invalid(self):
        with self.assertRaises(ValidationError):
            Amount(T2)

    def test_empty_string(self):
        with self.assertRaises(ValidationError):
            Amount(T3)

if __name__ == "__main__":
    unittest.main()