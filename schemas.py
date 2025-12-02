import re
from pydantic import BaseModel, Field, field_validator
from typing import List


# Mapeando a entrada de dados
class ConverterInput(BaseModel):
    price: float = Field(..., gt=0)
    to_currencies: List[str]

    @field_validator('to_currencies')
    def validate_to_currency(cls, value):
        for currency in value:
            if not re.match(r'^[A-Z]{3}$', currency):
                raise ValueError(f'Invalid currency code: {currency}')
        return value

# Mapeando a saída de dados
class ConverterOutput(BaseModel):
    message: str
    data: List[dict]


"""
{
    "price": 1512.35,
    "to_currency": ['USD', 'EUR', 'GBP']
}
"""

