# 🚀 Motor de Escoragem de Crédito | Arquitetura MLOps de Ponta a Ponta

Este repositório contém o ciclo de vida completo de um modelo de Machine Learning para previsão de Risco de Crédito. O projeto vai muito além da modelagem matemática (Data Science), englobando engenharia de software, automação de testes, infraestrutura em nuvem (AWS) e painéis de Business Intelligence, caracterizando uma arquitetura **MLOps** de nível corporativo.

## 🎯 O Desafio de Negócio
Instituições financeiras precisam aprovar ou negar crédito em milissegundos. Este sistema utiliza um algoritmo de **Random Forest** treinado com dados de clientes para classificar o risco de inadimplência em três categorias: `Good`, `Standard` ou `Poor`. A aplicação garante que o modelo esteja sempre acessível via API, testado continuamente e monitorado contra degradação ao longo do tempo.

## 🛠️ Stack Tecnológico e Arquitetura

O ecossistema foi desenhado para ser resiliente, escalável e totalmente automatizado:

* **Machine Learning (Core):** `Python`, `Scikit-Learn`, `Pandas`. Implementação de *Pipelines* robustos para evitar vazamento de dados (Data Leakage) no pré-processamento.
* **Armazenamento de Artefatos:** `AWS S3` integrado via `boto3`. O repositório Git mantém-se leve apenas com código; os modelos pesados (`.pkl`) são hospedados de forma segura na nuvem.
* **Serving (API):** `FastAPI` e `Uvicorn` para servir o modelo com alta performance, documentação automática (Swagger UI) e validação estrita do contrato de dados via Pydantic.
* **Automação de Testes (E2E):** `Playwright` e `Pytest`. Simulação de requisições reais de sistemas parceiros validando o tempo de resposta e a acurácia do *endpoint*.
* **CI/CD (Integração Contínua):** `GitHub Actions`. Esteira automatizada que levanta o ambiente, baixa o artefato da AWS, sobe a API e atira testes E2E a cada *push* na branch principal.
* **Monitoramento Ativo (Data Drift):** `AWS EventBridge` (agendamento cron), `AWS CodeBuild` (execução do ambiente) e `AWS SNS` (mensageria). Sistema autônomo que audita os dados de entrada mensalmente e alerta a equipe de risco por e-mail caso os padrões financeiros dos clientes sofram alterações drásticas.
* **Business Intelligence:** Relatórios e *dashboards* interativos criados no `Looker Studio` para acompanhamento de KPIs de aprovação, distribuição de risco e explicabilidade da inteligência artificial.

## 📂 Estrutura do Repositório

```text
├── data/                   # Datasets de treino e relatórios de produção (CSV)
├── models/                 # Diretório local temporário para os arquivos .pkl
├── .github/workflows/      # Esteira de CI/CD (ci.yml)
├── train.py                # Pipeline de treino e upload do artefato para o AWS S3
├── predict.py              # Script de inferência em lote gerando outputs para BI
├── api.py                  # Servidor FastAPI expondo o modelo via REST
├── test_api.py             # Testes automatizados de integração com Playwright
├── monitoramento.py        # Cão de guarda para cálculo de Data Drift
├── buildspec.yml           # Instruções de execução para o AWS CodeBuild
├── Dockerfile              # Empacotamento da aplicação para deploy em nuvem
├── .dockerignore           # Regras de exclusão para o contêiner
├── .gitignore              # Regras de exclusão de artefatos e dados sensíveis
└── requirements.txt        # Gerenciamento de dependências Python
```
## ⚙️ Como Executar Localmente

### 1. Clone o repositório e instale as dependências:

git clone [https://github.com/iago7almeida/credit-risk-prediction-ml.git](https://github.com/iago7almeida/credit-risk-prediction-ml.git)
cd credit-risk-prediction-ml
pip install -r requirements.txt
playwright install

### 2. Autentique-se na AWS (Necessário para baixar/enviar o modelo):

aws configure

### 3. Treine o modelo e envie para o S3:

python train.py

### 4. Inicie o Servidor da API:

uvicorn api:app --reload

Acesse http://127.0.0.1:8000/docs no navegador para interagir visualmente com a IA.


### 5. Execute a bateria de testes:
Em um novo terminal, dispare os testes contra a API em funcionamento:

pytest test_api.py -s

## 🛡️ Segurança e Boas Práticas

  - Zero Credenciais no Código: Todas as chaves da AWS (AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY) são gerenciadas estritamente através dos Secrets do GitHub.
  - Isolamento de Contêiner: A aplicação conta com um Dockerfile enxuto focado em produção, padronizando a execução em qualquer infraestrutura sem problemas de compatibilidade.
