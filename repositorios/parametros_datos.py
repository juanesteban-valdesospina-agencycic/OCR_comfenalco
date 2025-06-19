from repositorios.interfaces.parametros_datos import IRepositorioParametrosDatos
from esquemas.parametros_datos import RespuestaParametrosDatos
from utilidades.secciones.secciones_06 import obtener_secciones_formulario_trabajador


class RepositorioParametrosDatos(IRepositorioParametrosDatos):
    def __init__(self, conn, cursor):
        self.conn = conn
        self.cursor = cursor

    def obtener_parametros_documento(self, id_documento: int) -> list:
        try:
            sql = """
                SELECT etiqueta_dato, campo_dato, tipo_dato, activo, nombre, descripcion, detalle_dato
                FROM parametros_datos 
                INNER JOIN tipos_documentos 
                    ON tipos_documentos.id = parametros_datos.id_tipo_doc 
                WHERE parametros_datos.id_tipo_doc = %s 
                ORDER BY CAST(SUBSTRING(etiqueta_dato FROM '\\d+') AS INTEGER);
            """
            self.cursor.execute(sql, (id_documento,))
            filas = self.cursor.fetchall()
            return [(fila['etiqueta_dato'],fila['campo_dato'],fila['detalle_dato']) for fila in filas]  # Convertir a tuplas
        except Exception as e:
            self.conn.rollback()
            raise e
        # ❌ Ya no cerramos aquí la conexión ni el cursor
        # finally:
        #     self.cursor.close()
        #     self.conn.close()

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
                        campo: "" for campo in campos
                    }
                elif tipo == "list":
                    resultado[nombre] = [{campo: "" for campo in campos}]
            return resultado
        except Exception as e:
            print(f"Error al obtener parámetros: {e}")
            return {}
