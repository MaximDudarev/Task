from decimal import Decimal
from sqlalchemy.orm import Mapped, mapped_column
from src.database import Base


class Products(Base):
    __tablename__ = 'products'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str]
    description: Mapped[str | None]
    price: Mapped[Decimal]
    amount: Mapped[int]