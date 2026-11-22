import asyncio
import logging
from time import monotonic

from fastapi import APIRouter, HTTPException

from app.models.llm_model import (
    MODELO_ID,
    TEMPO_LIMITE,
    EntradaLonga,
    ModeloIndisponivel,
    resumir_texto,
)
from app.models.text_model import ErroResposta, ProcessarTextoEntrada, ProcessarTextoResposta

router = APIRouter(tags=["Processamento de texto"])
logger = logging.getLogger(__name__)


@router.post(
    "/processar_texto",
    response_model=ProcessarTextoResposta,
    responses={
        500: {"model": ErroResposta, "description": "Falha no processamento"},
        503: {"model": ErroResposta, "description": "Modelo local indisponível"},
        504: {"model": ErroResposta, "description": "Tempo limite excedido"},
    },
)
async def processar_texto(entrada: ProcessarTextoEntrada):
    prazo = monotonic() + TEMPO_LIMITE
    try:
        resumo = await asyncio.wait_for(
            asyncio.to_thread(resumir_texto, entrada.texto, prazo),
            timeout=TEMPO_LIMITE,
        )
        return ProcessarTextoResposta(modelo=MODELO_ID, texto_processado=resumo)
    except EntradaLonga as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
    except TimeoutError as exc:
        raise HTTPException(
            status_code=504, detail="O processamento excedeu 90 segundos. Tente um texto menor."
        ) from exc
    except (ModeloIndisponivel, ImportError, MemoryError) as exc:
        logger.warning("Modelo local indisponível: %s", exc)
        raise HTTPException(
            status_code=503,
            detail="Modelo local indisponível ou ocupado. Verifique a instalação e tente novamente.",
        ) from exc
    except Exception as exc:
        logger.exception("Falha ao processar texto.")
        raise HTTPException(
            status_code=500, detail="Falha ao gerar o resumo. Consulte o log do servidor."
        ) from exc
