from db import get_connection
from servicios.documento import ServicioDocumento
from repositorios.parametros_datos import RepositorioParametrosDatos
from repositorios.aws_ocr import RepositorioAwsOcr
from repositorios.handwriting_ocr import RepositorioHandwritingOcr
from repositorios.openai import RepositorioOpenAI
from servicios.interfaces.documentos import IServicioDocumento


def obtener_servicio_documento() -> IServicioDocumento:
    conn, cursor = get_connection()
    repositorio_parametros_datos = RepositorioParametrosDatos(conn, cursor)
    repositorio_aws_ocr = RepositorioAwsOcr()
    repositorio_handwriting = RepositorioHandwritingOcr()
    repositorio_openai = RepositorioOpenAI()
    servicio_documentos = ServicioDocumento(repositorio_parametros_datos, repositorio_aws_ocr, repositorio_handwriting,
                                            repositorio_openai)
    return servicio_documentos
