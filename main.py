from datetime import date

import uvicorn
from fastapi import FastAPI, Depends, HTTPException, status, Response, Query
from sqlalchemy.orm import Session

from models import Spent, AuthorizationNumber
from database import engine, Base, get_db
from repositories import SpentRepository, NumberRepository
from schemas import SpentRequest, SpentResponse, NumberRequest, NumberResponse

Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.post("/api/authorization", response_model=NumberResponse, status_code=status.HTTP_201_CREATED)
def create(request: NumberRequest, db: Session = Depends(get_db)):
    number = NumberRepository.salvar(db, AuthorizationNumber(**request.model_dump()))
    return NumberResponse.model_validate(number)

@app.get("/api/authorization/numbers/{number}", response_model=NumberResponse)
def find_by_id(number: str, db: Session = Depends(get_db)):
    number = NumberRepository.find_by_number(db, number)
    if not number:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Número não encontrado"
        )
    return NumberResponse.model_validate(number)

@app.post("/api/spents", response_model=SpentResponse, status_code=status.HTTP_201_CREATED)
def create(request: SpentRequest, db: Session = Depends(get_db)):
    spent = SpentRepository.save(db, Spent(**request.model_dump()))
    return SpentResponse.model_validate(spent)

@app.get("/api/spents/all", response_model=list[SpentResponse])
def find_all(db: Session = Depends(get_db)):
    spents = SpentRepository.find_all(db)
    return [SpentResponse.model_validate(spent) for spent in spents]

@app.get("/api/spents/search/{id}", response_model=SpentResponse)
def find_by_id(id: int, db: Session = Depends(get_db)):
    spent = SpentRepository.find_by_id(db, id)
    if not spent:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Gasto não encontrado"
        )
    return SpentResponse.model_validate(spent)

@app.delete("/api/spents/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_by_id(id: int, db: Session = Depends(get_db)):
    if not SpentRepository.exists_by_id(db, id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Gasto não encontrado"
        )
    SpentRepository.delete_by_id(db, id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put("/api/spents/{id}", response_model=SpentResponse)
def update(id: int, request: SpentRequest, db: Session = Depends(get_db)):
    if not SpentRepository.exists_by_id(db, id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Gasto não encontrado"
        )
    spent = SpentRepository.save(db, Spent(id=id, **request.model_dump()))
    return SpentResponse.model_validate(spent)

@app.get("/api/spents/total")
def get_total_spent(
    start_date: date = Query(None, description="Data de início (YYYY-MM-DD)"),
    end_date: date = Query(None, description="Data de fim (YYYY-MM-DD)"),
    year: int = Query(None, description="Ano (ex: 2024)"),
    month: int = Query(None, description="Mês (1-12)"),
    db: Session = Depends(get_db)
):
    if year and month:
        total = SpentRepository.get_total_spent_by_month(db, year, month)
    elif start_date and end_date:
        total = SpentRepository.get_total_spent(db, start_date, end_date)
    else:
        raise HTTPException(status_code=400, detail="Forneça um intervalo de datas ou um ano e mês.")

    return {"total_spent": total}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
