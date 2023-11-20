from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from server import schemas, dependencies
from server.crud import simulation as crud

router = APIRouter()


@router.get("/", response_model=List[schemas.SimulationBase])
def fetch_simulations(db: Session = Depends(dependencies.get_db)):
    return crud.fetch_simulations(db=db)
