from fastapi import FastAPI

from app.routes.auth_routes import auth_router

app = FastAPI()

# INCLUINDO ROTAS
app.include_router(auth_router)


# ROTA RAIZ
@app.get("/")
async def root():
    return {"message": "API Python com FastAPI!"}
