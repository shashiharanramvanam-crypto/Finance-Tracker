from decimal import Decimal
from src.models import Transaction
from src.validators import Amount,DateAndTime,Transactioncheck,ValidCategory
from typing import Optional
from src.storage import Storage

class FinanceService:
    def __init__(self,storage:Storage):
        self.storage=storage

    def add_transaction(
            self,
            amount:float | Decimal,
            category :str,
            date: str,
            type: str,
            description : str=""
    )->Transaction:
        amount_dec=Decimal(str(amount)) if not isinstance(amount,Decimal) else amount

        transaction = Transaction(
            amount=Decimal(amount_dec),
            category=category.strip(),
            date=date.strip(),
            type=type.strip().upper(),
            description=description.strip()
        )

        Amount(transaction)
        Transactioncheck(transaction)
        DateAndTime(transaction)
        ValidCategory(transaction)

        self.storage.add(transaction)
        return transaction

    def list_transactions(
            self,
            category :str ="",
            type:str="",
            start_date: str="",
            end_date: str=""
    ) -> list[Transaction]:
        transactions = self.storage.load_all()

        if category:
            cat_lower = category.lower()
            transactions = [t for t in transactions if t.category.lower() == cat_lower]
        if type:
            type_upper = type.upper()
            transactions = [t for t in transactions if t.type.upper()==type_upper]
        if start_date:
            transactions =[t for t in transactions if t.date>=start_date]
        if end_date:
            transactions =[t for t in transactions if t.date <= end_date]

        return transactions


    def calculate_summary(self,transactions :Optional[list[Transaction]]=None) -> dict:
        if transactions is None:
            transactions = self.storage.load_all()

        total_income = Decimal("0.00")
        total_expenses = Decimal("0.00")
        category_breakdown:dict[str,Decimal]={}

        for t in transactions:
            t_type = t.type.upper()
            t_amt = Decimal(str(t.amount))

            if t_type == "INCOME":
                total_income+=t_amt
            elif t_type == "EXPENSE":
                total_expenses+=t_amt
                category_breakdown[t.category]=category_breakdown.get(t.category, Decimal("0.00")) + t_amt

        net_savings = total_income-total_expenses
        savings_rate = (net_savings/total_income*Decimal("100")) if total_income>Decimal("0") else Decimal("0.0")

        return {
            "total_income":float(round(total_income,2)),
            "total_expenses":float(round(total_expenses,2)),
            "net_savings":float(round(net_savings,2)),
            "savings_rate":float(round(savings_rate,2)),
            "category_breakdown":{k:float(round(v,2)) for k,v in category_breakdown.items()}
        }

    def budget_audit(self,monthly_budget_limits:float |Decimal, month :str)->dict:
        budget = Decimal(str(monthly_budget_limits))

        expenses = [
            t for t in self.list_transactions(type="EXPENSE")
            if t.date.startswith(month)
        ]

        total_spent = sum(((Decimal(str(t.amount))) for t in expenses) , Decimal("0.0"))
        remaining=budget-total_spent

        if total_spent<=Decimal("0.8")*budget:
            status = "NORMAL"
        elif total_spent<=budget:
            status = "WARNING"
        else:
            status = "EXCEEDED"

        return {
            "month":month,
            "budget":float(round(budget,2)),
            "total_spent":float(round(total_spent,2)),
            "remaining" :float(round(remaining,2)),
            "status":status
        }
    