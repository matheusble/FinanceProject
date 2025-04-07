from sqlalchemy import Column, Integer, String, Boolean, Date, Float

from database import Base


class Spent(Base):
    __tablename__ = "spents"

    id: int = Column(Integer, primary_key=True, index=True)
    name: str = Column(String(100), nullable=False)
    content: str = Column(String(255), nullable=False)
    category: str = Column(String(100), nullable=False)
    recurring = Column(Boolean, nullable=False, default=False)
    installment_debt: int = Column(Integer, nullable=True)
    purchase_date = Column(Date, nullable=False)
    amount = Column(Float, nullable=False)

class AuthorizationNumber(Base):
    __tablename__ = "authorization_number"

    id: int = Column(Integer, primary_key=True, index=True)
    name: str = Column(String(100), nullable=False)
    number: str = Column(String(255), nullable=False)
    status = Column(Boolean, nullable=False, default=False)