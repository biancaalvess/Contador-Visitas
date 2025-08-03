# Use Python 3.11 como base
FROM python:3.11-slim

# Define diretório de trabalho
WORKDIR /app

# Instala dependências do sistema
RUN apt-get update && apt-get install -y \
    && rm -rf /var/lib/apt/lists/*

# Copia arquivos de dependências
COPY requirements.txt .

# Instala dependências Python
RUN pip install --no-cache-dir -r requirements.txt

# Copia código da aplicação
COPY . .

# Cria diretório para dados
RUN mkdir -p /app/data

# Define variáveis de ambiente
ENV FLASK_APP=app.py
ENV FLASK_ENV=production
ENV ARQUIVO_VISITAS=/app/data/visitas.json
ENV PORT=5000

# Expõe a porta
EXPOSE 5000

# Define usuário não-root para segurança
RUN adduser --disabled-password --gecos '' appuser && \
    chown -R appuser:appuser /app
USER appuser

# Comando para iniciar a aplicação
CMD ["python", "app.py"]