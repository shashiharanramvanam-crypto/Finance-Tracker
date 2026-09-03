# main.py
from src.storage import Storage
from src.services import FinanceService
from src.cli import run_cli

def main():
    # Initialize storage (JSON file in data/)
    storage = Storage("data/transactions.json")

    # Initialize FinanceService with storage
    service = FinanceService(storage)

    # Pass the service into CLI runner
    run_cli(service)

if __name__ == "__main__":
    main()
