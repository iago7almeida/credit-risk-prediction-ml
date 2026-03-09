import pandas as pd
import joblib
import boto3
from botocore.exceptions import NoCredentialsError
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.ensemble import RandomForestClassifier

# --- Configurações da AWS ---
BUCKET_NAME = 'credit-risk-prediction-ml-bucket'
S3_MODEL_PATH = 'modelos_producao/modelo_risco_credito_v1.pkl' # Onde ele vai ficar no S3

def upload_to_s3(local_file, bucket, s3_file):
    """Faz o upload do arquivo local para o Amazon S3."""
    s3_client = boto3.client('s3')
    try:
        print(f"☁️ Iniciando upload para o S3 (Bucket: {bucket})...")
        s3_client.upload_file(local_file, bucket, s3_file)
        print("✅ Upload para o S3 concluído com sucesso!")
    except FileNotFoundError:
        print("❌ Erro: O arquivo local não foi encontrado para o upload.")
    except NoCredentialsError:
        print("❌ Erro: Credenciais da AWS não encontradas.")
        print("Certifique-se de configurar o AWS CLI ou garantir que o CodeBuild tenha a role com permissão de escrita no S3.")

def train_model():
    print("⏳ Iniciando o processo de treinamento...")
    
    # 1. Carregar os dados
    try:
        df = pd.read_csv('data/clientes.csv')
    except FileNotFoundError:
        print("❌ Erro: Arquivo data/clientes.csv não encontrado.")
        return

    # 2. Separar features (X) e target (y)
    X = df.drop(columns=['score_credito', 'id_cliente'])
    y = df['score_credito']

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42, stratify=y)

    # 3. Configurar o pré-processamento
    cols_numericas = X_train.select_dtypes(include=['int64', 'float64']).columns.tolist()
    cols_categoricas = X_train.select_dtypes(include=['object']).columns.tolist()

    transformador_numerico = Pipeline(steps=[
        ('imputer', SimpleImputer(strategy='median')),
        ('scaler', StandardScaler())
    ])

    transformador_categorico = Pipeline(steps=[
        ('imputer', SimpleImputer(strategy='most_frequent')),
        ('onehot', OneHotEncoder(handle_unknown='ignore'))
    ])

    pre_processador = ColumnTransformer(
        transformers=[
            ('num', transformador_numerico, cols_numericas),
            ('cat', transformador_categorico, cols_categoricas)
        ])

    # 4. Construir o pipeline final
    pipeline_rf = Pipeline(steps=[
        ('preprocessor', pre_processador),
        ('classifier', RandomForestClassifier(n_estimators=200, max_depth=20, random_state=42, class_weight='balanced'))
    ])

    # 5. Treinar o model
    print("🧠 Treinando o algoritmo Random Forest...")
    pipeline_rf.fit(X_train, y_train)

    # 6. Salvar o modelo temporariamente na máquina/container
    caminho_modelo_local = 'models/modelo_risco_credito_v1.pkl'
    joblib.dump(pipeline_rf, caminho_modelo_local)
    print(f"💾 Modelo salvo localmente em: {caminho_modelo_local}")

    # 7. Disparar o envio do artefato para a AWS
    upload_to_s3(caminho_modelo_local, BUCKET_NAME, S3_MODEL_PATH)

if __name__ == "__main__":
    train_model()