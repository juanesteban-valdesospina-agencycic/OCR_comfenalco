from repositorios.interfaces.parametros_datos import IRepositorioParametrosDatos
from esquemas.parametros_datos import RespuestaParametrosDatos
from utilidades.secciones.secciones_06 import obtener_secciones_formulario_trabajador


class RepositorioParametrosDatos(IRepositorioParametrosDatos):

    def __init__(self, conn, cursor):
        self.conn = conn
        self.cursor = cursor

    def obtener_parametros_documento(self, id_documento: int) -> list:
        try:
            sql = """SELECT etiqueta_dato, campo_dato, tipo_dato, activo, nombre, descripcion
FROM parametros_datos 
INNER JOIN tipos_documentos 
  ON tipos_documentos.id = parametros_datos.id_tipo_doc 
WHERE parametros_datos.id_tipo_doc = %s 
ORDER BY CAST(SUBSTRING(etiqueta_dato FROM '\d+') AS INTEGER);"""
            self.cursor.execute(sql, (id_documento,))
            filas = self.cursor.fetchall()

            return [RespuestaParametrosDatos(**fila) for fila in filas]
        except Exception as e:
            self.conn.rollback()
            raise e
        finally:
            self.cursor.close()
            self.conn.close()


def obtener_parametros_documentos_en_formato_json_para_prompt(self, id_documento: int) -> dict:
    try:
        parametros = self.obtener_parametros_documento(id_documento)
        if not parametros:
            return {}
        if id_documento == 6:
            secciones = obtener_secciones_formulario_trabajador()
        else:
            secciones = []

        resultado = {}

        for seccion in secciones:
            nombre = seccion["nombre"]
            campos = seccion["campos"]
            tipo = seccion["tipo"]

            if tipo == "dict":
                resultado[nombre] = {
                    p["etiqueta_dato"]: p["valor"]
                    for p in parametros
                    if p["etiqueta_dato"] in campos
                }

            elif tipo == "list":
                lista = []
                grupos = {}
                for p in parametros:
                    if p["etiqueta_dato"] in campos:
                        grupo = p.get("grupo", 0)
                        if grupo not in grupos:
                            grupos[grupo] = {}
                        grupos[grupo][p["etiqueta_dato"]] = p["valor"]
                resultado[nombre] = list(grupos.values())

        return resultado

    except Exception as e:
        print(f"Error al obtener parámetros: {e}")
        return {}
