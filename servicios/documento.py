from fastapi import UploadFile
from esquemas.documento import DocumentoProcesado
from utilidades.crear_prompt import generar_prompt
from repositorios.interfaces.parametros_datos import IRepositorioParametrosDatos
from repositorios.interfaces.ocr import IRepositorioOcr
from repositorios.interfaces.ia import IRepositorioIA
from servicios.interfaces.documentos import IServicioDocumento
from io import BytesIO

class ServicioDocumento(IServicioDocumento):

    def __init__(self, repositorio_parametros_datos: IRepositorioParametrosDatos, repositorio_aws: IRepositorioOcr,
                 repositorio_handwriting: IRepositorioOcr, repositorio_openai: IRepositorioIA):
        self.repositorio_aws = repositorio_aws
        self.repositorio_openai = repositorio_openai
        self.repositorio_handwriting = repositorio_handwriting
        self.repositorio = repositorio_parametros_datos

    async def procesar_documento(self, id_documento: int, archivo: UploadFile) -> DocumentoProcesado:
        try:
            # Leer el contenido una sola vez en memoria
            contenido = await archivo.read()

            # Crear copias en memoria para cada OCR
            archivo_aws = UploadFile(filename=archivo.filename, file=BytesIO(contenido))
            archivo_handwriting = UploadFile(filename=archivo.filename, file=BytesIO(contenido))

            texto_aws = await self.repositorio_aws.extraer_texto(archivo_aws)
            print(f"Texto extraído de AWS: {texto_aws}")

            texto_handwriting = await self.repositorio_handwriting.extraer_texto(archivo_handwriting)
            print(f"Texto extraído de Handwriting OCR: {texto_handwriting}")

            prompt = self._obtener_prompt(id_documento)
            print(f"Prompt generado: {prompt}")
            texto = "TEXTO AWS TEXTRACT \n" + texto_aws + "\nTEXTO HANDWRITING OCR\n" + texto_handwriting

            resultado = await self.repositorio_openai.procesar_con_prompt(
                texto=texto, archivo=archivo, prompt=prompt
            )
            print(f"Resultado del procesamiento: {resultado}")

            return DocumentoProcesado(id_documento=id_documento, resultado=resultado)

        except Exception as e:
            print(f"Error al procesar el documento: {e}")
            raise e

    def _obtener_prompt(self, id_documento: int, detalles_adicionales: str = "") -> str:
        parametros = self.repositorio.obtener_parametros_documento(id_documento)
        explicacion_texto = ""
        for parametro in parametros:
            explicacion_texto += str(parametro)+"\n"
        estructura_json: dict = self.repositorio.obtener_parametros_documentos_en_formato_json_para_prompt(id_documento)
        if not parametros or len(parametros) == 0:
            raise ValueError(f"No se encontraron parámetros para el documento con ID {id_documento}")
        else:
            if id_documento == 6:
                return generar_prompt(
                    document_information="Afiliacion Trabajador",
                    estructura_json=str(estructura_json),
                    detalles_adicionales=detalles_adicionales,
                    explicacion_campos=explicacion_texto
                )
            else:
                raise NotImplementedError(f"No hay prompt definido para el documento con ID {id_documento}")
