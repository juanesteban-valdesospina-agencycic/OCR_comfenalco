from pydantic import BaseModel


class ResultadosValidacion(BaseModel):
    id: int
    id_cons: int
    id_doc: int
    id_validacion: int
    resultado_validacion: str

