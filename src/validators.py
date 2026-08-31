from exceptions import ValidationError
from models import Transaction
import datetime

def Amount(Transaction):
    amount=Transaction["amount"]
    if not isinstance(amount, (int, float)) or isinstance(amount, bool):
        raise ValidationError("Amount must be a number.")
    if amount <= 0:
        raise ValidationError("Amount must be greater than 0.")

    
def Transactioncheck(Transaction):
    if not isinstance(Transaction["type"], (int, float)) or Transaction["type"].upper()not in ("INCOME", "EXPENSE"):
        raise ValidationError("Must be INCOOME or EXPENSE")


def is_iso_date(s: str) -> bool:
    try:
        datetime.date.fromisoformat(s)
        return True
    except ValueError:
        return False
    
def DateaAndTime(Transaction):
    if not isinstance(Transaction["date"], str) or not is_iso_date(Transaction["date"]):
        raise ValidationError("Must be in YYYY-MM-DD Format")


def ValidCategory(Transaction):
    if not isinstance(Transaction["category"], str) or len(Transaction["category"].strip()) == 0:
        raise ValidationError("Provide the Category")

