from pydantic import BaseModel


class ResultadosCalidad(BaseModel):
    id: int
    id_cons: int
    id_doc: int
    resultado_calidad: str

