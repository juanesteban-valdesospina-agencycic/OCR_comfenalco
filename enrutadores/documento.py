from fastapi import APIRouter, Depends, HTTPException, UploadFile
from dependencias import obtener_servicio_documento
router = APIRouter(
    prefix="/ocr",
    tags=["OCR"]
)

@router.post("/{id_documento}/procesar")
def procesar_documento(id_documento: int, archivo: UploadFile, servicio=Depends(obtener_servicio_documento)):
    try:
        return servicio.procesar_documento(id_documento=id_documento, archivo=archivo)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except NotImplementedError as e:
        raise HTTPException(status_code=501, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error interno del servidor")
