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
    responder_conversa,
)
from app.models.text_model import (
    ConversaEntrada,
    ConversaResposta,
    ErroResposta,
    ProcessarTextoEntrada,
    ProcessarTextoResposta,
)

router = APIRouter(tags=["Processamento de texto"])
logger = logging.getLogger(__name__)


ERROS = {
    500: {"model": ErroResposta, "description": "Falha no processamento"},
    503: {"model": ErroResposta, "description": "Modelo local indisponível"},
    504: {"model": ErroResposta, "description": "Tempo limite excedido"},
}


@router.post("/processar_texto", response_model=ProcessarTextoResposta, responses=ERROS)
async def processar_texto(entrada: ProcessarTextoEntrada):
    resumo = await executar_modelo(resumir_texto, entrada.texto)
    return ProcessarTextoResposta(modelo=MODELO_ID, texto_processado=resumo)


@router.post("/conversar", response_model=ConversaResposta, responses=ERROS)
async def conversar(entrada: ConversaEntrada):
    resposta = await executar_modelo(
        responder_conversa, entrada.pergunta, entrada.contexto, entrada.historico
    )
    return ConversaResposta(modelo=MODELO_ID, resposta=resposta)


async def executar_modelo(funcao, *dados):
    prazo = monotonic() + TEMPO_LIMITE
    try:
        return await asyncio.wait_for(
            asyncio.to_thread(funcao, *dados, prazo),
            timeout=TEMPO_LIMITE,
        )
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
            status_code=500, detail="Falha ao gerar a resposta. Consulte o log do servidor."
        ) from exc
