import os
import time
from typing import Optional

import requests
import uuid
from dotenv import load_dotenv
from fastapi import UploadFile
from repositorios.interfaces.ocr import IRepositorioOcr

load_dotenv()


class RepositorioHandwritingOcr(IRepositorioOcr):
    def __init__(self):
        self.api_token = os.getenv("HANDWRITING_TOKEN")
        self.base_url = "https://www.handwritingocr.com/api/v3"

    async def extraer_texto(self, archivo: UploadFile) -> str:
        if not self.api_token:
            raise ValueError("HANDWRITING_TOKEN no definido en variables de entorno")

        nombre_temp = f"/tmp/{uuid.uuid4()}_{archivo.filename}"
        contenido = await archivo.read()
        with open(nombre_temp, "wb") as f:
            f.write(contenido)

        try:
            documento = self._subir_documento(nombre_temp)
            if not documento or not documento.get("id"):
                raise Exception("No se pudo obtener el ID del documento")

            resultado = self._esperar_resultado(documento["id"])
            if resultado.get("status") != "processed":
                raise Exception("No se pudo procesar el documento correctamente")

            texto = resultado["results"][0]["transcript"]
            return texto

        finally:
            if os.path.exists(nombre_temp):
                os.remove(nombre_temp)

    def _get_headers(self) -> dict:
        return {
            "Authorization": f"Bearer {self.api_token}",
            "Accept": "application/json"
        }

    def _subir_documento(self, path: str) -> Optional[dict]:
        with open(path, "rb") as f:
            files = {"file": f}
            data = {"action": "transcribe"}
            response = requests.post(
                f"{self.base_url}/documents",
                headers=self._get_headers(),
                files=files,
                data=data
            )
        if response.status_code == 201:
            return response.json()
        return None

    def _esperar_resultado(self, document_id: str, intentos: int = 20, espera: int = 5) -> Optional[dict]:
        for _ in range(intentos):
            response = requests.get(
                f"{self.base_url}/documents/{document_id}.json",
                headers=self._get_headers()
            )
            if response.status_code == 200:
                data = response.json()
                if data.get("status") == "processed":
                    return data
                elif data.get("status") in ["failed", "error"]:
                    return data
            time.sleep(espera)
        return {"status": "timeout"}
