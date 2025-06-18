from pydantic import BaseModel


class DocumentoProcesado(BaseModel):
    id_tipo_doc: int
    resultado_procesamiento: dict




