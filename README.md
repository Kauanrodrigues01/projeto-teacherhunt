# 🎓 TeacherHunt API

<div align="center">
  <img src="https://raw.githubusercontent.com/Kauanrodrigues01/Kauanrodrigues01/refs/heads/main/images/projetos/teacherhunt/swagger.jpeg" alt="TeacherHunt API Swagger Documentation" width="800"/>
</div>

<br>

> 🚀 Uma API REST robusta para conectar professores e alunos, desenvolvida com Django REST Framework

<div align="center">
  <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=white" alt="Django">
  <img src="https://img.shields.io/badge/DRF-ff1709?style=for-the-badge&logo=django&logoColor=white" alt="Django REST Framework">
  <img src="https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white" alt="PostgreSQL">
  <img src="https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white" alt="Docker">
  <img src="https://img.shields.io/badge/JWT-000000?style=for-the-badge&logo=JSON%20web%20tokens&logoColor=white" alt="JWT">
</div>

<br>

## 🎯 Sobre o Projeto

O **TeacherHunt** é uma plataforma que facilita a conexão entre professores e alunos, permitindo o agendamento de aulas particulares, avaliações, sistema de favoritos e muito mais. A API oferece um sistema completo de autenticação, gerenciamento de perfis e funcionalidades educacionais.

### 🎨 Principais Funcionalidades

- 🔐 **Sistema de Autenticação JWT** - Login, logout e refresh tokens
- 👥 **Gerenciamento de Usuários** - Professores e Alunos
- 📚 **Sistema de Matérias** - Categorização por disciplinas
- 📅 **Agendamento de Aulas** - Sistema completo de reservas
- ⭐ **Sistema de Avaliações** - Ratings e comentários
- ❤️ **Professores Favoritos** - Lista de favoritos personalizada
- 📧 **Reset de Senha** - Via email seguro
- 🔍 **Busca Avançada** - Filtros por preço, avaliação e matéria
- 📱 **Upload de Imagens** - Fotos de perfil
- 🌐 **CORS Configurado** - Para integração frontend

## 🛠 Tecnologias Utilizadas

### Backend

- **Python 3.12** - Linguagem principal
- **Django 5.1** - Framework web
- **Django REST Framework** - API REST
- **Simple JWT** - Autenticação JWT
- **drf-yasg** - Documentação Swagger/OpenAPI

### Banco de Dados

- **PostgreSQL** - Banco principal (suporte também para MySQL/MariaDB)
- **SQLite** - Desenvolvimento local

### DevOps & Ferramentas

- **Docker & Docker Compose** - Containerização
- **Pillow** - Processamento de imagens
- **django-cors-headers** - Configuração CORS
- **python-decouple** - Gerenciamento de variáveis ambiente

### Qualidade de Código

- **pytest** - Framework de testes
- **Black** - Formatação de código
- **pylint** - Análise estática

## 🏗 Arquitetura do Sistema

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│    Frontend     │────│   TeacherHunt   │────│   Banco de      │
│  (React/Vue/    │    │      API        │    │     Dados       │
│   Angular)      │    │   (Django DRF)  │    │ (PostgreSQL)    │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                              │
                       ┌──────┴──────┐
                       │   Docker    │
                       │ Container   │
                       └─────────────┘
```

## ⚙️ Instalação e Configuração

### 📋 Pré-requisitos

- Python 3.12+
- Docker & Docker Compose
- Git

### 🚀 Configuração Rápida

1. **Clone o repositório**

```bash
git clone https://github.com/Kauanrodrigues01/projeto-teacherhunt.git
cd projeto-teacherhunt
```

2. **Configure o ambiente virtual**

```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate     # Windows
```

3. **Instale as dependências**

```bash
pip install -r requirements.txt
```

4. **Configure as variáveis de ambiente**

```bash
# Crie o arquivo .env na raiz do projeto
SECRET_KEY=sua-chave-secreta-super-segura
DEBUG=True
ALLOWED_HOSTS=*
DATABASE_URL=postgresql://user:password@localhost:5432/teacherhunt
ACCESS_TOKEN_LIFETIME_SECONDS=3600
REFRESH_TOKEN_LIFETIME_SECONDS=7200
```

5. **Execute as migrações**

```bash
python manage.py migrate
```

6. **Popule o banco (opcional)**

```bash
cd populate
python populate.py
```

7. **Inicie o servidor**

```bash
python manage.py runserver
```

## 📚 Documentação da API

A documentação completa está disponível via Swagger UI:

- **Swagger UI**: `http://localhost:8000/swagger/`
- **ReDoc**: `http://localhost:8000/redoc/`
- **JSON Schema**: `http://localhost:8000/swagger.json`

