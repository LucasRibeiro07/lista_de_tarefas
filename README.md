# 🚀 To-Do Pro - Sistema Completo de Gerenciamento de Tarefas

## Tutorial Passo a Passo para Criar Seu Site de Lista de Tarefas com Python

Este é um tutorial completo para criar um sistema de gerenciamento de tarefas (To-Do List) completo com Python usando Flask. O projeto inclui todas as funcionalidades de CRUD que você pediu.

---

## 📋 Índice

1. [Pré-requisitos](#pré-requisitos)
2. [Estrutura do Projeto](#estrutura-do-projeto)
3. [Instalação](#instalação)
4. [Executando o Projeto](#executando-o-projeto)
5. [Funcionalidades](#funcionalidades)
6. [Paleta de Cores](#paleta-de-cores)
7. [Tecnologias Usadas](#tecnologias-usadas)

---

## ✅ Pré-requisitos

Antes de começar, você precisa ter instalado no seu computador:

### 1. **Python 3.8 ou superior**
- Download: https://www.python.org/downloads/
- **Importante**: Marque a opção "Add Python to PATH" durante a instalação

### 2. **Git (opcional)**
- Download: https://git-scm.com/
- Usaremos apenas para clonar, se desejado

---

## 📁 Estrutura do Projeto

O projeto está organizado da seguinte forma:

```
todo_project/
├── app/
│   └── main.py              # Código principal (Flask)
├── static/
│   └── style.css            # Estilos CSS moderno
├── templates/
│   ├── base.html            # Template base
│   ├── login.html           # Página de login
│   ├── cadastro.html        # Página de cadastro
│   ├── dashboard.html       # Dashboard principal
│   ├── tarefas.html         # Lista de tarefas
│   ├── tarefa_nova.html     # Criar tarefa
│   ├── tarefa_editar.html  # Editar tarefa
│   ├── pastas.html         # Lista de pastas
│   ├── pasta_nova.html     # Criar pasta
│   ├── pasta_editar.html   # Editar pasta
│   └── settings.html       # Configurações do usuário
├── requirements.txt        # Dependências Python
└── README.md               # Este arquivo
```

---

## 🔧 Instalação

### Passo 1: Criar o Ambiente Virtual

Abra o terminal (Prompt de Comando ou PowerShell) e execute:

```bash
# Navegue até a pasta onde quer criar o projeto
cd "c:\Users\Lucas Ribeiro\Documents\PROJETOS"

# Crie uma pasta para o projeto
mkdir todo_project
cd todo_project

# Crie o ambiente virtual
python -m venv venv
```

### Passo 2: Ativar o Ambiente Virtual

```bash
# No Windows (PowerShell)
.\venv\Scripts\Activate

# No Windows (CMD)
venv\Scripts\activate.bat

# No Linux/Mac
source venv/bin/activate
```

Você verá `(venv)` no início da linha do terminal.

### Passo 3: Instalar as Dependências

```bash
pip install Flask==3.0.0 Flask-SQLAlchemy==3.1.1 Flask-Login==0.6.3 Werkzeug==3.0.1 python-dotenv==1.0.0
```

Ou simplemente:

```bash
pip install -r requirements.txt
```

### Passo 4: Preparar o Banco de Dados

O banco SQLite será primeira vez que você criado automaticamente na executar o projeto.

---

## ▶️ Executando o Projeto

### Método 1: Execução Direta

```bash
cd todo_project
python app/main.py
```

### Método 2: Com Flask

```bash
# Defina a variável de ambiente (opcional)
set FLASK_APP=app/main.py
set FLASK_ENV=development

# Execute
python -m flask run
```

### Método 3: No VS Code

1. Abra a pasta `todo_project` no VS Code
2. Pressione `F5` ou vá em "Run > Start Debugging"
3. Escolha "Python" e "Flask"

---

## 🌐 Acessando o Site

Após executar, abra seu navegador e vá para:

```
http://localhost:5000
```

---

## ✨ Funcionalidades Implementadas

### 1. **Sistema de Autenticação**
- ✅ Cadastro de múltiplos usuários
- ✅ Login seguro com senha hasheada
- ✅ Logout
- ✅ Cada usuário tem suas próprias tarefas (isoladas)

### 2. **CRUD Completo de Tarefas**
- ✅ **Criar** - Adicionar novas tarefas com título, descrição, prioridade e deadline
- ✅ **Ler** - Visualizar lista de tarefas com filtros
- ✅ **Atualizar** - Editar qualquer tarefa existente
- ✅ **Excluir** - Remover tarefas

### 3. **Status de Tarefas**
- ✅ Pendente
- ✅ Em Andamento
- ✅ Concluída
- ✅ Marcar como concluída com um clique
- ✅ Reativar tarefas concluídas

### 4. **Sistema de Pastas**
- ✅ Criar pastas (categorias)
- ✅ Criar subpastas (aninhamento)
- ✅ Associar tarefas a pastas
- ✅ Personalizar com ícones e cores
- ✅ Mover tarefas entre pastas

### 5. **Deadline e Prazos**
- ✅ Definir data limite para tarefas
- ✅ Exibir tempo restante
- ✅ Alertas de tarefas atrasadas
- ✅ Dashboard com tarefas próximas do prazo

### 6. **Dashboard Informativo**
- ✅ Total de tarefas
- ✅ Tarefas pendentes
- ✅ Tarefas em andamento
- ✅ Tarefas concluídas
- ✅ Tarefas próximas do prazo
- ✅ Tarefas atrasadas

### 7. **Configurações do Usuário**
- ✅ Alterar nome completo
- ✅ Alterar e-mail
- ✅ Alterar senha
- ✅ Cor do avatar
- ✅ Modo escuro (tema)
- ✅ Idioma
- ✅ Notificações por e-mail

---

## 🎨 Paleta de Cores

O design foi criado com uma paleta de cores moderna e profissional:

### Cores Principais
| Cor | Hex | Uso |
|-----|-----|-----|
| Indigo | `#6366f1` | Primária (botões, links) |
| Purple | `#8b5cf6` | Secundária (gradientes) |
| Cyan | `#06b6d4` | Accent (destaques) |
| Slate Dark | `#1e293b` | Escuro (textos) |
| Slate Light | `#f8fafc` | Fundo claro |

### Cores Semânticas
| Cor | Hex | Uso |
|-----|-----|-----|
| Emerald | `#10b981` | Sucesso (tarefas concluídas) |
| Amber | `#f59e0b` | Aviso (pendente, prazo) |
| Red | `#ef4444` | Erro (atrasada, excluir) |

### Cores para Prioridade
| Prioridade | Cor | Badge |
|------------|-----|-------|
| Baixa | `#10b981` | Verde |
| Média | `#6366f1` | Indigo |
| Alta | `#f59e0b` | Amarelo |
| Urgente | `#ef4444` | Vermelho |

---

## 🎯 Como Testar as Funcionalidades

### 1. Criar Conta
1. Acesse `http://localhost:5000`
2. Clique em "Cadastre-se"
3. Preencha os dados
4. Você será redirecionado para o Dashboard

### 2. Criar uma Pasta
1. No menu, clique em "Pastas"
2. Clique em "Nova Pasta"
3. Dê um nome (ex: "Trabalho")
4. Escolha um ícone e cor
5. Clique em "Criar Pasta"

### 3. Criar uma Tarefa
1. Clique em "Nova Tarefa" ou vá em "Tarefas"
2. Preencha o título
3. (Opcional) Adicione descrição
4. Escolha a pasta
5. Defina a prioridade
6. Defina uma data limite (deadline)
7. Clique em "Criar Tarefa"

### 4. Gerenciar Tarefas
- **Concluir**: Clique no círculo ao lado da tarefa
- **Editar**: Clique nos três pontinhos > Editar
- **Excluir**: Clique nos três pontinhos > Excluir
- **Filtrar**: Use os filtros na página de tarefas

### 5. Configurações
1. Clique no seu nome no menu superior
2. Escolha "Configurações"
3. Altere o que desej4. Clique em "Salvar Configurações"

### 6. Criar Outro Usuário
1. Faça logout
2. Clique em "Cadastre-se"
3. Crie uma nova conta
4. Observe que você não vê as tarefas do outro usuário!

---

## 🛠️ Tecnologias Usadas

### Backend
- **Python 3** - Linguagem de programação
- **Flask** - Framework web
- **SQLAlchemy** - ORM para banco de dados
- **Werkzeug** - Segurança (hashing de senhas)
- **Flask-Login** - Gerenciamento de sessões

### Frontend
- **HTML5** - Estrutura das páginas
- **CSS3** - Estilização moderna
- **Bootstrap 5** - Framework CSS (componentes)
- **Font Awesome** - Ícones
- **Google Fonts (Inter)** - Tipografia

### Banco de Dados
- **SQLite** - Banco de dados leve (arquivo local)

---

## 📝 Comandos Úteis

```bash
# Ativar ambiente virtual
.\venv\Scripts\Activate

# Instalar dependências
pip install -r requirements.txt

# Executar projeto
python app/main.py

# Parar servidor
# Pressione Ctrl + C no terminal
```

---

## 🔒 Segurança Implementada

1. **Senhas hasheadas** - Senhas nunca são armazenadas em texto plain
2. **Proteção de rotas** - Usuários não autenticados são redirecionados
3. **Isolamento de dados** - Cada usuário só vê suas próprias tarefas
4. **CSRF Protection** - Proteção contra ataques Cross-Site Request Forgery
5. **Validação de dados** - Entradas validadas antes de salvar

---

## 📱 Design Responsivo

O site funciona em:
- ✅ Computadores desktop
- ✅ Tablets
- ✅ Smartphones

---

## 🚀 Próximos Passos (Opcional)

Se você quiser expandir o projeto:

1. **API REST** - Criar endpoints JSON
2. **Lembretes por e-mail** - Integrar com SMTP
3. **Upload de arquivos** - Anexar arquivos às tarefas
4. **Tarefas compartilhadas** - Colaboração entre usuários
5. **Estatísticas avançadas** - Gráficos e relatórios
6. **Aplicativo mobile** - React Native ou Flutter

---

## 📄 Licença

Este projeto é de uso livre para aprendizado e desenvolvimento pessoal.

---

## ❓ Problemas Comuns

### "Porta 5000 já está em uso"
```bash
# Encontre e mate o processo
netstat -ano | findstr :5000
taskkill /PID <NUMERO> /F
```

### "Módulo não encontrado"
```bash
# Reinstale as dependências
pip install -r requirements.txt
```

### "Erro de banco de dados"
```bash
# Delete o arquivo e deixe criar novamente
# O arquivo está em: app/todolist.db
```

---

**Desenvolvido com ❤️ usando Python e Flask**

Este projeto demonstra suas habilidades com:
- ✅ CRUD completo
- ✅ Autenticação e autorização
- ✅ Banco de dados relacionais
- ✅ Design moderno e responsivo
- ✅ Boas práticas de segurança
- ✅ Organização de código
