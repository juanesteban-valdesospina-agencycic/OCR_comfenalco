import boto3
from fastapi import UploadFile
from repositorios.interfaces.ocr import IRepositorioOcr
import uuid

class RepositorioAwsOcr(IRepositorioOcr):
    def __init__(self):
        self.textract = boto3.client("textract")
        self.s3 = boto3.client("s3")
        self.bucket_name = "formularios-trabajador"

    async def extraer_texto(self, archivo: UploadFile) -> str:
        nombre_archivo = f"{uuid.uuid4()}_{archivo.filename}"
        await self._subir_a_s3(archivo, nombre_archivo)

        response = self.textract.detect_document_text(
            Document={
                'S3Object': {
                    'Bucket': self.bucket_name,
                    'Name': nombre_archivo
                }
            }
        )

        lineas = [
            block['Text']
            for block in response.get('Blocks', [])
            if block['BlockType'] == 'LINE' and block['Confidence'] >= 50
        ]

        return "\n".join(lineas)

    async def _subir_a_s3(self, archivo: UploadFile, key: str):
        contenido = await archivo.read()
        self.s3.put_object(Bucket=self.bucket_name, Key=key, Body=contenido)
