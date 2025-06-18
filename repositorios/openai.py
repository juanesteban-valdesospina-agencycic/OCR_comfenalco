import os
import json
import base64
from io import BytesIO
from fastapi import UploadFile
from openai import OpenAI
from PIL import Image
from typing import Dict, Any

from repositorios.interfaces.ia import IRepositorioIA

class RepositorioOpenAI(IRepositorioIA):
    def __init__(self):
        api_key = os.getenv("OPENAI_TOKEN")
        if not api_key:
            raise ValueError("OPENAI_TOKEN no definido en variables de entorno.")
        self.client = OpenAI(api_key=api_key)
        self.model = "gpt-4o"

    async def procesar_con_prompt(self, texto: str, archivo: UploadFile, prompt: str) -> Dict[str, Any]:
        try:
            contenido_base64 = await self._convertir_archivo_a_base64(archivo)
        except Exception as e:
            print(f"Error al convertir archivo a base64: {e}")
            return {}

        user_content = [
            {"type": "text", "text": prompt},
            {"type": "text", "text": texto}
        ]

        if contenido_base64:
            user_content.append({
                "type": "image_url",
                "image_url": {"url": f"data:image/jpeg;base64,{contenido_base64}"}
            })

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a data extraction expert system."},
                    {"role": "user", "content": user_content}
                ],
                temperature=0.0,
                max_tokens=12000,
            )

            respuesta = response.choices[0].message.content
            try:
                clean_json = respuesta.strip().removeprefix("```json").removesuffix("```")
                return json.loads(clean_json)
            except json.JSONDecodeError as e:
                print(f"Error al decodificar JSON: {e}")
                print("Respuesta cruda del modelo:\n", respuesta)
                return {}

        except Exception as e:
            print(f"Error al llamar a OpenAI: {e}")
            return {}

    async def _convertir_archivo_a_base64(self, archivo: UploadFile) -> str:
        try:
            contenido = await archivo.read()
            with Image.open(BytesIO(contenido)) as img:
                buffered = BytesIO()
                formato = "JPEG"
                if img.format in ["PNG", "GIF"]:
                    formato = img.format
                img.save(buffered, format=formato, quality=80)
                return base64.b64encode(buffered.getvalue()).decode("utf-8")
        except Exception as e:
            raise RuntimeError(f"Error al procesar imagen: {e}")
