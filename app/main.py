from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routes.auth_routes import auth_router

app = FastAPI()


#CONFIGURAÇÃO DO CORS(EDITAR AQUI DE ACORDO COM O FRONTEND)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",     
        "http://127.0.0.1:5173",   
        "http://localhost:3000",     
    ],
    allow_credentials=True,
    allow_methods=["*"],       
    allow_headers=["*"],             
)


# INCLUINDO ROTAS
app.include_router(auth_router)


# ROTA RAIZ
@app.get("/")
async def root():
    return {"message": "API Python com FastAPI!"}
