from pydantic import BaseModel


class ParametrosDatos(BaseModel):
    id_parametro_dato: int
    id_tipo_doc: int
    etiqueta_dato: str
    campo_dato: str
    tipo_dato: str
    activo: bool
