from abc import ABC, abstractmethod

from fastapi import UploadFile


class IRepositorioOcr(ABC):
    @abstractmethod
    async def extraer_texto(self, archivo: UploadFile) -> str:
        pass
