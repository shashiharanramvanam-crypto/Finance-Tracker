import os
import json
from src.models import Transaction

class Storage:
    
    def __init__(self, filepath :str):
        self.file=filepath

        os.makedirs(os.path.dirname(filepath),exist_ok=True)

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
        