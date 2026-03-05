# 🚀 Guia Completo: Publicar To-Do Pro no GitHub e Render

## Parte 1: Preparar o Projeto para Produção

### 1. Criar arquivo `.gitignore`
```gitignore
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
venv/
.venv/
ENV/
env/
*.egg-info/
dist/
build/

# Banco de dados
*.db
*.sqlite
*.sqlite3
instance/

# IDEs
.vscode/
.idea/
*.swp
*.swo
*~

# Environment
.env
.env.local

# OS
.DS_Store
Thumbs.db

# Logs
*.log
```

### 2. Criar arquivo `runtime.txt` (versão do Python)
```
python-3.11.0
```

### 3. Criar arquivo `Procfile` (para o Render)
```
web: python app/main.py
```

### 4. Atualizar o `app/main.py` para produção
Edite o final do arquivo `app/main.py`:

```python
if __name__ == '__main__':
    # Production mode
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
```

### 5. Criar arquivo `.env` para configurações
```
SECRET_KEY=sua-chave-secreta-aqui-mude-para-producao
FLASK_ENV=production
```

---

## Parte 2: Criar Repositório no GitHub

### 1. Criar conta no GitHub
Acesse: https://github.com

### 2. Criar novo repositório
1. Clique no botão **"+"** → **"New repository"**
2. Nome: `todo-pro` (ou outro nome)
3. Description: "Sistema completo de gerenciamento de tarefas com Python/Flask"
4. Marque **"Public"**
5. Clique **"Create repository"**

### 3. Comandos Git no seu computador

Abra o terminal na pasta do projeto:

```bash
# 1. Inicializar git (se não estiver inicializado)
git init

# 2. Adicionar todos os arquivos
git add .

# 3. Fazer o primeiro commit
git commit -m "Initial commit - To-Do Pro v1.0"

# 4. Renomear branch para main
git branch -M main

# 5. Adicionar o repositório remoto
git remote add origin https://github.com/SEU_USUARIO/todo-pro.git

# 6. Enviar para o GitHub
git push -u origin main
```

**Nota:** Substitua `SEU_USUARIO` pelo seu username do GitHub.

---

## Parte 3: Configurar o Render

### 1. Criar conta no Render
Acesse: https://render.com
- Clique em **"Get Started"**
- Conecte com GitHub

### 2. Criar Web Service

1. No dashboard do Render, clique em **"New +"** → **"Web Service"**

2. Configure:
   - **Name**: `todo-pro` (ou outro nome)
   - **Region**: São Paulo (ou o mais próximo)
   - **Branch**: `main`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `python app/main.py`

3. Clique em **"Create Web Service"**

### 3. Configurar Variáveis de Ambiente

Nas configurações do seu Web Service no Render:

1. Vá em **"Environment"**
2. Adicione as variáveis:
   - `SECRET_KEY` = Uma chave secreta forte (use: `python -c "import secrets; print(secrets.token_hex(20))"` para gerar)
   - `FLASK_ENV` = `production`

### 4. Esperar o Deploy

1. O Render vai fazer o build automaticamente
2. Você pode acompanhar em **"Logs"**
3. Quando aparecer **"Healthy"**, seu site está no ar!

### 5. Acessar o Site

O URL será algo como: `https://todo-pro.onrender.com`

---

## ⚠️ Problema com Banco de Dados no Render

O SQLite não funciona bem em serviços de cloud porque é apenas para desenvolvimento local. Para produção, você tem duas opções:

### Opção A: Usar PostgreSQL (Recomendado)

1. No Render, crie um PostgreSQL:
   - **New +** → **PostgreSQL**
   - Nome: `todo-pro-db`
   - Salve a **Internal Database URL**

2. Altere o `app/main.py`:

```python
import os

# Use PostgreSQL se disponível, senão SQLite
DATABASE_URL = os.environ.get('DATABASE_URL')
if DATABASE_URL and DATABASE_URL.startswith('postgres://'):
    DATABASE_URL = DATABASE_URL.replace('postgres://', 'postgresql://', 1)

app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL or f'sqlite:///{os.path.join(BASE_DIR, "instance", "todolist.db")}'
```

3. Adicione no `requirements.txt`:
```
psycopg2-binary==2.9.9
```

4. Faça o commit e push:
```bash
git add .
git commit -m "Add PostgreSQL support"
git push origin main
```

### Opção B: Usar SQLite com Disco (Solução Temporária)

O Render fornece um disco ephemeral. Para usar:

1. No `Procfile`:
```
web: python app/main.py
```

2. O banco será recriado a cada deploy (perde dados). **Não recomendado para produção real.**

---

## 📋 Comandos Úteis

### Atualizar o Deploy após mudanças
```bash
git add .
git commit -m "Descrição da mudança"
git push origin main
```

### Ver logs no Render
- No dashboard do Render → seu serviço → **"Logs"**

### Variáveis de Ambiente importantes
```bash
# Gerar chave secreta
python -c "import secrets; print(secrets.token_hex(20))"
```

---

## ✅ Checklist Final

- [ ] Arquivo `.gitignore` criado
- [ ] Arquivo `requirements.txt` atualizado
- [ ] Arquivo `runtime.txt` criado
- [ ] Arquivo `Procfile` criado
- [ ] Código atualizado para produção
- [ ] Repositório criado no GitHub
- [ ] Código enviado para o GitHub
- [ ] Conta criada no Render
- [ ] Web Service criado
- [ ] Variáveis de ambiente configuradas
- [ ] Deploy concluído
- [ ] Site funcionando!

---

## 🔧 Solução de Problemas

### "Build failed"
- Verifique os logs no Render
- Certifique-se que o `requirements.txt` está correto

### "Application failed to start"
- Verifique a variável `SECRET_KEY`
- Verifique se a porta está configurada como `PORT`

### Banco de dados não conecta
- Verifique a URL do PostgreSQL
- Certifique-se que o `psycopg2-binary` está no requirements.txt

---

**Seu site estará disponível em: `https://seu-projeto.onrender.com`**
