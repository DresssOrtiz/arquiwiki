from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db import get_db
from app.models import Fuente
from app.schemas import FuenteCreate, FuenteDetalle, FuenteOut, FuenteUpdate

router = APIRouter(prefix="/fuentes", tags=["fuentes"])


def _get_or_404(db: Session, fuente_id: int) -> Fuente:
    fuente = db.get(Fuente, fuente_id)
    if fuente is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Fuente no encontrada")
    return fuente


@router.post("", response_model=FuenteOut, status_code=status.HTTP_201_CREATED)
def crear(datos: FuenteCreate, db: Session = Depends(get_db)):
    fuente = Fuente(**datos.model_dump())
    db.add(fuente)
    db.commit()
    return fuente


@router.get("", response_model=list[FuenteOut])
def listar(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    consulta = select(Fuente).order_by(Fuente.id).offset(skip).limit(min(limit, 500))
    return db.scalars(consulta).all()


@router.get("/{fuente_id}", response_model=FuenteDetalle)
def obtener(fuente_id: int, db: Session = Depends(get_db)):
    return _get_or_404(db, fuente_id)


@router.put("/{fuente_id}", response_model=FuenteOut)
def actualizar(fuente_id: int, datos: FuenteUpdate, db: Session = Depends(get_db)):
    fuente = _get_or_404(db, fuente_id)
    for campo, valor in datos.model_dump(exclude_unset=True).items():
        setattr(fuente, campo, valor)
    db.commit()
    return fuente


@router.delete("/{fuente_id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar(fuente_id: int, db: Session = Depends(get_db)):
    fuente = _get_or_404(db, fuente_id)
    db.delete(fuente)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
