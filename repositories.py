from datetime import date
from typing import Type

from sqlalchemy import func
from sqlalchemy.orm import Session

from models import Spent, AuthorizationNumber

class SpentRepository:
    @staticmethod
    def find_all(db: Session) -> list[Type[Spent]]:
        return db.query(Spent).all()

    @staticmethod
    def save(db: Session, spent: Spent) -> Spent:
        if spent.id:
            db.merge(spent)
        else:
            db.add(spent)
        db.commit()
        return spent

    @staticmethod
    def find_by_id(db: Session, id: int) -> Spent:
        return db.query(Spent).filter(Spent.id == id).first()

    @staticmethod
    def exists_by_id(db: Session, id: int) -> bool:
        return db.query(Spent).filter(Spent.id == id).first() is not None

    @staticmethod
    def delete_by_id(db: Session, id: int) -> None:
        spent = db.query(Spent).filter(Spent.id == id).first()
        if spent is not None:
            db.delete(spent)
            db.commit()

    @staticmethod
    def get_total_spent(db: Session, start_date: date, end_date: date) -> float:
        total = db.query(func.sum(Spent.amount)).filter(
            Spent.purchase_date >= start_date,
            Spent.purchase_date <= end_date
        ).scalar()
        return total or 0.0

    @staticmethod
    def get_total_spent_by_month(db: Session, year: int, month: int) -> float:
        total = db.query(func.sum(Spent.amount)).filter(
            func.extract('year', Spent.purchase_date) == year,
            func.extract('month', Spent.purchase_date) == month
        ).scalar()
        return total or 0.0

class NumberRepository:

    @staticmethod
    def salvar(db: Session, number: AuthorizationNumber) -> AuthorizationNumber:
        if number.id:
            db.merge(number)
        else:
            db.add(number)
        db.commit()
        db.refresh(number)
        return number

    @staticmethod
    def find_by_number(db: Session, number: str) -> AuthorizationNumber:
        return db.query(AuthorizationNumber).filter(AuthorizationNumber.number == number).first()