# Painel ODS 13

Este projeto reúne dados históricos de temperatura e conteúdo sobre os efeitos do calor para apoiar a exploração de informações relacionadas ao ODS 13, Ação Contra a Mudança Global do Clima. O painel permite filtrar séries de temperatura, visualizar gráficos e baixar recortes dos dados em CSV.

Na página **Tire Sua Dúvida**, o usuário pode colar um boletim de queimadas ou outro texto sobre clima e receber um resumo em português. O Streamlit envia o texto ao FastAPI, que executa o modelo Qwen2.5-0.5B-Instruct localmente.

## Funcionalidades

- Explorar séries históricas de temperatura por país, estado e ano.
- Baixar recortes do painel em CSV.
- Consultar temperaturas por país e data pela API.
- Registrar e consultar observações no diário climático, mantidas em memória
  durante a execução da API.
- Gerar resumos em português de textos enviados pelo usuário.

## Tecnologias utilizadas

- **Python e pandas** para leitura e preparação dos dados.
- **Streamlit e Altair** para a interface e os gráficos.
- **FastAPI, Uvicorn e Pydantic** para execução da API e validação das entradas
  e respostas.
- **Transformers e PyTorch** para executar o modelo Qwen localmente.
- **Requests e BeautifulSoup** para coleta de conteúdo da web.

## Fontes de dados

- **Kaggle** para as séries históricas de temperatura.
- **Wikipédia** para a tabela climatológica de São Paulo.
- **Blog da Raia** para a reportagem exibida na página **Consequências**.

## Como executar

Abra um terminal na raiz do projeto, na pasta que contém `app/` e `requirements.txt`. Crie e ative o ambiente virtual, instale as dependências e baixe o modelo.

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python -m app.models.baixar_modelo
```

O download inicial do modelo exige internet. Depois disso, a geração dos resumos usa os arquivos locais. Mantenha `/app/models/weights/` no `.gitignore` para deixar os pesos fora do repositório.

No primeiro terminal, inicie a API.

```bash
HF_HUB_OFFLINE=1 python -m uvicorn app.main:app --host 127.0.0.1 --port 8000
```

Em outro terminal, na mesma pasta, inicie o painel.

```bash
source .venv/bin/activate
python -m streamlit run app/Home.py
```

| HTTP | Quando ocorre                                                                                                                                             |
| ---- | --------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 200  | Resumo gerado e validado pelo modelo Pydantic.                                                                                                            |
| 422  | JSON inválido, campo `texto` ausente, vazio ou com mais de 6.000 caracteres, campos extras ou entrada acima de 2.048 tokens incluindo as instruções. |
| 500  | Falha inesperada durante a geração. O servidor registra o diagnóstico.                                                                                 |
| 503  | Pesos ou dependências indisponíveis, erro de carregamento, ou outra inferência em andamento.                                                           |
| 504  | A solicitação excedeu 90 s, incluindo a primeira carga. A operação em CPU pode terminar o passo em curso depois de a API retornar.                    |

Os erros retornam `{"detail":"mensagem"}`, e o Streamlit mostra a mensagem ao usuário. A cada solicitação, a geração produz até 160 novos tokens. A consulta climática usa o CSV local por país e retorna 503 se a base estiver indisponível ou inválida. O diário climático continua em memória.

## Arquivos

- `app/main.py` registra as rotas e padroniza os erros de validação.
- `app/models/llm_model.py` carrega o modelo local e gera o resumo.
- `app/models/baixar_modelo.py` prepara os pesos e o tokenizador.
- `app/models/text_model.py` e `app/models/climate_model.py` definem os contratos Pydantic.
- `app/routers/text_router.py` implementa `POST /processar_texto`.
- `app/routers/climate_router.py` e `app/data/processed.py` mantêm as rotas climáticas e separam o acesso ao CSV da coleta web.
- `app/pages/Tire Sua Dúvida.py` contém o formulário de resumo e mostra o resultado ou o erro.
- `app/Home.py` e `app/pages/Consequencias.py` completam os arquivos Python enviados do painel.
