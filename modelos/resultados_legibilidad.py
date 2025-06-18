from pydantic import BaseModel


class ResultadosLegibilidad(BaseModel):
    id: int
    id_cons: int
    id_doc: int
    resultado_legibilidad: str

