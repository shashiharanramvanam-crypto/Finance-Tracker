import os
import json
import tempfile
import unittest
from src.models import Transaction
from src.storage import Storage   # adjust import if your Storage class lives elsewhere

class TestStorage(unittest.TestCase):
    def setUp(self):
        # Create a temporary directory and file for each test
        self.test_dir = tempfile.TemporaryDirectory()
        self.test_file = os.path.join(self.test_dir.name, "transactions.json")
        self.storage = Storage(self.test_file)

    def tearDown(self):
        # Clean up temporary directory
        self.test_dir.cleanup()

    def test_init_creates_empty_file(self):
        # File should exist and contain []
        with open(self.test_file, "r") as f:
            content = f.read().strip()
        self.assertEqual(content, "[]")
        self.assertEqual(self.storage.load_all(), [])

    def test_add_and_load_single_transaction(self):
        t = Transaction(
            id="1",
            amount=50.0,
            category="Food",
            date="2026-09-01",
            type="EXPENSE",
            description="Lunch"
        )
        self.storage.add(t)
        loaded = self.storage.load_all()
        self.assertEqual(len(loaded), 1)
        self.assertEqual(loaded[0].amount, 50.0)
        self.assertEqual(loaded[0].category, "Food")
        self.assertEqual(loaded[0].date, "2026-09-01")
        self.assertEqual(loaded[0].type, "EXPENSE")
        self.assertEqual(loaded[0].description, "Lunch")

    def test_add_multiple_transactions_preserves_order(self):
        t1 = Transaction(id="1", amount=10.0, category="A", date="2026-09-01", type="EXPENSE", description="First")
        t2 = Transaction(id="2", amount=20.0, category="B", date="2026-09-02", type="INCOME", description="Second")
        t3 = Transaction(id="3", amount=30.0, category="C", date="2026-09-03", type="EXPENSE", description="Third")

        self.storage.add(t1)
        self.storage.add(t2)
        self.storage.add(t3)

        loaded = self.storage.load_all()
        self.assertEqual(len(loaded), 3)
        self.assertEqual([txn.id for txn in loaded], ["1", "2", "3"])

    def test_corrupted_json_recovery(self):
        # Write invalid JSON directly
        with open(self.test_file, "w") as f:
            f.write("INVALID JSON {{{[")
        loaded = self.storage.load_all()
        self.assertEqual(loaded, [])

    def test_csv_export_and_import(self):
        # Add 2 transactions
        t1 = Transaction(id="1", amount=100.0, category="Salary", date="2026-09-01", type="INCOME", description="Paycheck")
        t2 = Transaction(id="2", amount=40.0, category="Transport", date="2026-09-02", type="EXPENSE", description="Bus fare")
        self.storage.add(t1)
        self.storage.add(t2)

        # Export to CSV
        csv_path = os.path.join(self.test_dir.name, "export.csv")
        self.storage.export_to_csv(csv_path)

        # Import into a fresh storage
        new_file = os.path.join(self.test_dir.name, "new_storage.json")
        new_storage = Storage(new_file)
        count = new_storage.import_from_csv(csv_path)

        self.assertEqual(count, 2)
        loaded = new_storage.load_all()
        self.assertEqual(len(loaded), 2)
        self.assertEqual(loaded[0].category, "Salary")
        self.assertEqual(loaded[1].category, "Transport")


if __name__ == "__main__":
    unittest.main()
