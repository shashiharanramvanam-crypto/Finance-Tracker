from exceptions import ValidationError
from models import Transaction

def Amount(Transaction):
    if(Transaction["Amount"]<0):
        raise ValidationError("Must be greater than 0")

    if isinstance(Transaction["Amount"],float):
        pass
    else:
        raise ValidationError("Must be a number")

    
       