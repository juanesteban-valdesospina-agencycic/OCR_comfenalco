# main.py
from fastapi import FastAPI
from enrutadores.documento import router as documento_router

import uvicorn
app = FastAPI()
app.include_router(documento_router)



if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)