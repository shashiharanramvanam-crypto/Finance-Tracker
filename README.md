# Personal Financial Tracker & Budget Auditor (CLI)

A modular, zero-dependency command-line personal finance engine and budget auditor built in pure Python. Designed with clean backend architecture principles, robust validation, domain-driven error handling, and complete unit test coverage.

---

## Architecture & Design Principles

The application strictly separates domain models, validation, storage persistence, computational business logic, and CLI routing:

```text
finance_tracker/
│
├── src/
│   ├── models.py       # Entity data structures (dataclasses, serialization)
│   ├── exceptions.py   # Domain-specific exception hierarchy
│   ├── validators.py   # Pure-function gatekeeper validation rules
│   ├── storage.py      # Persistence layer (JSON & CSV I/O handling)
│   ├── services.py     # Pure business logic, analytics, and budget audits
│   └── cli.py          # Command-line interface and terminal formatting (argparse)
│
├── tests/
│   ├── test_validators.py  # Validation edge cases and boundary checks
│   ├── test_storage.py     # File persistence and I/O isolation tests
│   └── test_services.py    # Business calculations and audit logic tests
│
├── data/
│   └── transactions.json   # Local transaction datastore
│
├── main.py             # Application bootstrap entry point
└── requirements.txt    # Tooling dependencies




Key Engineering Highlights
Separation of Concerns: Business logic (FinanceService) has zero awareness of terminal flags or JSON file formats.

Dependency Injection: FinanceService accepts an instance of Storage, enabling straightforward mocking and sandboxed testing.

Domain Exception Hierarchy: Custom exceptions derived from FinanceTrackerError prevent unhandled runtime tracebacks and surface user-friendly terminal errors.

Test Isolation: File I/O tests run inside sandboxed temporary directories via tempfile.TemporaryDirectory, ensuring test runs never mutate or pollute local data files.

Zero External Runtime Dependencies: Implemented entirely with Python standard libraries (dataclasses, uuid, datetime, argparse, json, csv, unittest).

Installation & Setup
Clone the repository:

Bash
git clone <repo-url>
cd finance_tracker
Ensure Python 3.10+ is installed:

Bash
python --version
(Optional) Install development tools:

Bash
pip install -r requirements.txt
Usage Guide
Run commands via main.py:

1. Add a Transaction
Bash
python main.py add --amount 45.50 --category Food --type EXPENSE --date 2026-09-03 --desc "Groceries"
python main.py add --amount 2500.00 --category Salary --type INCOME --date 2026-09-01 --desc "Monthly Paycheck"
2. List Transactions (with Optional Filters)
Bash
# List all transactions
python main.py list

# Filter by category and type
python main.py list --category Food --type EXPENSE

# Filter by date range
python main.py list --start-date 2026-09-01 --end-date 2026-09-30
Sample output:

Plaintext
DATE         | TYPE    | CATEGORY       | AMOUNT      | DESCRIPTION
----------------------------------------------------------------------
2026-09-01   | INCOME  | Salary         | $   2500.00 | Monthly Paycheck
2026-09-03   | EXPENSE | Food           | $     45.50 | Groceries
3. View Financial Summary
Bash
python main.py summary
Sample output:

Plaintext
Summary:

Expenses by Category:
  - Food           : $   45.50
Total Income : $2500.00
Total Expense: $45.50
Net Savings  : $2454.50
Savings Rate : 98.18%
4. Run a Monthly Budget Audit
Bash
python main.py audit --budget 1200.00 --month 2026-09
Sample output:

Plaintext
Month 2026-09 | Budget: $1200.00 | Spent: $45.50 | Remaining: $1154.50 [NORMAL]
5. Export / Import CSV
Bash
# Export transactions to CSV
python main.py export --file data/backup.csv

# Import transactions from a bank export
python main.py import --file data/bank_statement.csv