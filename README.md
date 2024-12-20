# Passa a Passo para utilizar a API

### Documentação e descrição completa da API:

- [Link para acessar a documentação](https://github.com/Kauanrodrigues01/documentacao-teacherhunt)

### Requisitos:
- VS Code
- Python
- XAMPP (Mariadb 10.5 ou superior)
- MySQL

OBS: Se não for o Mariadb 10.5 ou superior pode dar um erro

**links para instalação:**
- [Python](https://www.python.org/ftp/python/3.12.6/python-3.12.6-amd64.exe)
- [XAMPP](https://sourceforge.net/projects/xampp/files/XAMPP%20Windows/8.2.12/xampp-windows-x64-8.2.12-0-VS16-installer.exe)
- [MySQL](https://dev.mysql.com/get/Downloads/MySQLGUITools/mysql-workbench-community-8.0.38-winx64.msi)

**Link para video de atualização do Mariadb:**
- [link para atualização do Mariadb no XAMPP](https://youtu.be/0zEMZ1yO5A8?si=sPB2yDbfHb9K-xN0)

### **Executar a API usando docker e docker-compose:**
- [Link para acessar o passo a passo](#docker)

## Primeiros passos para usar a API

- Abrir o XAMPP botar o apache o MySQL para rodar.
- Abrir o MySQL workbench, criar uma connection com o **nome de usuário "root"**, o **hostname "127.0.0.1"**, a **port "3306"**.
- Depois da connection criada, acesse ela e crie uma database com o nome **"teacherhunt"**

    ```
    CREATE DATABASE teacherhunt
    CHARACTER SET utf8
    COLLATE utf8_general_ci;
    ```

- Depois da database criada, vai no github e baixe ou faça um clone do repositório
- Com o projeto no seu PC abra ele no vscode, abra o terminal e digite **"python -m venv venv"**, depois **"venv/scripts/activate"**, depois disso tem que instalar as dependências, use o comando **"pip install -r requirements.txt"**
    ```
    python -m venv venv

    venv/scripts/activate

    pip install -r requirements.txt
    ```

- Após todas as dependências instaladas, crie o arquivo **".env"** dentro do diretório principal, **cuidado para não criar ele dentro de outra paste sem ser o diretório principal**, coloque o seguinte conteúdo dentro do arquivo **".env"**
    ```
    SECRET_KEY=-px9!&aurijpz9e*f_c8)jov!v=++5hx6r%vslywp2^l+8*@gr
    DEBUG=True
    ALLOWED_HOSTS=*
    DATABASE_URL=mysql://root@127.0.0.1:3306/teacherhunt
    # mysql://username:password@host:port/database
    ACCESS_TOKEN_LIFETIME_SECONDS = 3600
    REFRESH_TOKEN_LIFETIME_SECONDS = 7200
    ```

- Depois disso volte no terminal e execute o comando "python manage.py migrate"
- Pronto, a API está pronta para usar, para ativar o servidor use o comando "python manage.py runserver"

    ```
    python manage.py migrate

    # Iniciar o servidor
    python manage.py runserver
    ```

## Popular banco de dados(Opcional)
- Executando o arquivo populate, o banco de dados vai se preencher com vários dados aleatórios. Pode ajudar no desenvolvimento do front e mobile, pois vai ter dados para serem visualizados na aplicação.
    ```
    python populate.py
    ```

<a id="docker"></a>

# Executando a API com Docker

- Execute no terminal:
    ```
    docker-compose up --build
    ```

- Certifique-se de que os container estejam rodando:
    ```
    docker start teacherhunt-db

    docker start teacherhunt-app
    ```

## **Aviso importante:**

- Sempre que fechar e abrir o VS Code tem que ativar a venv(ambiente virtual) antes de utilizar o "python manage.py runserver", sempre verificar se a venv está ativa antes de iniciar o servidor.
- Quando a venv está ativa fica o nome (venv) em cima da linha principal do terminal
