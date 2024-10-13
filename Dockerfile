# Usa a imagem oficial do Python 3.11 em uma versão minimalista chamada 'slim'.
FROM python:3.11-slim

# Instale as dependências necessárias
RUN apt-get update && \
    apt-get install -y gcc libmariadb-dev pkg-config && \
    rm -rf /var/lib/apt/lists/*

# Define o diretório de trabalho dentro do container como '/app'.
WORKDIR /app

# Copia o arquivo requirements.txt da máquina local para o diretório de trabalho no container.
COPY requirements.txt /app/

# Instala as dependências do Python listadas no arquivo requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copia todo o restante do código do diretório local para o diretório de trabalho no container.
COPY . /app/

# Expõe a porta 8000 do container para que seja possível acessar o servidor rodando no Django externamente.
EXPOSE 8000

# Define o comando padrão a ser executado ao iniciar o container.
CMD ["sh", "-c", "python manage.py migrate && python populate.py && python manage.py runserver 0.0.0.0:8000"]
