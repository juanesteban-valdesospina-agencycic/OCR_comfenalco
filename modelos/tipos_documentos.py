from pydantic import BaseModel


class TiposDocumentos(BaseModel):
    id: int
    categoria: str
