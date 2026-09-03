import argparse
from src.exceptions import ValidationError

def run_cli(service):
    parser = argparse.ArgumentParser(description="Personal Financial Tracker CLI")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # add
    add_parser = subparsers.add_parser("add", help="Add a transaction")
    add_parser.add_argument("--amount", type=float, required=True)
    add_parser.add_argument("--category", type=str, required=True)
    add_parser.add_argument("--type", type=str, choices=["INCOME", "EXPENSE", "income", "expense"], required=True)
    add_parser.add_argument("--date", type=str, required=True, help="Format: YYYY-MM-DD")
    add_parser.add_argument("--desc", type=str, default="", help="Optional description")

    # list
    list_parser = subparsers.add_parser("list", help="List transactions")
    list_parser.add_argument("--category", type=str, default=None)
    list_parser.add_argument("--type", type=str, default=None)
    list_parser.add_argument("--start-date", type=str, default=None)
    list_parser.add_argument("--end-date", type=str, default=None)

    # summary
    subparsers.add_parser("summary", help="Show financial summary")

    # audit
    audit_parser = subparsers.add_parser("audit", help="Audit monthly budget")
    audit_parser.add_argument("--budget", type=float, required=True)
    audit_parser.add_argument("--month", type=str, required=True, help="Format: YYYY-MM")

    # export
    export_parser = subparsers.add_parser("export", help="Export transactions to CSV")
    export_parser.add_argument("--file", type=str, required=True, help="Target CSV file path")

    # import
    import_parser = subparsers.add_parser("import", help="Import transactions from CSV")
    import_parser.add_argument("--file", type=str, required=True, help="Source CSV file path")

    args = parser.parse_args()

    try:
        if args.command == "add":
            service.add_transaction(args.amount, args.category, args.date, args.type, args.desc)
            print("Transaction added successfully.")

        elif args.command == "list":
            txns = service.list_transactions(args.category, args.type, args.start_date, args.end_date)
            if not txns:
                print("No transactions found matching your criteria.")
                return
            print(f"{'DATE':<12} | {'TYPE':<7} | {'CATEGORY':<14} | {'AMOUNT':>10} | DESCRIPTION")
            print("-" * 70)
            for t in txns:
                print(f"{t.date:<12} | {t.type:<7} | {t.category:<14} | ${t.amount:>10.2f} | {t.description}")

        elif args.command == "summary":
            summary = service.calculate_summary()
            print("Summary:")
            if summary.get("category_breakdown"):
                print("\nExpenses by Category:")
                for cat, amt in summary["category_breakdown"].items():
                    print(f"  - {cat:<15}: ${amt:>8.2f}")
            print(f"Total Income : ${summary['total_income']:.2f}")
            print(f"Total Expense: ${summary['total_expenses']:.2f}")
            print(f"Net Savings  : ${summary['net_savings']:.2f}")
            print(f"Savings Rate : {summary['savings_rate']:.2f}%")

        elif args.command == "audit":
            audit = service.budget_audit(args.budget, args.month)
            print(f"Month {audit['month']} | Budget: ${audit['budget']:.2f} | "
                  f"Spent: ${audit['total_spent']:.2f} | Remaining: ${audit['remaining']:.2f} "
                  f"[{audit['status']}]")

        elif args.command == "export":
            service.storage.export_to_csv(args.file)
            print(f"Transactions exported successfully to {args.file}")

        elif args.command == "import":
            count = service.storage.import_from_csv(args.file)
            print(f"Successfully imported {count} transactions from {args.file}")

    except ValidationError as e:
        print(f"[ERROR] {e.message} (Code: {e.error_code})")
