from typing import Annotated, Literal

from pydantic import BaseModel, ConfigDict, Field, StringConstraints

MAX_CARACTERES = 2000
Texto = Annotated[
    str,
    StringConstraints(strip_whitespace=True, min_length=1, max_length=MAX_CARACTERES),
]


class ProcessarTextoEntrada(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True)

    texto: Texto


class ProcessarTextoResposta(BaseModel):
    tipo_analise: Literal["resumo"] = "resumo"
    modelo: str
    texto_processado: Texto


class ErroResposta(BaseModel):
    detail: str


class TurnoConversa(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True)

    pergunta: Texto
    resposta: Texto


class ConversaEntrada(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True)

    pergunta: Texto
    contexto: Texto
    historico: list[TurnoConversa] = Field(default_factory=list, max_length=3)


class ConversaResposta(BaseModel):
    modelo: str
    resposta: Texto
