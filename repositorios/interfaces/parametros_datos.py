from abc import ABC, abstractmethod
from esquemas.parametros_datos import RespuestaParametrosDatos
from typing import List

class IRepositorioParametrosDatos(ABC):
    @abstractmethod
    def obtener_parametros_documento(self,id_documento:int) -> List[RespuestaParametrosDatos]:
        pass

    @abstractmethod
    def obtener_parametros_documentos_en_formato_json_para_prompt(self,id:int) -> dict:
        pass
