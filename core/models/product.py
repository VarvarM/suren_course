from sqlalchemy.orm import Mapped, relationship
from typing import TYPE_CHECKING
from .base import Base

if TYPE_CHECKING:
    from .order import Order
    from .order_product_association import OrderProductAssociation


class Product(Base):
    name: Mapped[str]
    description: Mapped[str]
    price: Mapped[int]
    # orders: Mapped[list["Order"]] = relationship(back_populates="products", secondary="order_product_association")
    order_details: Mapped[list["OrderProductAssociation"]] = relationship(back_populates="product")