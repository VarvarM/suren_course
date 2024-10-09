from sqlalchemy import func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from .base import Base
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .product import Product
    from .order_product_association import OrderProductAssociation


class Order(Base):
    promocode: Mapped[str | None]
    created_at: Mapped[datetime] = mapped_column(server_default=func.now(), default=datetime.utcnow)
    # products: Mapped[list["Product"]] = relationship(back_populates="orders",
    #                                                  secondary="order_product_association")
    products_details: Mapped[list["OrderProductAssociation"]] = relationship(back_populates="order")
    # при работе появляются warnings. Так как products и products_details, а они обращаются по сути к одному и тому же.
    # В реальном проекте надо использовать 1 из способов. Оставил тут 2 примера для наглядности
