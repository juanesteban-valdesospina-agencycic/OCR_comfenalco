from pydantic import BaseModel
from datetime import datetime

class ResultadosDatos(BaseModel):
    id_resultado: int
    id_cons: int
    id_tipo_doc: int
    id_parametro_dato: int
    resultado_validacion: str
    dato_extraido: str
    mensaje_error: str
    fecha_lectura: datetime
