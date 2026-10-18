from pydantic import BaseModel, Field
from datetime import date as Date

class ClimateDiaryEntry(BaseModel):
    date: Date = Field(description="Data da observação formato YYYY-MM-DD")
    temperature: float = Field( description="Temperatura em Ceulsius")
    observations: str = Field( description="Observações adicionais do usuário")

class ClimateDiaryResponse(ClimateDiaryEntry):
    pass

class ClimateConsultation(BaseModel):
    country: str = Field(description="Consulta por país")
    date: Date = Field(description="Data da consulta formato YYYY-MM-DD")
    temperature: float | None = Field(description="Temperatura média do país na data especificada")