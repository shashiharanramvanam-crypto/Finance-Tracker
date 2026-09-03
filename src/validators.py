from src.exceptions import ValidationError
import datetime
from decimal import Decimal

def Amount(Transaction):
    amount=Transaction.amount
    if not isinstance(amount, (int, float, Decimal)) or isinstance(amount, bool):
        raise ValidationError("Amount must be a number.")
    if amount <= 0:
        raise ValidationError("Amount must be greater than 0.")
    else:
        return True
    
def Transactioncheck(Transaction):
    if not isinstance(Transaction.type, str) or Transaction.type.upper() not in ("INCOME", "EXPENSE"):
        raise ValidationError("Must be INCOME or EXPENSE")
    else:
        return True

def is_iso_date(s: str) -> bool:
    try:
        datetime.date.fromisoformat(s)
        return True
    except ValueError:
        return False
    
def DateAndTime(Transaction):
    if not isinstance(Transaction.date, str) or not is_iso_date(Transaction.date):
        raise ValidationError("Must be in YYYY-MM-DD Format")
    else:
        return True


def ValidCategory(Transaction):
    if not isinstance(Transaction.category, str) or len(Transaction.category.strip()) == 0:
        raise ValidationError("Provide the Category")
    else:
        return True

