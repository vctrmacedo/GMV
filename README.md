# 🚗 Sistema de Gestão de Frota (GMV Fleet Management)

Sistema completo de gestão de frota desenvolvido com FastAPI, oferecendo controle total sobre motoristas, veículos e agendamentos.

## ✨ Funcionalidades

### 🔐 Autenticação e Usuários
- **Sistema JWT** com tokens seguros
- **Login flexível** (email ou nome de usuário)
- **Controle de acesso** baseado em autenticação
- **Senhas criptografadas** com bcrypt

### 👨‍💼 Gestão de Motoristas
- **Cadastro completo** com dados pessoais
- **Validação de CNH** e categoria
- **Controle de status** ativo/inativo
- **Histórico de viagens**

### 🚙 Gestão de Veículos
- **Controle de frota** com placa e modelo
- **Acompanhamento** de quilometragem
- **Status operacional** ativo/inativo
- **Histórico de uso**

### 📅 Sistema de Agendamentos
- **Reserva de veículos** para motoristas
- **Controle de datas** de saída e retorno
- **Rastreamento** de origem e destino
- **Monitoramento** de consumo de combustível
- **Cálculo de custos** por viagem

## 🛠️ Tecnologias

- **Backend**: FastAPI (Python 3.13+)
- **Banco de Dados**: SQLite (SQLAlchemy ORM)
- **Autenticação**: JWT (JSON Web Tokens)
- **Validação**: Pydantic
- **Documentação**: Swagger UI / ReDoc
- **Segurança**: bcrypt, python-jose

## 🚀 Instalação

### 1. Clone o repositório
```bash
git clone https://github.com/seu-usuario/gmv-backend.git
cd gmv-backend
```

### 2. Crie e ative o ambiente virtual
```bash
python -m venv venv
venv\Scripts\activate  # Windows
# ou
source venv/bin/activate  # Linux/Mac
```

### 3. Instale as dependências
```bash
pip install -r requirements.txt
```

### 4. Execute o servidor
```bash
python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

## 📚 Documentação da API

### Acesse a documentação interativa:
- **Swagger UI**: http://127.0.0.1:8000/docs
- **ReDoc**: http://127.0.0.1:8000/redoc

## 🔑 Primeiro Acesso

### 1. Crie o primeiro usuário
```bash
POST /auth/register
{
  "name": "Administrador",
  "email": "admin@empresa.com",
  "password": "SenhaSegura123!"
}
```

### 2. Faça login
```bash
POST /auth/login
{
  "username_or_email": "admin@empresa.com",
  "password": "SenhaSegura123!"
}
```

### 3. Use o token retornado
```bash
Authorization: Bearer <seu_token_aqui>
```

## 📊 Endpoints Disponíveis

### Autenticação
- `POST /auth/login` - Login de usuário
- `POST /auth/register` - Registro inicial

### Usuários
- `GET /users/` - Listar usuários
- `POST /users/` - Criar usuário
- `PUT /users/{id}` - Atualizar usuário
- `DELETE /users/{id}` - Deletar usuário

### Motoristas
- `GET /drivers/` - Listar motoristas
- `POST /drivers/` - Criar motorista
- `PUT /drivers/{id}` - Atualizar motorista
- `DELETE /drivers/{id}` - Deletar motorista

### Veículos
- `GET /vehicles/` - Listar veículos
- `POST /vehicles/` - Criar veículo
- `PUT /vehicles/{id}` - Atualizar veículo
- `DELETE /vehicles/{id}` - Deletar veículo

### Agendamentos
- `GET /schedules/` - Listar agendamentos
- `POST /schedules/` - Criar agendamento
- `PUT /schedules/{id}` - Atualizar agendamento
- `DELETE /schedules/{id}` - Deletar agendamento

## 🏗️ Estrutura do Projeto

```
GMV-backend/
├── app/
│   ├── __init__.py
│   ├── main.py              # Aplicação principal
│   ├── config.py            # Configurações
│   ├── database.py          # Conexão com banco
│   ├── core/
│   │   ├── dependencies.py  # Dependências de autenticação
│   │   └── security.py      # Funções de segurança
│   ├── models/              # Modelos do banco
│   ├── routes/              # Endpoints da API
│   └── schemas/             # Schemas de validação
├── requirements.txt          # Dependências Python
├── .gitignore               # Arquivos ignorados pelo Git
└── README.md                # Este arquivo
```

## 🔒 Segurança

- **Autenticação JWT** em todas as rotas protegidas
- **Senhas criptografadas** com bcrypt
- **Validação de dados** com Pydantic
- **Controle de acesso** por usuário autenticado

## 🎯 Próximos Passos

- [ ] **Frontend Web** (Vue.js/React)
- [ ] **App Mobile** para motoristas
- [ ] **Sistema de notificações**
- [ ] **Relatórios avançados**
- [ ] **Dashboard com gráficos**
- [ ] **Integração com APIs externas**


