from sqlalchemy import Column,func, Enum as sqlalchemyEnum
from sqlalchemy.sql.sqltypes import Integer, String, Float, DateTime, Date, Boolean
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import relationship
from sqlalchemy.schema import ForeignKey

from db.engine import Base


class DBBooking(Base):
    __tablename__ = "booking"

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False, index=True)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    room_id = Column(Integer, ForeignKey("room.id"), nullable=False, index=True)
    is_paid = Column(Boolean, default=False, nullable=False)
    start_date = Column(Date, nullable=False, index=True)
    end_date = Column(Date, nullable=False, index=True)
    created_at = Column(DateTime, nullable=False, default=func.now())
    updated_at = Column(
        DateTime, nullable=False, default=func.now(), onupdate=func.now()
    )

    user = relationship("DBUser", back_populates="bookings")
    room = relationship("DBRoom", back_populates="bookings")

    @hybrid_property
    def total_price(self) -> float:
        days: int = (self.end_date - self.start_date).days
        print(days)
        base_price: float = days * self.room.price

        # Apply discount if there's an offer
        discount: float = base_price * self.user.offer_type.value
        total_price: float = base_price - discount
        return total_price
