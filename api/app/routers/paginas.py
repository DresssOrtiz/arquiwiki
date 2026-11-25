from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.db import get_db
from app.models import Fuente, Pagina
from app.schemas import PaginaCreate, PaginaOut, PaginaUpdate

router = APIRouter(prefix="/paginas", tags=["paginas"])


def _get_or_404(db: Session, pagina_id: int) -> Pagina:
    pagina = db.get(Pagina, pagina_id)
    if pagina is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Página no encontrada")
    return pagina


def _guardar(db: Session) -> None:
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status.HTTP_409_CONFLICT, "Ya existe una página con ese título")


@router.post("", response_model=PaginaOut, status_code=status.HTTP_201_CREATED)
def crear(datos: PaginaCreate, db: Session = Depends(get_db)):
    pagina = Pagina(**datos.model_dump())
    db.add(pagina)
    _guardar(db)
    return pagina


@router.get("", response_model=list[PaginaOut])
def listar(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    consulta = select(Pagina).order_by(Pagina.id).offset(skip).limit(min(limit, 500))
    return db.scalars(consulta).all()


@router.get("/{pagina_id}", response_model=PaginaOut)
def obtener(pagina_id: int, db: Session = Depends(get_db)):
    return _get_or_404(db, pagina_id)


@router.put("/{pagina_id}", response_model=PaginaOut)
def actualizar(pagina_id: int, datos: PaginaUpdate, db: Session = Depends(get_db)):
    pagina = _get_or_404(db, pagina_id)
    for campo, valor in datos.model_dump(exclude_unset=True).items():
        setattr(pagina, campo, valor)
    _guardar(db)
    return pagina


@router.delete("/{pagina_id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar(pagina_id: int, db: Session = Depends(get_db)):
    pagina = _get_or_404(db, pagina_id)
    db.delete(pagina)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


# --- Relación N:M página <-> fuente ---


@router.put("/{pagina_id}/fuentes/{fuente_id}", response_model=PaginaOut)
def vincular_fuente(pagina_id: int, fuente_id: int, db: Session = Depends(get_db)):
    pagina = _get_or_404(db, pagina_id)
    fuente = db.get(Fuente, fuente_id)
    if fuente is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Fuente no encontrada")
    if fuente not in pagina.fuentes:
        pagina.fuentes.append(fuente)
        db.commit()
    return pagina


@router.delete("/{pagina_id}/fuentes/{fuente_id}", response_model=PaginaOut)
def desvincular_fuente(pagina_id: int, fuente_id: int, db: Session = Depends(get_db)):
    pagina = _get_or_404(db, pagina_id)
    fuente = next((f for f in pagina.fuentes if f.id == fuente_id), None)
    if fuente is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "La página no cita esa fuente")
    pagina.fuentes.remove(fuente)
    db.commit()
    return pagina
