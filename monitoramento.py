import pandas as pd
import numpy as np

def check_data_drift():
    print("🔍 Iniciando auditoria de Data Drift (Desvio de Dados)...")

    # 1. Carrega os dados originais de treinamento (A Referência)
    try:
        df_treino = pd.read_csv('data/clientes.csv')
        df_producao = pd.read_csv('data/novos_clientes.csv')
    except FileNotFoundError as e:
        print(f"❌ Erro ao carregar as bases de dados: {e}")
        return

    # 2. Escolhe variáveis críticas do negócio para monitorar
    features_criticas = ['idade', 'salario_anual', 'taxa_uso_credito', 'dias_atraso']

    drift_detectado = False

    print("-" * 50)
    for col in features_criticas:
        # Calcula a média das colunas nas duas bases
        media_treino = df_treino[col].mean()
        media_producao = df_producao[col].mean()

        # variação percentual entre o passado e o presente
        variacao = abs((media_producao - media_treino) / media_treino) * 100

        print(f"📊 Variável: {col.upper()}")
        print(f"   Média no Treino: {media_treino:.2f}")
        print(f"   Média em Produção (Hoje): {media_producao:.2f}")
        print(f"   Variação: {variacao:.2f}%")

        # Se a variação passar de 15%, consideramos que o público mudou demais
        if variacao > 15.0:
            print(f"   ⚠️ ALERTA: Desvio drástico detectado na variável '{col}'!")
            drift_detectado = True
        print("-" * 50)

    # 3. Veredito Final
    if drift_detectado:
        print("🚨 CONCLUSÃO: O comportamento financeiro dos clientes mudou significativamente.")
        print("   Ação Automática: Disparando pipeline de re-treino do modelo na AWS...")
        # Aqui, na vida real, você colocaria um código para acionar o AWS CodeBuild ou mandar um Slack
    else:
        print("✅ CONCLUSÃO: Os dados de produção estão estáveis. O modelo continua confiável.")

if __name__ == "__main__":
    check_data_drift()