from datetime import datetime
from typing import Annotated
from sqlalchemy import text, ForeignKey
from src.Orders.schemas import Status
from sqlalchemy.orm import mapped_column, Mapped

from src.Products.models import Products
from src.database import Base

created_at = Annotated[datetime, mapped_column(server_default=text("TIMEZONE('utc', now())"))]

class Orders(Base):
    __tablename__ = 'orders'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    create_at: Mapped[created_at]
    status: Mapped[Status]

class OrdersItems(Base):
    __tablename__ = 'orders_items'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    id_orders: Mapped[int] = mapped_column(ForeignKey(Orders.id))
    id_products: Mapped[int] = mapped_column(ForeignKey(Products.id))
    count: Mapped[int]