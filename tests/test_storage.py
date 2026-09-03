import os
import json
import tempfile
import unittest
from src.storage import Storage
from src.models import Transaction


class TestStorage(unittest.TestCase):

    def setUp(self):
        self.tmpdir = tempfile.TemporaryDirectory()
        self.storage_file = os.path.join(self.tmpdir.name, "transactions.json")
        self.storage = Storage(self.storage_file)

    def tearDown(self):
        self.tmpdir.cleanup()

    def test_init_creates_empty_storage(self):
        self.assertTrue(os.path.exists(self.storage_file))
        records = self.storage.load_all()
        self.assertEqual(records, [])

    def test_add_and_load_single_transaction(self):
        t = Transaction(
            amount=50.0,
            category="Food",
            date="2026-09-01",
            type="EXPENSE",
            description="Lunch",
        )
        self.storage.add(t)

        records = self.storage.load_all()
        self.assertEqual(len(records), 1)
        self.assertEqual(records[0].amount, 50.0)
        self.assertEqual(records[0].category, "Food")
        self.assertEqual(records[0].date, "2026-09-01")
        self.assertEqual(records[0].type, "EXPENSE")
        self.assertEqual(records[0].description, "Lunch")

    def test_add_multiple_preserves_order(self):
        t1 = Transaction(amount=100.0, category="Rent", date="2026-09-01", type="EXPENSE")
        t2 = Transaction(amount=2000.0, category="Salary", date="2026-09-02", type="INCOME")
        t3 = Transaction(amount=25.0, category="Food", date="2026-09-03", type="EXPENSE")

        self.storage.add(t1)
        self.storage.add(t2)
        self.storage.add(t3)

        records = self.storage.load_all()
        self.assertEqual(len(records), 3)
        self.assertEqual(records[0].category, "Rent")
        self.assertEqual(records[1].category, "Salary")
        self.assertEqual(records[2].category, "Food")

    def test_corrupted_json_recovery(self):
        with open(self.storage_file, "w") as f:
            f.write("{ invalid json [")

        records = self.storage.load_all()
        self.assertEqual(records, [])

    def test_empty_file_recovery(self):
        with open(self.storage_file, "w") as f:
            f.write("")

        records = self.storage.load_all()
        self.assertEqual(records, [])

    def test_export_to_csv(self):
        t1 = Transaction(amount=45.0, category="Food", date="2026-09-01", type="EXPENSE", description="Snack")
        t2 = Transaction(amount=1200.0, category="Salary", date="2026-09-02", type="INCOME", description="Pay")
        self.storage.add(t1)
        self.storage.add(t2)

        csv_path = os.path.join(self.tmpdir.name, "export.csv")
        self.storage.export_to_csv(csv_path)

        self.assertTrue(os.path.exists(csv_path))
        with open(csv_path, "r") as f:
            lines = [line.strip() for line in f.readlines() if line.strip()]
            self.assertEqual(len(lines), 3)  # 1 header line + 2 transaction rows
            self.assertIn("id,amount,category,date,type,description", lines[0])

    def test_import_from_csv(self):
        csv_path = os.path.join(self.tmpdir.name, "import.csv")
        csv_content = (
            "id,amount,category,date,type,description\n"
            "t1,55.0,Food,2026-09-01,EXPENSE,Dinner\n"
            "t2,3000.0,Salary,2026-09-02,INCOME,Consulting\n"
            "t3,-10.0,Invalid,2026-09-03,EXPENSE,Bad Amount\n"  # Corrupt row: negative amount
            "t4,15.0,Food,invalid-date,EXPENSE,Bad Date\n"        # Corrupt row: bad date
        )
        with open(csv_path, "w") as f:
            f.write(csv_content)

        fresh_storage_file = os.path.join(self.tmpdir.name, "fresh.json")
        fresh_storage = Storage(fresh_storage_file)

        imported_count = fresh_storage.import_from_csv(csv_path)

        # 2 valid rows should import, 2 malformed rows should be skipped
        self.assertEqual(imported_count, 2)
        records = fresh_storage.load_all()
        self.assertEqual(len(records), 2)
        self.assertEqual(records[0].category, "Food")
        self.assertEqual(records[1].category, "Salary")


if __name__ == "__main__":
    unittest.main()