import enum
from datetime import datetime
from typing import List
from sqlalchemy import  text, Column
from sqlmodel import SQLModel, Field


class Status(str, enum.Enum):
    in_progress = 'in_progress'
    sent = 'sent'
    delivered = 'delivered'

class OrdersUpdate(SQLModel):
    status: Status


class OrdersCreate(SQLModel):
    id_products: int
    count: int


class OrdersWithItems(SQLModel):
    id: int = Field(default=None, primary_key=True)
    status: Status
    create_at: datetime = Field(sa_column=Column(server_default=text("TIMEZONE('utc', now())")))
    id_product: int
    count: int

class OrdersResponseGet(SQLModel):
    status: str
    data: List[OrdersWithItems]