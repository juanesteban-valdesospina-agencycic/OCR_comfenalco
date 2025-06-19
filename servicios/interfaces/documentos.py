from abc import ABC, abstractmethod
from esquemas.documento import DocumentoProcesado

class IServicioDocumento(ABC):
    @abstractmethod
    async def procesar_documento(self, id_documento : int, archivo) -> DocumentoProcesado:
        pass
