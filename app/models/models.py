from pydantic import BaseModel, Field

class ClimateDiaryEntry(BaseModel):
    date: str = Field(..., description="Data da observação formato YYYY-MM-DD")
    temperature: float = Field(..., description="Temperatura em Ceulsius")
    observations: str = Field(..., description="Observações adicionais do usuário")

class ClimateConsultation(BaseModel):
    state: str = Field(..., description="Estado do Brasil")
    date: str = Field(..., description="Data da consulta formato YYYY-MM-DD")
    