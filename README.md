Markdown
# Personal Financial Tracker & Budget Auditor (CLI)

A modular, zero-dependency command-line personal finance engine and budget auditor built in pure Python. Designed with clean backend architectural principles, strict validation boundaries, domain-driven error handling, and complete automated unit test coverage.

---

## Table of Contents

- [Architecture & Design Principles](#architecture--design-principles)
- [Project Structure](#project-structure)
- [Key Engineering Highlights](#key-engineering-highlights)
- [Installation & Setup](#installation--setup)
- [Usage Guide](#usage-guide)
  - [1. Add a Transaction](#1-add-a-transaction)
  - [2. List Transactions (with Filters)](#2-list-transactions-with-filters)
  - [3. View Financial Summary](#3-view-financial-summary)
  - [4. Run a Monthly Budget Audit](#4-run-a-monthly-budget-audit)
  - [5. Export & Import CSV](#5-export--import-csv)
- [Running Automated Tests](#running-automated-tests)
- [Error Handling & Edge Cases](#error-handling--edge-cases)

---

## Architecture & Design Principles

The application implements a decoupled, layered backend architecture where concerns are strictly separated:

* **Domain Model Layer (`models.py`):** Encapsulates core financial entities and serialization logic using Python standard dataclasses.
* **Validation Layer (`validators.py`):** Pure-function boundary gatekeepers that sanitize and validate inputs before any object is created or persisted.
* **Persistence Layer (`storage.py`):** Manages file I/O operations for JSON storage and CSV data portability, with safe fallback mechanisms for missing or corrupted files.
* **Service Layer (`services.py`):** Contains computational domain logic, aggregations, spending rate calculations, and budget thresholds. Completely decoupled from CLI arguments and terminal formatting.
* **Presentation Layer (`cli.py` & `main.py`):** CLI parsing using argparse subparsers, formatted ASCII table outputs, and top-level exception trapping.

```
[ Terminal Input (CLI / main.py) ]
               │
               ▼
   [ Presentation Layer (cli.py) ]
               │
               ▼
    [ Service Layer (services.py) ] <───> [ Validation Layer (validators.py) ]
               │
               ▼
    [ Storage Layer (storage.py) ]
               │
               ▼
   [ Data Store (JSON / CSV files) ]

```
## Project Structure


```
finance_tracker/
│
├── data/
│   └── .gitkeep            # Tracks folder structure without committing personal data
│
├── src/
│   ├── __init__.py
│   ├── cli.py              # CLI commands, arguments, and table formatting
│   ├── exceptions.py       # Domain-specific exception hierarchy
│   ├── models.py           # Transaction dataclass and serialization helpers
│   ├── services.py         # Business logic, aggregations, and audit calculations
│   ├── storage.py          # JSON and CSV persistence engine
│   └── validators.py       # Input sanitation and validation rules
│
├── tests/
│   ├── __init__.py
│   ├── test_services.py    # Unit tests for calculations, metrics, and filters
│   ├── test_storage.py     # Hermetic tests for file I/O using tempfile
│   └── test_validators.py  # Boundary tests for dates, types, amounts, and strings
│
├── .gitignore              # Ignores runtime data, caches, and virtual environments
├── main.py                 # Application bootstrap entry point
├── README.md               # Project documentation
└── requirements.txt        # Optional development/tooling dependencies

```
## Key Engineering Highlights
Separation of concerns: Business logic (FinanceService) has zero awareness of terminal flags, arguments, or JSON formatting.

Dependency Injection: FinanceService accepts an instance of Storage via constructor injection, enabling simple mocking and isolated testing.

Domain Exception Hierarchy: Custom exceptions inheriting from a root FinanceTrackerError prevent unhandled runtime tracebacks and surface structured, user-friendly error codes.

Precision Handling: Uses decimal.Decimal conversion internally to eliminate floating-point precision drift during financial computations.

Test Isolation: Storage unit tests execute within sandboxed temporary directories via tempfile.TemporaryDirectory, ensuring test suites never mutate or corrupt local data files.

Zero External Runtime Dependencies: Built entirely with the Python standard library (dataclasses, uuid, datetime, decimal, argparse, json, csv, unittest).


## Installation & Setup
Clone the repository:

Bash
```
git clone https://github.com/shashiharanramvanam-crypto/Finance-Tracker.git
cd Finance-Tracker
```
Verify Python version (Python 3.10+ recommended):
Bash
```
python --version
```
(Optional) Set up a virtual environment for development tooling:

Bash
```
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```
## Usage Guide

All operations are executed through main.py via structured subcommands.

1. Add a Transaction
Records a new financial entry with automatic UUID assignment and validation checks.

Bash
```
# Add an Expense
python main.py add --amount 45.50 --category Food --type EXPENSE --date 2026-09-03 --desc "Groceries"
```
# Add Income
```
python main.py add --amount 2500.00 --category Salary --type INCOME --date 2026-09-01 --desc "Monthly Paycheck"
```
2. List Transactions (with Filters)
Outputs transactions in an aligned tabular format. Supports filtering by category, type, and date range.

Bash
```
# List all transactions
python main.py list
```

# Filter by category (case-insensitive)
```
python main.py list --category Food


# Filter by transaction type
python main.py list --type EXPENSE

# Filter by inclusive date range
python main.py list --start-date 2026-09-01 --end-date 2026-09-30
```
Sample output:

```
DATE         | TYPE    | CATEGORY       | AMOUNT      | DESCRIPTION
----------------------------------------------------------------------
2026-09-01   | INCOME  | Salary         | $   2500.00 | Monthly Paycheck
2026-09-03   | EXPENSE | Food           | $     45.50 | Groceries

```
3. View Financial Summary
Aggregates total income, expenses, net savings, savings rate percentage, and category-level expense distributions.

Bash
```
python main.py summary
```

Sample output:

Plaintext
```
Summary:

Expenses by Category:
  - Food           : $   45.50
Total Income : $2500.00
Total Expense: $45.50
Net Savings  : $2454.50
Savings Rate : 98.18%
```

4. Run a Monthly Budget Audit
Evaluates actual expenses against a defined monthly budget cap and flags status thresholds (NORMAL, WARNING at 80% or higher, or EXCEEDED above 100%).

Bash
```
python main.py audit --budget 1200.00 --month 2026-09
```
Sample output:
```
Plaintext
Month 2026-09 | Budget: $1200.00 | Spent: $45.50 | Remaining: $1154.50 [NORMAL]
5. Export & Import CSV
Facilitates bulk imports from external financial services and exports local records to standard CSV files.
```
Bash
```
# Export transactions to CSV
python main.py export --file data/backup.csv

# Import transactions from an external CSV file
python main.py import --file data/bank_statement.csv
```
## Running Automated Tests
The project includes complete unit test coverage across all domain, validation, storage, and service layers.

Run all tests via Python's built-in discovery tool:

Bash
```
python -m unittest discover tests
```
To run individual test modules:

Bash
```
# Test validation rules and boundary inputs
python -m unittest tests/test_validators.py

# Test storage persistence and CSV utilities
python -m unittest tests/test_storage.py

# Test service layer calculations and business rules
python -m unittest tests/test_services.py
```
## Error Handling & Edge Cases
The application includes defensive programming safeguards against common failure modes:

Corrupted / Empty Storage: storage.py gracefully recovers from empty files or invalid JSON by initializing an empty state instead of crashing.

Division by Zero: calculate_summary returns a clean 0.0% savings rate when income is $0.00, avoiding unhandled mathematical exceptions.

Date & Calendar Validation: Rejects non-existent dates (e.g., leap year miscalculations like 2023-02-29 or invalid month-ends like 2026-04-31).

Input Sanitization: CLI exceptions are caught at the entry boundary, displaying clean diagnostic messages ([ERROR] <reason> (Code: <code_id>)) instead of raw stack traces.
