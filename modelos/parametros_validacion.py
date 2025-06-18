from pydantic import BaseModel


class ParametrosValidacion(BaseModel):
    id_parametro: int
    id_tipo_doc: int
    id_tipo_validacion: int
    estado: str

