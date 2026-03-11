import pytest
from playwright.sync_api import sync_playwright

# Endereço local 
API_URL = "http://127.0.0.1:8000"

def test_predict_endpoint_retorna_score_valido():
    with sync_playwright() as p:
        # 1. Inicia o contexto de API do Playwright
        request_context = p.request.new_context(base_url=API_URL)
        
        # 2. Cria o pacote de dados (JSON) do "cliente fantasma"
        payload_cliente = {
            "mes": 1, "idade": 31.0, "profissao": "empresario", "salario_anual": 19300.34,
            "num_contas": 6.0, "num_cartoes": 7.0, "juros_emprestimo": 17.0, "num_emprestimos": 5.0,
            "dias_atraso": 52.0, "num_pagamentos_atrasados": 19.0, "num_verificacoes_credito": 8.0,
            "mix_credito": "Ruim", "divida_total": 4500.00, "taxa_uso_credito": 29.93,
            "idade_historico_credito": 218.0, "investimento_mensal": 44.5,
            "comportamento_pagamento": "baixo_gasto_pagamento_baixo", "saldo_final_mes": 312.48,
            "emprestimo_carro": 1, "emprestimo_casa": 1, "emprestimo_pessoal": 0,
            "emprestimo_credito": 0, "emprestimo_estudantil": 0
        }
        
        # 3. Dispara o 'tiro' POST contra a sua API
        resposta = request_context.post("/predict", data=payload_cliente)
        
        # 4. Validações (Asserts) de Produção
        # A API tem que responder 200 OK (não pode dar erro 500 de servidor)
        assert resposta.ok, f"A API retornou erro: {resposta.status} - {resposta.status_text}"
        assert resposta.status == 200
        
        dados_resposta = resposta.json()
        
        # Verifica se a API devolveu os campos que o app do banco está esperando ler
        assert "score_previsto" in dados_resposta
        assert "confianca_percentual" in dados_resposta
        
        # Garante que a IA não inventou uma classe nova. Tem que ser uma das 3 que treinamos.
        assert dados_resposta["score_previsto"] in ["Good", "Standard", "Poor"]
        
        print(f"\n✅ Teste passou! A API está operante e retornou: {dados_resposta}")