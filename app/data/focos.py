from io import BytesIO
from pathlib import Path
import unicodedata

import pandas as pd

INPE = "https://terrabrasilis.dpi.inpe.br/queimadas/bdqueimadas/"
EXEMPLO_INPE = Path(__file__).parent / "exemplos" / "inpe_aqua_20261031_20261101.csv"


def normalizar(nome: str) -> str:
    sem_acentos = unicodedata.normalize("NFKD", nome).encode("ascii", "ignore").decode()
    return sem_acentos.strip().lower()


def preparar_focos(conteudo: bytes) -> tuple[pd.DataFrame, dict]:
    opcoes = {"sep": None, "engine": "python", "dtype": str}
    try:
        bruto = pd.read_csv(BytesIO(conteudo), encoding="utf-8-sig", **opcoes)
    except UnicodeDecodeError:
        bruto = pd.read_csv(BytesIO(conteudo), encoding="latin1", **opcoes)

    bruto.columns = [normalizar(coluna) for coluna in bruto.columns]
    bruto = bruto.rename(columns={
        "data_hora_gmt": "datahora", "data_gmt": "datahora",
        "lat": "latitude", "lon": "longitude",
    })
    campos = ["datahora", "satelite", "pais", "estado", "latitude", "longitude"]
    ausentes = sorted(set(campos) - set(bruto.columns))
    if ausentes or bruto.columns.has_duplicates:
        raise ValueError(f"Cabeçalho inválido. Campos obrigatórios: {', '.join(campos)}.")

    focos = bruto[campos].copy()
    focos["datahora"] = pd.to_datetime(focos["datahora"], errors="coerce", utc=True, format="mixed")
    for coluna in ("latitude", "longitude"):
        focos[coluna] = pd.to_numeric(focos[coluna], errors="coerce")
    for coluna in ("pais", "estado", "satelite"):
        focos[coluna] = focos[coluna].str.strip().str.upper().replace("", pd.NA)

    validos = focos.dropna().loc[
        lambda linhas: linhas["latitude"].between(-90, 90)
        & linhas["longitude"].between(-180, 180)
    ]
    brasil = validos[validos["pais"].isin(["BRASIL", "BRAZIL"])]
    limpos = brasil.drop_duplicates(subset=["datahora", "satelite", "latitude", "longitude"])
    limpos = limpos.assign(
        dia=limpos["datahora"].dt.date,
        mes=limpos["datahora"].dt.strftime("%Y-%m"),
    ).sort_values("datahora")
    qualidade = {
        "Linhas lidas": len(bruto),
        "Linhas inválidas": len(bruto) - len(validos),
        "Fora do Brasil": len(validos) - len(brasil),
        "Duplicatas": len(brasil) - len(limpos),
        "Detecções válidas": len(limpos),
    }
    return limpos, qualidade


def resumir_focos(recorte: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame, dict[str, str]]:
    meses = recorte.groupby("mes").size().rename("Focos").reset_index()
    estados = recorte.groupby("estado", sort=True).size().rename("Focos").reset_index()
    estados = estados.sort_values("Focos", ascending=False, kind="stable")
    if meses.empty:
        return meses, estados, {}

    mes = meses.loc[meses["Focos"].idxmax()]
    estado = estados.iloc[0]
    empates_meses = int((meses["Focos"] == mes["Focos"]).sum())
    empates_estados = int((estados["Focos"] == estado["Focos"]).sum())
    nota_meses = f" (empate entre {empates_meses} meses)" if empates_meses > 1 else ""
    nota_estados = f" (empate entre {empates_estados} estados)" if empates_estados > 1 else ""
    fatos = {
        "E1": f"{len(recorte)} focos detectados no recorte.",
        "E2": f"{mes['mes']} concentrou {mes['Focos']} detecções no recorte, "
              f"a maior contagem no agrupamento por mês{nota_meses}.",
        "E3": f"{estado['estado']} teve a maior contagem por estado, "
              f"com {estado['Focos']} focos no recorte{nota_estados}.",
    }
    return meses, estados, fatos
