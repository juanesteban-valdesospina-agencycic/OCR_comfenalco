import os
import time
import tempfile
import requests
from fastapi import UploadFile
from dotenv import load_dotenv
from typing import Optional

load_dotenv()


class RepositorioHandwritingOcr:
    def __init__(self):
        self.api_token = os.getenv("HANDWRITING_TOKEN")
        self.base_url = "https://www.handwritingocr.com/api/v3"
        print(f"API Token loaded: {'Yes' if self.api_token else 'No'}")

    async def extraer_texto(self, archivo: UploadFile) -> str:
        # Guardar el archivo en una ubicación temporal
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
            contents = await archivo.read()
            tmp.write(contents)
            tmp_path = tmp.name

        try:
            response = self._subir_documento(tmp_path)
            id = response.json().get("id")
            resultado = self._wait_for_result(id)
            return resultado
        except Exception as e:
            print(f"Error al subir el documento: {e}")
            return ""

    def _get_headers(self) -> dict:
        if not self.api_token:
            raise ValueError("HANDWRITING_TOKEN is not set in the environment variables.")
        return {
            "Authorization": f"Bearer {self.api_token}",
            "Accept": "application/json"
        }

    def _subir_documento(self, ruta_archivo: str) -> Optional[requests.Response]:
        url = f"{self.base_url}/documents"
        headers = self._get_headers()
        print(headers)

        with open(ruta_archivo, "rb") as archivo:
            files = {
                "file": (os.path.basename(ruta_archivo), archivo, "application/pdf")
            }
            data = {
                "action": "transcribe"
            }
            response = requests.post(url, headers=headers, files=files, data=data)

        print(f"Response status code: {response.status_code}")
        try:
            print("Response Json:", response.json())
        except Exception:
            print("No JSON en la respuesta.")

        return response

    def _wait_for_result(self, document_id: str, attempts: int = 20, wait_time: int = 5) -> Optional[str]:
        url = f"{self.base_url}/documents/{document_id}.txt"
        headers = self._get_headers()

        for i in range(attempts):
            response = requests.get(url, headers=headers)
            if response.status_code == 202:
                print(f"procesando")
                time.sleep(wait_time)
                continue
            elif response.status_code != 200:
                print(f"Error al obtener el resultado: {response.status_code} - {response.text}")
                return None
            else:
                data = response.text
                return data
        return None
