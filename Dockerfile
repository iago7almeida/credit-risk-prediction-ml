# 1. Usa uma imagem oficial do Python, versão 'slim' para ficar mais leve
FROM python:3.10-slim

# 2. Define o diretório de trabalho lá dentro do contêiner
WORKDIR /app

# 3. Copia APENAS o requirements primeiro. 
# Isso é um truque de MLOps: se o requirements não mudar, o Docker usa o cache e o build fica 10x mais rápido!
COPY requirements.txt .

# 4. Instala as bibliotecas (FastAPI, Pandas, Scikit-Learn, Joblib, etc.)
# O --no-cache-dir evita que o Docker guarde arquivos temporários de instalação, diminuindo o tamanho da imagem
RUN pip install --no-cache-dir -r requirements.txt

# 5. Copia todo o resto do seu projeto (os scripts .py e a pasta models/) para dentro do contêiner
COPY . .

# 6. Libera a porta 8000 para o mundo externo conseguir se comunicar com a API
EXPOSE 8000

# 7. O comando que liga o servidor assim que o contêiner nasce
CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8000"]