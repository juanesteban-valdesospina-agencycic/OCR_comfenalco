from fastapi import APIRouter, Depends, HTTPException, UploadFile
from dependencias import obtener_servicio_documento
import os
router = APIRouter(
    prefix="/ocr",
    tags=["OCR"]
)

@router.post("/{id_documento}/procesar")
async def procesar_documento(id_documento: int, archivo: UploadFile, servicio=Depends(obtener_servicio_documento)):
    try:
        validar_y_normalizar_archivo(archivo)
        return await servicio.procesar_documento(id_documento=id_documento, archivo=archivo)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except NotImplementedError as e:
        raise HTTPException(status_code=501, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error interno del servidor")





EXTENSIONES_PERMITIDAS = {"pdf", "jpg", "jpeg", "png", "tiff","tif"}

def validar_y_normalizar_archivo(archivo: UploadFile) -> None:
    if not archivo.filename:
        raise HTTPException(status_code=400, detail="El archivo debe tener un nombre válido")

    # Obtener extensión
    nombre_archivo = archivo.filename
    extension = os.path.splitext(nombre_archivo)[1].lower().strip(".")

    # Si es .tiff, cambiar a .tif
    if extension == "tif":
        archivo.filename = nombre_archivo.replace(".tif", ".tiff")

    if extension not in EXTENSIONES_PERMITIDAS:
        raise HTTPException(
            status_code=400,
            detail=f"Tipo de archivo no permitido: .{extension}. Tipos permitidos: {', '.join(sorted(EXTENSIONES_PERMITIDAS))}"
        )