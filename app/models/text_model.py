from typing import Annotated, Literal

from pydantic import BaseModel, ConfigDict, StringConstraints

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
