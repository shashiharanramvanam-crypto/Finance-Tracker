from dataclasses import dataclass,field
import uuid
from decimal import Decimal

@dataclass
class Transaction:
    id:str = field(default_factory=lambda: str(uuid.uuid4()))
    amount:float | Decimal =0.0
    category:str=""
    date:str=""
    type:str=""
    description:str=""

    def to_dict(self)->dict:
        return {
            "id":self.id,
            "amount":self.amount,
            "category":self.category,
            "date":self.date,
            "type":self.type,
            "description":self.description
        }

    @classmethod
    def from_dict(cls,data:dict):
        return cls(**data)

