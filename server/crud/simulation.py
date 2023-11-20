from sqlalchemy.orm import Session

from server import models


def fetch_simulations(db: Session):
    return db.query(models.Simulation).all()
