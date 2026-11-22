from huggingface_hub import snapshot_download

from app.models.llm_model import MODELO_ID, MODELO_REVISAO, diretorio_modelo


if __name__ == "__main__":
    pasta = snapshot_download(
        repo_id=MODELO_ID,
        revision=MODELO_REVISAO,
        local_dir=diretorio_modelo(),
        allow_patterns=["*.json", "merges.txt", "vocab.json", "model.safetensors", "LICENSE"],
    )
    print(f"Modelo disponível em {pasta}")
