from pydantic import BaseModel


class ParametrosCalidad(BaseModel):
    id_parametro_calidad: int
    id_tipo_doc: int
    porcentage_calidad: str
