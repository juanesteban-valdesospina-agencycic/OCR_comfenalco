from fastapi import UploadFile

from esquemas.documento import DocumentoProcesado
from utilidades.crear_prompt import generar_prompt
from repositorios.interfaces.parametros_datos import IRepositorioParametrosDatos
from repositorios.interfaces.ocr import IRepositorioOcr
from repositorios.interfaces.ia import IRepositorioIA
from servicios.interfaces.documentos import IServicioDocumento


class ServicioDocumento(IServicioDocumento):

    def __init__(self, repositorio_parametros_datos: IRepositorioParametrosDatos, repositorio_aws: IRepositorioOcr,
                 repositorio_handwriting: IRepositorioOcr, repositorio_openai: IRepositorioIA):
        self.repositorio_aws = repositorio_aws
        self.repositorio_openai = repositorio_openai
        self.repositorio_handwriting = repositorio_handwriting
        self.repositorio = repositorio_parametros_datos

    def procesar_documento(self, id_documento: int, archivo: UploadFile) -> DocumentoProcesado:
        texto_aws = self.repositorio_aws.extraer_texto(archivo)
        texto_handwriting = self.repositorio_handwriting.extraer_texto(archivo)
        texto_para_prompt = "EXTRACTED TEXT FROM AWS:\n" + texto_aws + "\n\nEXTRACTED TEXT FROM HANDWRITING:\n" + texto_handwriting
        prompt = self._obtener_prompt(id_documento)
        resultado = self.repositorio_openai.procesar_con_prompt(texto=texto_para_prompt, archivo=archivo, prompt=prompt)
        return DocumentoProcesado(id_documento=id_documento, resultado=resultado)

    def _obtener_prompt(self, id_documento: int, detalles_adicionales: str = "") -> str:
        parametros = self.repositorio.obtener_parametros_documento(id_documento)
        estructura_json: dict = self.repositorio.obtener_parametros_documentos_en_formato_json_para_prompt(id_documento)
        if not parametros or len(parametros) == 0:
            raise ValueError(f"No se encontraron parámetros para el documento con ID {id_documento}")
        else:
            if id_documento == 6:
                return generar_prompt(
                    document_information=parametros[0]['nombre'],
                    estructura_json=str(estructura_json),
                    detalles_adicionales=detalles_adicionales
                )
            else:
                raise NotImplementedError(f"No hay prompt definido para el documento con ID {id_documento}")