### 📌 Documentação Externa

- [Documentação Completa no GitHub](https://github.com/Kauanrodrigues01/documentacao-teacherhunt)

## 🔗 Endpoints Principais

### 🔐 Autenticação

```http
POST /api/auth/login              # Login do usuário
POST /api/auth/refresh            # Renovar token
POST /api/auth/logout             # Logout
POST /api/auth/password-reset-request  # Solicitar reset de senha
```

### 👨‍🏫 Professores

```http
GET    /api/professores/          # Listar professores
POST   /api/professores/          # Cadastrar professor
GET    /api/professores/{id}/     # Detalhes do professor
PUT    /api/professores/me/       # Atualizar perfil
GET    /api/professores/aulas/    # Aulas do professor
POST   /api/professores/aulas/aceitar/{id}/  # Aceitar aula
```

### 👨‍🎓 Alunos

```http
GET    /api/alunos/               # Listar alunos
POST   /api/alunos/               # Cadastrar aluno
GET    /api/alunos/me/            # Perfil do aluno
POST   /api/alunos/agendar-aulas/ # Agendar nova aula
GET    /api/alunos/professores-favoritos/  # Favoritos
```

### 📚 Matérias

```http
GET    /api/materias/             # Listar matérias
POST   /api/materias/             # Criar matéria (admin)
GET    /api/professores/materia/{id}/  # Professores por matéria
```

## 📁 Estrutura do Projeto

```
projeto-teacherhunt/
├── 📁 accounts/           # Autenticação e usuários
│   ├── models.py         # User, Teacher, Student, Rating
│   ├── serializers.py    # Serializers JWT customizados
│   ├── views.py          # Views de autenticação
│   └── urls.py           # URLs de auth
├── 📁 teachers/           # Funcionalidades dos professores
├── 📁 students/           # Funcionalidades dos alunos
├── 📁 classroom/          # Sistema de aulas
├── 📁 core/               # Configurações centrais
├── 📁 setup/              # Configurações Django
├── 📁 populate/           # Scripts de população do DB
├── 📁 docs/               # Documentação OpenAPI
├── 🐳 docker-compose.yml  # Configuração Docker
├── 🐳 Dockerfile          # Imagem Docker
├── 📋 requirements.txt    # Dependências Python
└── ⚙️ manage.py           # CLI do Django
```

## 🧪 Testes

Execute os testes com pytest:

```bash
# Rodar todos os testes
pytest

# Testes com coverage
pytest --cov=.

# Testes específicos
pytest accounts/tests/
pytest classroom/tests/
```

## 🐳 Docker

### Execução com Docker Compose

```bash
# Iniciar todos os serviços
docker-compose up --build

# Executar em background
docker-compose up -d

# Ver logs
docker-compose logs -f

# Parar serviços
docker-compose down
```

### Configuração do Container

O projeto inclui:

- 🐘 **PostgreSQL/MariaDB** - Banco de dados
- 🐍 **Python/Django** - API
- 🔧 **Volume persistente** - Dados do banco

## 🌟 Funcionalidades Especiais

### 🔍 Busca Inteligente

- Busca por nome, descrição e matérias
- Filtros por preço máximo e avaliação mínima
- Ordenação personalizada

### 📊 Sistema de Avaliações

- Ratings de 1 a 5 estrelas
- Comentários detalhados
- Cálculo automático de média

### 📅 Agendamento Inteligente

- Validação de conflitos de horário
- Cálculo automático de preços
- Status de aula (Pendente/Aceita/Cancelada)

### 🔐 Segurança

- Autenticação JWT com refresh tokens
- Permissões granulares por tipo de usuário
- Validação robusta de dados

## 🚀 Próximas Funcionalidades

- [ ] Sistema de notificações em tempo real
- [ ] Chat integrado entre professor e aluno
- [ ] Sistema de pagamentos
- [ ] Calendário interativo
- [ ] Relatórios e analytics

## 👨‍💻 Autor

**Kauan Rodrigues Lima**

- GitHub: [@Kauanrodrigues01](https://github.com/Kauanrodrigues01)
- LinkedIn: [Kauan Rodrigues](https://www.linkedin.com/in/kauan-rodrigues-lima/)
