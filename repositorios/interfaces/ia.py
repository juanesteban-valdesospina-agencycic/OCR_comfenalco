from abc import ABC, abstractmethod
from fastapi import UploadFile

class IRepositorioIA(ABC):
    @abstractmethod
    async def procesar_con_prompt(self,texto: str, archivo: UploadFile, prompt: str) -> dict:
        pass
