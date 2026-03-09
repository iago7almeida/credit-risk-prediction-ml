import pandas as pd
import joblib

def predict_new_clients(input_path, output_path):
    print("⏳ Carregando o modelo de produção...")
    try:
        modelo = joblib.load('models/modelo_risco_credito_v1.pkl')
    except FileNotFoundError:
        print("❌ Erro: Modelo não encontrado. Rode o train.py primeiro.")
        return

    print("📁 Carregando base de novos clientes...")
    try:
        df_novos = pd.read_csv(input_path)
    except FileNotFoundError:
        print(f"❌ Erro: Arquivo {input_path} não encontrado.")
        return

    print("🎯 Gerando previsões e calculando confiança matemática...")
    previsoes = modelo.predict(df_novos)
    probabilidades = modelo.predict_proba(df_novos)
    
    # Criar DataFrame com os resultados
    df_resultado = df_novos.copy()
    df_resultado['Score_Previsto'] = previsoes
    df_resultado['Confianca_IA_(%)'] = (probabilidades.max(axis=1) * 100).round(2)
    
    # Exportar resultados
    df_resultado.to_csv(output_path, index=False)
    print(f"✅ Escoragem finalizada! Relatório salvo em: {output_path}")

if __name__ == "__main__":
    # Caminhos padrão para a execução do script
    ARQUIVO_ENTRADA = 'data/novos_clientes.csv'
    ARQUIVO_SAIDA = 'data/relatorio_novos_clientes_escorados.csv'
    
    predict_new_clients(ARQUIVO_ENTRADA, ARQUIVO_SAIDA)