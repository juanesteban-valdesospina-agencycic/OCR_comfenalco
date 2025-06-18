from pydantic import BaseModel


class ParametrosLegibilidad(BaseModel):
    id_parametro_legibilidad: int
    id_tipo_doc: int
    porcentaje_legibilidad: str
