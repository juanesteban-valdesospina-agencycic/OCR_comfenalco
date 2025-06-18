from pydantic import BaseModel


class ResultadosPrecios(BaseModel):
    id: int
    id_cons: int
    id_doc: int
    precio_calidad: float
    tokens_input_calidad: int
    tokens_output_calidad: int
    precio_legibilidad: float
    tokens_input_legibilidad: int
    tokens_output_legibilidad: int
    precio_validacion: float
    tokens_input_validacion: int
    tokens_output_validacion: int
    precio_lectura: float
    tokens_input_lectura: int
    tokens_output_lectura: int
    paginas_leidas: int

