from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from app.models.text_model import ErroResposta
from app.routers.climate_router import router as climate_router
from app.routers.text_router import router as text_router

app = FastAPI(
    title="Painel ODS 13",
    responses={422: {"model": ErroResposta, "description": "Entrada inválida"}},
)
app.include_router(climate_router)
app.include_router(text_router)


@app.exception_handler(RequestValidationError)
async def tratar_entrada_invalida(request, exc):
    campos = ", ".join(
        dict.fromkeys(str(erro["loc"][-1]) for erro in exc.errors() if erro["loc"])
    )
    mensagem = f"Entrada inválida. Confira os campos em /docs ({campos})."
    if request.url.path.rstrip("/") == "/processar_texto":
        mensagem = "Envie JSON com o campo texto, contendo de 1 a 6000 caracteres."
    return JSONResponse(
        status_code=422, content=ErroResposta(detail=mensagem).model_dump()
    )
