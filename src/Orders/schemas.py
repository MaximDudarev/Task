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

class Orders(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    status: Status
    create_at: datetime = Field(sa_column=Column(server_default=text("TIMEZONE('utc', now())")))

class OrdersResponseGet(SQLModel):
    status: str
    data: List[Orders]

class OrdersCreate(SQLModel):
    id_products: int
    count: int

