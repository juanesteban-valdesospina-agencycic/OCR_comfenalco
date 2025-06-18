from fastapi import APIRouter, Depends, HTTPException
from esquemas.parametros_datos import ParametrosDatos
from servicios.usuario import ServicioUsuario
from dependencias import obtener_servicio_usuario
router = APIRouter(
    prefix="/usuarios",
    tags=["Usuarios"]
)

@router.post("/", response_model=RespuestaUsuario)
def crear_usuario(usuario: CrearUsuario, servicio: ServicioUsuario = Depends(obtener_servicio_usuario)):
    try:
        return servicio.crear_usuario(usuario)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/", response_model=list[RespuestaUsuario])
def obtener_todos_los_usuarios(servicio: ServicioUsuario = Depends(obtener_servicio_usuario)):
    try:
        return servicio.obtener_todos_los_usuarios()
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))