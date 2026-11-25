from pydantic import BaseModel, ConfigDict, Field

from app.models import EstadoIngesta, EstadoSalud, TipoFuente, TipoPagina


class FuenteBase(BaseModel):
    titulo: str = Field(min_length=1, max_length=300)
    tipo: TipoFuente
    archivo_o_url: str = Field(min_length=1, max_length=1000)
    estado_ingesta: EstadoIngesta = EstadoIngesta.pendiente


class FuenteCreate(FuenteBase):
    pass


class FuenteUpdate(BaseModel):
    titulo: str | None = Field(default=None, min_length=1, max_length=300)
    tipo: TipoFuente | None = None
    archivo_o_url: str | None = Field(default=None, min_length=1, max_length=1000)
    estado_ingesta: EstadoIngesta | None = None


class FuenteOut(FuenteBase):
    model_config = ConfigDict(from_attributes=True)
    id: int


class PaginaBase(BaseModel):
    titulo: str = Field(min_length=1, max_length=300)
    tipo: TipoPagina
    contenido: str = ""
    enlaces: list[str] = Field(default_factory=list)
    estado_salud: EstadoSalud = EstadoSalud.sin_revisar


class PaginaCreate(PaginaBase):
    pass


class PaginaUpdate(BaseModel):
    titulo: str | None = Field(default=None, min_length=1, max_length=300)
    tipo: TipoPagina | None = None
    contenido: str | None = None
    enlaces: list[str] | None = None
    estado_salud: EstadoSalud | None = None


class PaginaOut(PaginaBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
    fuentes: list[FuenteOut] = Field(default_factory=list)


class FuenteDetalle(FuenteOut):
    paginas: list["PaginaResumen"] = Field(default_factory=list)


class PaginaResumen(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    titulo: str


FuenteDetalle.model_rebuild()
