import os,uuid
import json
from src.models import Transaction
import csv
from src.validators import Amount,Transactioncheck,DateAndTime,ValidCategory
from src.exceptions import ValidationError

class Storage:
    
    def __init__(self, filepath :str):
        self.file=filepath

        parent_dir = os.path.dirname(filepath)
        if parent_dir:
            os.makedirs(parent_dir, exist_ok=True)

        if not os.path.exists(filepath):
            with open(filepath, "w") as f:
                json.dump([],f)

    def load_all(self) -> list[Transaction]:
        try:
            with open(self.file , "r") as datafile:
                content = datafile.read().strip()

                if not content:
                    return []

                raw_list = json.loads(content)
                return [Transaction.from_dict(item) for item in raw_list]
        except (json.JSONDecodeError , FileNotFoundError):
            return []

    def save_all(self, transactions :list[Transaction]) -> None:
        with open(self.file , "w") as datafile:
            json.dump([t.to_dict() for t in transactions],datafile,indent=4)

    def add(self,transaction: Transaction) -> None:
        transactions = self.load_all()
        transactions.append(transaction)
        self.save_all(transactions)

    def export_to_csv(self, csv_filepath:str) -> None:
        transactions = self.load_all()
        with open(csv_filepath,"w",newline="") as csvfile:
            writer = csv.DictWriter(csvfile,fieldnames=["id","amount","category","date","type","description"])
            writer.writeheader()

            for t in transactions:
                writer.writerow(t.to_dict())

    def import_from_csv(self,csv_filepath:str) ->int:
        imported_count=0
        transactions = self.load_all()

        with open(csv_filepath,"r",newline="") as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                try:

                    transaction = Transaction(
                        id=str(uuid.uuid4()),
                        amount=float(row["amount"]),
                        category=row["category"],
                        date=row["date"],
                        type=row["type"].strip().upper(),
                        description=row.get("description","")
                    )

                    DateAndTime(transaction)
                    ValidCategory(transaction)
                    Amount(transaction)
                    Transactioncheck(transaction)

                    transactions.append(transaction)
                    imported_count+=1

                except (ValidationError, KeyError, ValueError) as e:
                    print(f"Skipping malformed row: {row}. Reason: {e}")

        self.save_all(transactions)
        return imported_count

                    
                    


