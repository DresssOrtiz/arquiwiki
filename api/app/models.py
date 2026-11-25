import enum

from sqlalchemy import JSON, Column, Enum, ForeignKey, Integer, String, Table, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db import Base


class TipoFuente(str, enum.Enum):
    pdf = "pdf"
    markdown = "markdown"
    url = "url"
    otro = "otro"


class EstadoIngesta(str, enum.Enum):
    pendiente = "pendiente"
    ingestada = "ingestada"
    error = "error"


class TipoPagina(str, enum.Enum):
    concepto = "concepto"
    entidad = "entidad"
    comparacion = "comparacion"


class EstadoSalud(str, enum.Enum):
    sin_revisar = "sin_revisar"
    ok = "ok"
    con_problemas = "con_problemas"


pagina_fuente = Table(
    "pagina_fuente",
    Base.metadata,
    Column("pagina_id", ForeignKey("paginas.id", ondelete="CASCADE"), primary_key=True),
    Column("fuente_id", ForeignKey("fuentes.id", ondelete="CASCADE"), primary_key=True),
)


class Fuente(Base):
    __tablename__ = "fuentes"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    titulo: Mapped[str] = mapped_column(String(300))
    tipo: Mapped[TipoFuente] = mapped_column(Enum(TipoFuente, name="tipo_fuente"))
    archivo_o_url: Mapped[str] = mapped_column(String(1000))
    estado_ingesta: Mapped[EstadoIngesta] = mapped_column(
        Enum(EstadoIngesta, name="estado_ingesta"), default=EstadoIngesta.pendiente
    )

    paginas: Mapped[list["Pagina"]] = relationship(
        secondary=pagina_fuente, back_populates="fuentes"
    )


class Pagina(Base):
    __tablename__ = "paginas"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    titulo: Mapped[str] = mapped_column(String(300), unique=True)
    tipo: Mapped[TipoPagina] = mapped_column(Enum(TipoPagina, name="tipo_pagina"))
    contenido: Mapped[str] = mapped_column(Text, default="")
    enlaces: Mapped[list[str]] = mapped_column(JSON, default=list)
    estado_salud: Mapped[EstadoSalud] = mapped_column(
        Enum(EstadoSalud, name="estado_salud"), default=EstadoSalud.sin_revisar
    )

    fuentes: Mapped[list[Fuente]] = relationship(
        secondary=pagina_fuente, back_populates="paginas"
    )
