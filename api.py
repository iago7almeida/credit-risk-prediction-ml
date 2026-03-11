from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import pandas as pd
import joblib

# 1. Instancia a aplicação API
app = FastAPI(
    title="API de Escoragem de Crédito",
    description="Motor de decisão de crédito utilizando Random Forest",
    version="1.0"
)

# 2. Carrega o modelo treinado (faz isso apenas uma vez quando a API sobe)
try:
    modelo_pipeline = joblib.load('models/modelo_risco_credito_v1.pkl')
    print("✅ Modelo carregado na memória do servidor.")
except FileNotFoundError:
    modelo_pipeline = None
    print("⚠️ Aviso: Arquivo .pkl não encontrado. A API não conseguirá prever sem ele.")

# 3. Define o contrato de dados (Esquema de Validação)
class ClienteRequest(BaseModel):
    mes: int
    idade: float
    profissao: str
    salario_anual: float
    num_contas: float
    num_cartoes: float
    juros_emprestimo: float
    num_emprestimos: float
    dias_atraso: float
    num_pagamentos_atrasados: float
    num_verificacoes_credito: float
    mix_credito: str
    divida_total: float
    taxa_uso_credito: float
    idade_historico_credito: float
    investimento_mensal: float
    comportamento_pagamento: str
    saldo_final_mes: float
    emprestimo_carro: int
    emprestimo_casa: int
    emprestimo_pessoal: int
    emprestimo_credito: int
    emprestimo_estudantil: int

@app.get("/")
def read_root():
    return {
        "mensagem": "API de Risco de Crédito Operacional 🚀",
        "status": "online",
        "documentacao": "Acesse /docs para testar a API"
    }

# 4. Cria a Rota (Endpoint) que vai receber os dados
@app.post("/predict")
def predict_score(cliente: ClienteRequest):
    if modelo_pipeline is None:
        raise HTTPException(status_code=500, detail="Modelo indisponível no servidor.")
    
    # Transforma o JSON recebido em um DataFrame de uma linha (formato que o Scikit-Learn exige)
    df_cliente = pd.DataFrame([cliente.model_dump()])
    
    # Realiza a predição através do seu Pipeline
    previsao = modelo_pipeline.predict(df_cliente)[0]
    probabilidades = modelo_pipeline.predict_proba(df_cliente)[0]
    confianca = round(max(probabilidades) * 100, 2)
    
    # Devolve a resposta para quem chamou a API
    return {
        "status": "sucesso",
        "score_previsto": previsao,
        "confianca_percentual": confianca
    }