from decimal import Decimal

from sqlalchemy import Column, text, DECIMAL
from sqlmodel import SQLModel, Field

class Products(SQLModel, table=True):
    id: int = Field(primary_key=True) # без default=None
    name: str
    description: str
    price: float # Decimal = Field(sa_column=Column(server_default=text('NUMERIC(10, 2)')))
    amount: int

class ProductsResponseGet(SQLModel):
    status: str
    data: list[Products]

class CreateProducts(SQLModel):
    name: str
    description: str
    price: Decimal = Field(sa_column=Column(server_default=text('NUMERIC(10, 2)')))
    amount: int