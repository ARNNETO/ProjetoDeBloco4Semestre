from fastapi import APIRouter, HTTPException
from ..data.processed import carregar_dados
from datetime import date as Date
import pandas as pd

from app.models.climate_model import ClimateConsultation, ClimateDiaryEntry, ClimateDiaryResponse

climate_diary = []
df_country, _, _, _ = carregar_dados()

router = APIRouter()

# ------------------------------------------------------------------------------
@router.post(
        "/registro-nova-temperatura",
        response_model=ClimateDiaryEntry,
        status_code=201
)
async def create_climate_diary_entry(entry: ClimateDiaryEntry):
    new_registry={"date": entry.date,
                "temperature":entry.temperature,
                "observations": entry.observations
    }
    climate_diary.append(new_registry)
    return new_registry

# ------------------------------------------------------------------------------
@router.get(
    "/consulta-diario-climatico",
    response_model=list[ClimateDiaryResponse],
)
async def get_climate_diary(date: Date | None = None):
    if date is None:
        return climate_diary
    registros = [
        entry
        for entry in climate_diary
        if entry["date"] == date
    ]
    if not registros:
        raise HTTPException(
            status_code=404,
            detail=f"Nenhum registro encontrado para a data {date}",
        )
    return registros

# ------------------------------------------------------------------------------
@router.get(
    "/consulta-temperatura-por-pais",
    response_model=list[ClimateConsultation]
)
async def get_temperature_by_contry(country: str, date: Date):
    country_data = df_country[
        (df_country["Country"] == country) &
        (df_country["dt"] == date)
    ]
    if country_data.empty:
        raise HTTPException(
            status_code=404,
            detail=(
                f"Nenhum registro encontrado para o país "
                f"{country} na data {date}"
            ),
        )
    return [
        {
            "country": row["Country"],
            "date": date,
            "temperature": (
                None
                if pd.isna(row["AverageTemperature"])
                else float(row["AverageTemperature"])
            ),
        }
        for _, row in country_data.iterrows()
    ]