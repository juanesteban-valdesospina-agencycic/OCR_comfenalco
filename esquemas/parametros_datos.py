from pydantic import BaseModel
class RespuestaParametrosDatos(BaseModel):
    etiqueta_dato: str
    campo_dato: str
    tipo_dato: str
    activo: bool
    nombre:str
    descripcion:str
    detalle_dato:str
