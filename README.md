# Passa a Passo para utilizar a API

### Documentação e descrição completa da API:

- [Link para acessar a documentação](https://github.com/Kauanrodrigues01/documentacao-teacherhunt)

### Requisitos:
- VS Code
- Python
- Docker e Docker Compose

**links para instalação:**
- [Python](https://www.python.org/ftp/python/3.12.6/python-3.12.6-amd64.exe)
- [Docker](https://www.docker.com/products/docker-desktop)

### **Executar a API usando docker e docker-compose:**
- [Link para acessar o passo a passo](#docker)

## Primeiros passos para usar a API

- Certifique-se de que o Docker está instalado e em execução no seu sistema.
- Execute o seguinte comando no terminal para criar e iniciar um container com o banco de dados MySQL:
    ```
    docker run --name teacherhunt-db -e MYSQL_ROOT_PASSWORD=rootpassword -e MYSQL_DATABASE=teacherhunt -p 3306:3306 -d mysql:5.7
    ```
    
    - **MYSQL_ROOT_PASSWORD:** Substitua "rootpassword" pela senha desejada para o usuário root.
    - **MYSQL_DATABASE:** Garante que o banco de dados "teacherhunt" seja criado automaticamente.

- Depois de criar o container, vá ao GitHub e baixe ou faça um clone do repositório da API.
- Com o projeto no seu PC, abra-o no VS Code, abra o terminal e digite **"python -m venv venv"**, depois **"venv/scripts/activate"**, e em seguida instale as dependências com o comando **"pip install -r requirements.txt"**:
    ```
    python -m venv venv

    venv/scripts/activate

    pip install -r requirements.txt
    ```

- Após todas as dependências instaladas, crie o arquivo **".env"** dentro do diretório principal (cuidado para não criar o arquivo dentro de outra pasta que não seja o diretório principal) e insira o seguinte conteúdo:
    ```
    SECRET_KEY=-px9!&aurijpz9e*f_c8)jov!v=++5hx6r%vslywp2^l+8*@gr
    DEBUG=True
    ALLOWED_HOSTS=*
    DATABASE_URL=mysql://root:rootpassword@127.0.0.1:3306/teacherhunt
    # mysql://username:password@host:port/database
    ACCESS_TOKEN_LIFETIME_SECONDS = 3600
    REFRESH_TOKEN_LIFETIME_SECONDS = 7200
    ```

    **Nota:** Certifique-se de usar a mesma senha configurada no comando `docker run` para o campo `rootpassword`.

- Depois disso, volte ao terminal e execute os seguintes comandos para aplicar as migrações e iniciar o servidor:
    ```
    python manage.py migrate

    # Iniciar o servidor
    python manage.py runserver
    ```

## Popular banco de dados (Opcional)
- Executando o arquivo populate, o banco de dados será preenchido com vários dados aleatórios. Isso pode ajudar no desenvolvimento do front-end e mobile, pois haverá dados disponíveis para visualização na aplicação:
    ```
    python populate.py
    ```

<a id="docker"></a>

# Executando a API com Docker

- Execute no terminal:
    ```
    docker-compose up --build
    ```

- Certifique-se de que os containers estejam rodando:
    ```
    docker start teacherhunt-db

    docker start teacherhunt-app
    ```

## **Aviso importante:**

- Sempre que fechar e abrir o VS Code, ative a venv (ambiente virtual) antes de utilizar o "python manage.py runserver". Verifique se a venv está ativa antes de iniciar o servidor.
- Quando a venv está ativa, o nome (venv) aparece no início da linha principal do terminal.

