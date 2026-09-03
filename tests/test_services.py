import os
import tempfile
import unittest
from src.services import FinanceService
from src.storage import Storage
from src.models import Transaction
from src.exceptions import ValidationError

class TestFinanceService(unittest.TestCase):

    def setUp(self):
        # Create a clean temporary storage for each test
        self.tmpdir = tempfile.TemporaryDirectory()
        storage_path = os.path.join(self.tmpdir.name, "transactions.json")
        self.storage = Storage(storage_path)
        self.service = FinanceService(self.storage)

    def tearDown(self):
        self.tmpdir.cleanup()

    # 1. Transaction Creation & Validation
    def test_add_transaction_valid(self):
        t = self.service.add_transaction(
            amount=100.0,
            category="Food",
            date="2026-09-01",
            type="EXPENSE",
            description="Lunch"
        )
        self.assertIsInstance(t, Transaction)
        all_txns = self.storage.load_all()
        self.assertEqual(len(all_txns), 1)
        self.assertEqual(all_txns[0].amount, 100.0)
        self.assertEqual(all_txns[0].category, "Food")

    def test_add_transaction_invalid_amount(self):
        with self.assertRaises(ValidationError):
            self.service.add_transaction(-50.0, "Food", "2026-09-01", "EXPENSE")
        self.assertEqual(self.storage.load_all(), [])

    def test_add_transaction_invalid_date(self):
        with self.assertRaises(ValidationError):
            self.service.add_transaction(50.0, "Food", "01-09-2026", "EXPENSE")
        self.assertEqual(self.storage.load_all(), [])

    # 2. Dynamic Filtering
    def test_list_transactions_filters(self):
        self.service.add_transaction(100, "Food", "2026-09-01", "EXPENSE")
        self.service.add_transaction(200, "Rent", "2026-09-02", "EXPENSE")
        self.service.add_transaction(500, "Salary", "2026-09-03", "INCOME")

        food_txns = self.service.list_transactions(category="food")
        self.assertEqual(len(food_txns), 1)
        self.assertEqual(food_txns[0].category, "Food")

        income_txns = self.service.list_transactions(type="INCOME")
        self.assertEqual(len(income_txns), 1)
        self.assertEqual(income_txns[0].type, "INCOME")

        sept1_to2 = self.service.list_transactions(start_date="2026-09-01", end_date="2026-09-02")
        self.assertEqual(len(sept1_to2), 2)

    # 3. Summary & Financial Math
    def test_calculate_summary_standard(self):
        self.service.add_transaction(1000, "Salary", "2026-09-01", "INCOME")
        self.service.add_transaction(200, "Food", "2026-09-02", "EXPENSE")
        self.service.add_transaction(300, "Rent", "2026-09-03", "EXPENSE")

        summary = self.service.calculate_summary()
        self.assertEqual(summary["total_income"], 1000.0)
        self.assertEqual(summary["total_expenses"], 500.0)
        self.assertEqual(summary["net_savings"], 500.0)
        self.assertEqual(summary["savings_rate"], 50.0)
        self.assertEqual(summary["category_breakdown"], {"Food": 200.0, "Rent": 300.0})

    def test_calculate_summary_zero_income(self):
        self.service.add_transaction(200, "Food", "2026-09-02", "EXPENSE")
        summary = self.service.calculate_summary()
        self.assertEqual(summary["total_income"], 0.0)
        self.assertEqual(summary["savings_rate"], 0.0)

    # 4. Budget Audit
    def test_budget_audit_thresholds(self):
        self.service.add_transaction(200, "Food", "2026-09-01", "EXPENSE")   # 20% -> NORMAL
        self.service.add_transaction(700, "Rent", "2026-09-02", "EXPENSE")   # 90% -> WARNING
        self.service.add_transaction(200, "Shopping", "2026-09-03", "EXPENSE") # 110% -> EXCEEDED
        self.service.add_transaction(100, "Other", "2026-08-31", "EXPENSE")  # Different month

        audit = self.service.budget_audit(1000, "2026-09")
        self.assertEqual(audit["total_spent"], 1100.0)
        self.assertEqual(audit["remaining"], -100.0)
        self.assertEqual(audit["status"], "EXCEEDED")

if __name__ == "__main__":
    unittest.main()
