# 🚀 To-Do Pro - Tutorial Completo para Criar seu Site de Lista de Tarefas com Python

## 📋 Índice do Tutorial

1. [Visão Geral do Projeto](#1-visão-geral-do-projeto)
2. [Pré-requisitos](#2-pré-requisitos)
3. [Estrutura do Projeto](#3-estrutura-do-projeto)
4. [Instalação e Configuração](#4-instalação-e-configuração)
5. [O Código Completo](#5-o-código-completo)
6. [Executando o Projeto](#6-executando-o-projeto)
7. [Funcionalidades Implementadas](#7-funcionalidades-implementadas)
8. [Personalização (Settings)](#8-personalização-settings)
9. [Implantação (Deploy)](#9-implantação-deploy)
10. [Demonstrando suas Habilidades](#10-demonstrando-suas-habilidades)

---

## 1. VISÃO GERAL DO PROJETO

Este é um sistema completo de gerenciamento de tarefas (To-Do List) desenvolvido com Python e Flask. O projeto demonstra todas as habilidades de **CRUD** (Create, Read, Update, Delete) e muito mais:

### ✅ Funcionalidades Principais:
- **Sistema de múltiplos usuários** - Cada usuário tem suas próprias tarefas isoladas
- **CRUD completo de tarefas** - Criar, ler, atualizar e excluir tarefas
- **Sistema de pastas/categorias** - Organize tarefas em pastas (com subpastas)
- **Deadline/Prazos** - Defina data limite para cada tarefa
- **Dashboard informativo** - Veja tarefas pendentes, próximas do prazo e atrasadas
- **Modo escuro (Dark Mode)** - Tema escuro automático
- **Configurações personalizadas** - Cor do tema, avatar emoji, personalização
- **Design moderno e minimalista** - Interface responsiva e profesional

### 🎨 Paleta de Cores (Pesquisa Realizada)

Após pesquisa sobre as melhores cores para interfaces modernas, usamos:

| Tipo | Cor | Hex | Uso |
|------|-----|-----|-----|
| Primária | Indigo | `#6366f1` | Botões principais, links |
| Secundária | Purple | `#8b5cf6` | Gradientes, detalhes |
| Acento | Cyan | `#06b6d4` | Destaques, ícones |
| Sucesso | Emerald | `#10b981` | Tarefas concluídas |
| Aviso | Amber | `#f59e0b` | Prazos, pendências |
| Perigo | Red | `#ef4444` | Excluir, atrasadas |
| Fundo Escuro | Slate | `#1e293b` | Modo escuro |
| Fundo Claro | Slate Light | `#f8fafc` | Modo claro |

---

## 2. PRÉ-REQUISITOS

### 2.1 Python 3.8 ou Superior

```bash
# Verificar se o Python está instalado
python --version

# Se não tiver, baixe em: https://www.python.org/downloads/
# IMPORTANTE: Marque "Add Python to PATH" durante a instalação
```

### 2.2 Git (Opcional mas Recomendado)

```bash
# Verificar se o Git está instalado
git --version

# Baixar em: https://git-scm.com/
```

---

## 3. ESTRUTURA DO PROJETO

```
todo_project/
├── app/
│   └── main.py              # Aplicação principal (Flask + SQLAlchemy)
├── static/
│   └── style.css            # Estilos CSS moderno
├── templates/
│   ├── base.html            # Template base com navbar e footer
│   ├── login.html           # Página de login
│   ├── cadastro.html        # Página de cadastro de usuários
│   ├── dashboard.html      # Dashboard com estatísticas
│   ├── tarefas.html         # Lista de todas as tarefas
│   ├── tarefa_nova.html     # Formulário para criar tarefa
│   ├── tarefa_editar.html   # Formulário para editar tarefa
│   ├── pastas.html          # Lista de pastas/categorias
│   ├── pasta_nova.html     # Formulário para criar pasta
│   ├── pasta_editar.html   # Formulário para editar pasta
│   └── settings.html        # Configurações do usuário
├── instance/
│   └── todolist.db          # Banco de dados SQLite (criado automaticamente)
├── requirements.txt        # Dependências do Python
├── runtime.txt              # Versão do Python para deploy
├── Procfile                 # Comando para o Render
├── .gitignore               # Arquivos ignorados pelo Git
├── README.md                # Documentação
├── DEPLOY.md                # Guia de implantação
└── TUTORIAL_COMPLETO.md     # Este arquivo
```

---

## 4. INSTALAÇÃO E CONFIGURAÇÃO

### Passo 1: Criar a Pasta do Projeto

```bash
# Abra o terminal/prompt de comando
# Navegue até onde quer criar o projeto
cd "C:\Users\Lucas Ribeiro\Documents\PROJETOS"

# Crie a pasta do projeto
mkdir todo_project
cd todo_project
```

### Passo 2: Criar o Ambiente Virtual

```bash
# Criar ambiente virtual
python -m venv venv

# Ativar no Windows (PowerShell)
.\venv\Scripts\Activate

# Ativar no Windows (CMD)
venv\Scripts\activate.bat

# Ativar no Linux/Mac
source venv/bin/activate
```

Você verá `(venv)` no início da linha do terminal.

### Passo 3: Instalar as Dependências

```bash
# Instalar todas as dependências de uma vez
pip install Flask==3.0.0 Flask-SQLAlchemy==3.1.1 Flask-Login==0.6.3 Werkzeug==3.0.1
```

**Ou use o arquivo requirements.txt:**

```bash
# Se você tiver o arquivo requirements.txt
pip install -r requirements.txt
```

### Passo 4: Criar a Estrutura de Pastas

```bash
# Criar pastas necessárias
mkdir app
mkdir static
mkdir templates
mkdir instance
```

---

## 5. O CÓDIGO COMPLETO

### 5.1 requirements.txt

```
Flask==3.0.0
Flask-SQLAlchemy==3.1.1
Flask-Login==0.6.3
Werkzeug==3.0.1
```

### 5.2 app/main.py (Código Completo)

Este é o arquivo principal que contém toda a lógica da aplicação:

```python
"""
To-Do List Completo com Python/Flask
Sistema de gerenciamento de tarefas com múltiplos usuários, pastas e deadlines
"""

from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
import os
from functools import wraps

# ============== CONFIGURAÇÃO DA APLICAÇÃO ==============
import os

# Obter o diretório base do projeto (pasta pai da pasta app)
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

app = Flask(__name__,
            template_folder=os.path.join(BASE_DIR, 'templates'),
            static_folder=os.path.join(BASE_DIR, 'static'))
app.config['SECRET_KEY'] = 'sua-chave-secreta-aqui-mude-para-producao'
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{os.path.join(BASE_DIR, "instance", "todolist.db")}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Configurações de tema (podem ser alteradas no settings)
app.config['THEME_PRIMARY'] = '#6366f1'  # Indigo
app.config['THEME_SECONDARY'] = '#8b5cf6'  # Purple
app.config['THEME_ACCENT'] = '#06b6d4'  # Cyan
app.config['THEME_DARK'] = '#1e293b'  # Slate dark
app.config['THEME_LIGHT'] = '#f8fafc'  # Slate light
app.config['THEME_SUCCESS'] = '#10b981'  # Emerald
app.config['THEME_WARNING'] = '#f59e0b'  # Amber
app.config['THEME_DANGER'] = '#ef4444'  # Red

# Inicializar extensões
db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message = 'Por favor, faça login para continuar.'
login_manager.login_message_category = 'info'

# ============== MODELOS DO BANCO DE DADOS ==============

# Modelo de Usuário
class Usuario(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    senha_hash = db.Column(db.String(200), nullable=False)
    nome_completo = db.Column(db.String(100))
    avatar_emoji = db.Column(db.String(10), default='👤')
    avatar_cor = db.Column(db.String(20), default='#6366f1')
    tema_cor_principal = db.Column(db.String(20), default='#6366f1')
    modo_escuro = db.Column(db.Boolean, default=False)
    data_criacao = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relacionamentos
    pastas = db.relationship('Pasta', backref='dono', lazy=True, cascade='all, delete-orphan')
    tarefas = db.relationship('Tarefa', backref='dono', lazy=True, cascade='all, delete-orphan')
    
    def set_senha(self, senha):
        self.senha_hash = generate_password_hash(senha)
    
    def verificar_senha(self, senha):
        return check_password_hash(self.senha_hash, senha)

# Modelo de Pasta (Categoria)
class Pasta(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    descricao = db.Column(db.Text)
    icone = db.Column(db.String(50), default='📁')
    cor = db.Column(db.String(20), default='#6366f1')
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)
    pasta_pai_id = db.Column(db.Integer, db.ForeignKey('pasta.id'), nullable=True)
    data_criacao = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relacionamento para subpastas
    subpastas = db.relationship('Pasta', backref=db.backref('pasta_pai', remote_side=[id]), lazy=True)
    tarefas = db.relationship('Tarefa', backref='pasta', lazy=True, cascade='all, delete-orphan')

# Modelo de Tarefa
class Tarefa(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(200), nullable=False)
    descricao = db.Column(db.Text)
    status = db.Column(db.String(20), default='pendente')  # pendente, em_andamento, concluida
    prioridade = db.Column(db.String(20), default='media')  # baixa, media, alta, urgente
    pasta_id = db.Column(db.Integer, db.ForeignKey('pasta.id'), nullable=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)
    deadline = db.Column(db.DateTime, nullable=True)
    data_criacao = db.Column(db.DateTime, default=datetime.utcnow)
    data_conclusao = db.Column(db.DateTime, nullable=True)
    
    def esta_atrasada(self):
        if self.deadline and self.status != 'concluida':
            return datetime.utcnow() > self.deadline
        return False
    
    def tempo_restante(self):
        if self.deadline:
            delta = self.deadline - datetime.utcnow()
            if delta.total_seconds() < 0:
                return "Atrasada"
            dias = delta.days
            horas = delta.seconds // 3600
            if dias > 0:
                return f"{dias}d {horas}h"
            return f"{horas}h"
        return "Sem prazo"

@login_manager.user_loader
def load_user(user_id):
    return Usuario.query.get(int(user_id))

# ============== ROTAS DA APLICAÇÃO ==============

# Página inicial - Redireciona para login ou dashboard
@app.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

# Login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    
    if request.method == 'POST':
        username = request.form.get('username')
        senha = request.form.get('senha')
        
        usuario = Usuario.query.filter_by(username=username).first()
        
        if usuario and usuario.verificar_senha(senha):
            login_user(usuario)
            flash(f'Bem-vindo de volta, {usuario.username}!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Login inválido. Verifique seu usuário e senha.', 'danger')
    
    return render_template('login.html')

# Cadastro de novo usuário
@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        senha = request.form.get('senha')
        nome_completo = request.form.get('nome_completo')
        
        # Verificar se usuário ou email já existe
        if Usuario.query.filter_by(username=username).first():
            flash('Nome de usuário já existe.', 'danger')
            return render_template('cadastro.html')
        
        if Usuario.query.filter_by(email=email).first():
            flash('E-mail já cadastrado.', 'danger')
            return render_template('cadastro.html')
        
        # Criar novo usuário
        novo_usuario = Usuario(
            username=username,
            email=email,
            nome_completo=nome_completo
        )
        novo_usuario.set_senha(senha)
        
        db.session.add(novo_usuario)
        db.session.commit()
        
        flash('Conta criada com sucesso! Faça login para continuar.', 'success')
        return redirect(url_for('login'))
    
    return render_template('cadastro.html')

# Logout
@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Você foi desconectado.', 'info')
    return redirect(url_for('login'))

# Dashboard - Página principal após login
@app.route('/dashboard')
@login_required
def dashboard():
    # Estatísticas
    total_tarefas = Tarefa.query.filter_by(usuario_id=current_user.id).count()
    tarefas_pendentes = Tarefa.query.filter_by(usuario_id=current_user.id, status='pendente').count()
    tarefas_andamento = Tarefa.query.filter_by(usuario_id=current_user.id, status='em_andamento').count()
    tarefas_concluidas = Tarefa.query.filter_by(usuario_id=current_user.id, status='concluida').count()
    
    # Tarefas próximas do prazo (próximos 3 dias)
    prazo_proximo = datetime.utcnow() + timedelta(days=3)
    tarefas_proximas = Tarefa.query.filter(
        Tarefa.usuario_id == current_user.id,
        Tarefa.status != 'concluida',
        Tarefa.deadline <= prazo_proximo,
        Tarefa.deadline >= datetime.utcnow()
    ).order_by(Tarefa.deadline).limit(5).all()
    
    # Tarefas atrasadas
    tarefas_atrasadas = Tarefa.query.filter(
        Tarefa.usuario_id == current_user.id,
        Tarefa.status != 'concluida',
        Tarefa.deadline < datetime.utcnow()
    ).order_by(Tarefa.deadline).all()
    
    # Próximas tarefas a fazer
    proximas_tarefas = Tarefa.query.filter(
        Tarefa.usuario_id == current_user.id,
        Tarefa.status != 'concluida'
    ).order_by(
        Tarefa.prioridade.desc(),
        Tarefa.deadline.asc().nullslast()
    ).limit(5).all()
    
    return render_template('dashboard.html',
                           total=total_tarefas,
                           pendentes=tarefas_pendentes,
                           andamento=tarefas_andamento,
                           concluidas=tarefas_concluidas,
                           proximas=pastas_proximas,
                           atrasadas=tarefas_atrasadas,
                           tarefas_proximas=pastas_proximas)

# Lista de tarefas
@app.route('/tarefas')
@app.route('/tarefas/<int:pasta_id>')
@login_required
def tarefas(pasta_id=None):
    status_filter = request.args.get('status')
    prioridade_filter = request.args.get('prioridade')
    
    query = Tarefa.query.filter_by(usuario_id=current_user.id)
    
    if pasta_id:
        query = query.filter_by(pasta_id=pasta_id)
    
    if status_filter:
        query = query.filter_by(status=status_filter)
    
    if prioridade_filter:
        query = query.filter_by(prioridade=prioridade_filter)
    
    todas_tarefas = query.order_by(Tarefa.data_criacao.desc()).all()
    pastas_usuario = Pasta.query.filter_by(usuario_id=current_user.id).all()
    
    return render_template('tarefas.html', tarefas=todas_tarefas, pastas=pastas_usuario, pasta_selecionada=pasta_id)

# Nova tarefa
@app.route('/tarefa/nova', methods=['GET', 'POST'])
@login_required
def nova_tarefa():
    pastas_usuario = Pasta.query.filter_by(usuario_id=current_user.id).all()
    
    if request.method == 'POST':
        titulo = request.form.get('titulo')
        descricao = request.form.get('descricao')
        pasta_id = request.form.get('pasta_id')
        prioridade = request.form.get('prioridade')
        deadline_str = request.form.get('deadline')
        
        deadline = None
        if deadline_str:
            try:
                deadline = datetime.strptime(deadline_str, '%Y-%m-%dT%H:%M')
            except:
                flash('Formato de data inválido.', 'warning')
        
        nova_tarefa = Tarefa(
            titulo=titulo,
            descricao=descricao,
            pasta_id=pasta_id if pasta_id else None,
            prioridade=prioridade,
            deadline=deadline,
            usuario_id=current_user.id
        )
        
        db.session.add(nova_tarefa)
        db.session.commit()
        
        flash('Tarefa criada com sucesso!', 'success')
        return redirect(url_for('tarefas'))
    
    return render_template('tarefa_nova.html', pastas=pastas_usuario)

# Editar tarefa
@app.route('/tarefa/editar/<int:tarefa_id>', methods=['GET', 'POST'])
@login_required
def editar_tarefa(tarefa_id):
    tarefa = Tarefa.query.get_or_404(tarefa_id)
    
    if tarefa.usuario_id != current_user.id:
        flash('Você não tem permissão para editar esta tarefa.', 'danger')
        return redirect(url_for('tarefas'))
    
    pastas_usuario = Pasta.query.filter_by(usuario_id=current_user.id).all()
    
    if request.method == 'POST':
        tarefa.titulo = request.form.get('titulo')
        tarefa.descricao = request.form.get('descricao')
        tarefa.pasta_id = request.form.get('pasta_id') or None
        tarefa.prioridade = request.form.get('prioridade')
        tarefa.status = request.form.get('status')
        
        deadline_str = request.form.get('deadline')
        if deadline_str:
            tarefa.deadline = datetime.strptime(deadline_str, '%Y-%m-%dT%H:%M')
        else:
            tarefa.deadline = None
        
        if tarefa.status == 'concluida' and not tarefa.data_conclusao:
            tarefa.data_conclusao = datetime.utcnow()
        elif tarefa.status != 'concluida':
            tarefa.data_conclusao = None
        
        db.session.commit()
        flash('Tarefa atualizada com sucesso!', 'success')
        return redirect(url_for('tarefas'))
    
    return render_template('tarefa_editar.html', tarefa=tarefa, pastas=pastas_usuario)

# Excluir tarefa
@app.route('/tarefa/excluir/<int:tarefa_id>')
@login_required
def excluir_tarefa(tarefa_id):
    tarefa = Tarefa.query.get_or_404(tarefa_id)
    
    if tarefa.usuario_id != current_user.id:
        flash('Você não tem permissão para excluir esta tarefa.', 'danger')
        return redirect(url_for('tarefas'))
    
    db.session.delete(tarefa)
    db.session.commit()
    flash('Tarefa excluída!', 'success')
    return redirect(url_for('tarefas'))

# Alternar status da tarefa (concluir/desconcluir)
@app.route('/tarefa/toggle/<int:tarefa_id>')
@login_required
def toggle_tarefa(tarefa_id):
    tarefa = Tarefa.query.get_or_404(tarefa_id)
    
    if tarefa.usuario_id != current_user.id:
        flash('Você não tem permissão para modificar esta tarefa.', 'danger')
        return redirect(url_for('tarefas'))
    
    if tarefa.status == 'concluida':
        tarefa.status = 'pendente'
        tarefa.data_conclusao = None
    else:
        tarefa.status = 'concluida'
        tarefa.data_conclusao = datetime.utcnow()
    
    db.session.commit()
    return redirect(request.referrer or url_for('tarefas'))

# Lista de pastas
@app.route('/pastas')
@login_required
def pastas():
    # Pegar apenas pastas raiz (sem pai)
    pastas_raiz = Pasta.query.filter_by(usuario_id=current_user.id, pasta_pai_id=None).all()
    return render_template('pastas.html', pastas=pastas_raiz)

# Nova pasta
@app.route('/pasta/nova', methods=['GET', 'POST'])
@app.route('/pasta/nova/<int:pasta_pai_id>', methods=['GET', 'POST'])
@login_required
def nova_pasta(pasta_pai_id=None):
    if request.method == 'POST':
        nome = request.form.get('nome')
        descricao = request.form.get('descricao')
        icone = request.form.get('icone')
        cor = request.form.get('cor')
        pasta_pai_id = request.form.get('pasta_pai_id')
        
        nova_pasta = Pasta(
            nome=nome,
            descricao=descricao,
            icone=icone,
            cor=cor,
            pasta_pai_id=pasta_pai_id if pasta_pai_id else None,
            usuario_id=current_user.id
        )
        
        db.session.add(nova_pasta)
        db.session.commit()
        
        flash('Pasta criada com sucesso!', 'success')
        return redirect(url_for('pastas'))
    
    pasta_pai = None
    if pasta_pai_id:
        pasta_pai = Pasta.query.get(pasta_pai_id)
    
    return render_template('pasta_nova.html', pasta_pai=pasta_pai)

# Editar pasta
@app.route('/pasta/editar/<int:pasta_id>', methods=['GET', 'POST'])
@login_required
def editar_pasta(pasta_id):
    pasta = Pasta.query.get_or_404(pasta_id)
    
    if pasta.usuario_id != current_user.id:
        flash('Você não tem permissão para editar esta pasta.', 'danger')
        return redirect(url_for('pastas'))
    
    if request.method == 'POST':
        pasta.nome = request.form.get('nome')
        pasta.descricao = request.form.get('descricao')
        pasta.icone = request.form.get('icone')
        pasta.cor = request.form.get('cor')
        
        db.session.commit()
        flash('Pasta atualizada com sucesso!', 'success')
        return redirect(url_for('pastas'))
    
    return render_template('pasta_editar.html', pasta=pasta)

# Excluir pasta
@app.route('/pasta/excluir/<int:pasta_id>')
@login_required
def excluir_pasta(pasta_id):
    pasta = Pasta.query.get_or_404(pasta_id)
    
    if pasta.usuario_id != current_user.id:
        flash('Você não tem permissão para excluir esta pasta.', 'danger')
        return redirect(url_for('pastas'))
    
    # Verificar se tem tarefas
    if pasta.tarefas:
        flash('Não é possível excluir uma pasta que contém tarefas. Mova ou exclua as tarefas primeiro.', 'warning')
        return redirect(url_for('pastas'))
    
    db.session.delete(pasta)
    db.session.commit()
    flash('Pasta excluída!', 'success')
    return redirect(url_for('pastas'))

# Settings - Configurações do usuário
@app.route('/settings', methods=['GET', 'POST'])
@login_required
def settings():
    if request.method == 'POST':
        # Atualizar informações pessoais
        current_user.nome_completo = request.form.get('nome_completo')
        current_user.email = request.form.get('email')
        
        # Atualizar avatar
        current_user.avatar_emoji = request.form.get('avatar_emoji')
        current_user.avatar_cor = request.form.get('avatar_cor')
        
        # Atualizar tema
        current_user.tema_cor_principal = request.form.get('tema_cor')
        current_user.modo_escuro = 'modo_escuro' in request.form
        
        # Atualizar senha se fornecida
        nova_senha = request.form.get('nova_senha')
        if nova_senha:
            current_user.set_senha(nova_senha)
        
        db.session.commit()
        flash('Configurações salvas com sucesso!', 'success')
        return redirect(url_for('settings'))
    
    return render_template('settings.html')

# ============== INICIALIZAÇÃO ==============

if __name__ == '__main__':
    # Criar banco de dados se não existir
    with app.app_context():
        db.create_all()
    
    # Iniciar servidor
    app.run(debug=True, host='0.0.0.0', port=5000)
```

### 5.3 templates/base.html (Template Base)

```html
<!DOCTYPE html>
<html lang="pt-br" data-bs-theme="{{ 'dark' if current_user.modo_escuro else 'light' }}">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}To-Do Pro{% endblock %}</title>
    
    <!-- Bootstrap 5 CSS -->
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet">
    <!-- Font Awesome -->
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <!-- Google Fonts -->
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    
    <style>
        :root {
            --primary-color: {{ current_user.tema_cor_principal if current_user.is_authenticated else '#6366f1' }};
            --bs-primary: {{ current_user.tema_cor_principal if current_user.is_authenticated else '#6366f1' }};
        }
        
        body {
            font-family: 'Inter', sans-serif;
            background-color: var(--bs-body-bg);
        }
        
        .btn-primary {
            background-color: var(--primary-color);
            border-color: var(--primary-color);
        }
        
        .btn-primary:hover {
            background-color: color-mix(in srgb, var(--primary-color) 85%, black);
            border-color: color-mix(in srgb, var(--primary-color) 85%, black);
        }
        
        .avatar {
            width: 40px;
            height: 40px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 1.5rem;
            background-color: {{ current_user.avatar_cor if current_user.is_authenticated else '#6366f1' }};
        }
        
        .sidebar {
            min-height: 100vh;
            background: linear-gradient(180deg, var(--primary-color) 0%, #4f46e5 100%);
        }
        
        .task-card {
            transition: transform 0.2s, box-shadow 0.2s;
            border: none;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        
        .task-card:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(0,0,0,0.15);
        }
        
        .status-pendente { border-left: 4px solid #f59e0b; }
        .status-em_andamento { border-left: 4px solid #6366f1; }
        .status-concluida { border-left: 4px solid #10b981; }
        
        .priority-baixa { color: #10b981; }
        .priority-media { color: #6366f1; }
        .priority-alta { color: #f59e0b; }
        .priority-urgente { color: #ef4444; }
        
        .deadline-atrasada { color: #ef4444; }
        .deadline-proxima { color: #f59e0b; }
        
        .dropdown-menu {
            border: 1px solid rgba(0,0,0,0.1);
        }
        
        .navbar-brand {
            font-weight: 700;
        }
    </style>
    
    {% block extra_css %}{% endblock %}
</head>
<body>
    {% if current_user.is_authenticated %}
    <nav class="navbar navbar-expand-lg navbar-dark" style="background-color: var(--primary-color);">
        <div class="container-fluid">
            <a class="navbar-brand" href="{{ url_for('dashboard') }}">
                <i class="fas fa-check-double me-2"></i>To-Do Pro
            </a>
            
            <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav">
                <span class="navbar-toggler-icon"></span>
            </button>
            
            <div class="collapse navbar-collapse" id="navbarNav">
                <ul class="navbar-nav me-auto">
                    <li class="nav-item">
                        <a class="nav-link" href="{{ url_for('dashboard') }}">
                            <i class="fas fa-chart-line me-1"></i> Dashboard
                        </a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" href="{{ url_for('tarefas') }}">
                            <i class="fas fa-tasks me-1"></i> Tarefas
                        </a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" href="{{ url_for('pastas') }}">
                            <i class="fas fa-folder me-1"></i> Pastas
                        </a>
                    </li>
                </ul>
                
                <div class="d-flex align-items-center">
                    <div class="dropdown">
                        <button class="btn btn-light dropdown-toggle d-flex align-items-center gap-2" type="button" data-bs-toggle="dropdown">
                            <span class="avatar" style="width:32px;height:32px;font-size:1.2rem;">
                                {{ current_user.avatar_emoji }}
                            </span>
                            <span class="d-none d-md-inline">{{ current_user.username }}</span>
                        </button>
                        <ul class="dropdown-menu dropdown-menu-end">
                            <li><a class="dropdown-item" href="{{ url_for('settings') }}">
                                <i class="fas fa-cog me-2"></i>Configurações
                            </a></li>
                            <li><hr class="dropdown-divider"></li>
                            <li><a class="dropdown-item" href="{{ url_for('logout') }}">
                                <i class="fas fa-sign-out-alt me-2"></i>Sair
                            </a></li>
                        </ul>
                    </div>
                </div>
            </div>
        </div>
    </nav>
    {% endif %}
    
    <main class="flex-grow-1">
        {% with messages = get_flashed_messages(with_categories=true) %}
            {% if messages %}
                <div class="container mt-3">
                    {% for category, message in messages %}
                        <div class="alert alert-{{ category }} alert-dismissible fade show" role="alert">
                            {{ message }}
                            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
                        </div>
                    {% endfor %}
                </div>
            {% endif %}
        {% endwith %}
        
        {% block content %}{% endblock %}
    </main>
    
    <!-- Bootstrap 5 JS -->
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/js/bootstrap.bundle.min.js"></script>
    
    {% block extra_js %}{% endblock %}
</body>
</html>
```

### 5.4 templates/login.html

```html
{% extends "base.html" %}

{% block title %}Login - To-Do Pro{% endblock %}

{% block content %}
<div class="container">
    <div class="row justify-content-center mt-5">
        <div class="col-md-5">
            <div class="card shadow">
                <div class="card-body p-5">
                    <div class="text-center mb-4">
                        <i class="fas fa-check-double fa-3x" style="color: var(--primary-color);"></i>
                        <h2 class="mt-3 fw-bold">To-Do Pro</h2>
                        <p class="text-muted">Gerencie suas tarefas de forma eficiente</p>
                    </div>
                    
                    <form method="POST">
                        <div class="mb-3">
                            <label class="form-label">Usuário</label>
                            <div class="input-group">
                                <span class="input-group-text"><i class="fas fa-user"></i></span>
                                <input type="text" name="username" class="form-control" required>
                            </div>
                        </div>
                        
                        <div class="mb-3">
                            <label class="form-label">Senha</label>
                            <div class="input-group">
                                <span class="input-group-text"><i class="fas fa-lock"></i></span>
                                <input type="password" name="senha" class="form-control" required>
                            </div>
                        </div>
                        
                        <button type="submit" class="btn btn-primary w-100 py-2">
                            <i class="fas fa-sign-in-alt me-2"></i>Entrar
                        </button>
                    </form>
                    
                    <div class="text-center mt-4">
                        <p class="mb-0">Não tem uma conta? 
                            <a href="{{ url_for('cadastro') }}" style="color: var(--primary-color);">Cadastre-se</a>
                        </p>
                    </div>
                </div>
            </div>
        </div>
    </div>
</div>
{% endblock %}
```

### 5.5 templates/cadastro.html

```html
{% extends "base.html" %}

{% block title %}Cadastro - To-Do Pro{% endblock %}

{% block content %}
<div class="container">
    <div class="row justify-content-center mt-5">
        <div class="col-md-6">
            <div class="card shadow">
                <div class="card-body p-5">
                    <div class="text-center mb-4">
                        <i class="fas fa-user-plus fa-3x" style="color: var(--primary-color);"></i>
                        <h2 class="mt-3 fw-bold">Criar Conta</h2>
                        <p class="text-muted">Junte-se ao To-Do Pro</p>
                    </div>
                    
                    <form method="POST">
                        <div class="mb-3">
                            <label class="form-label">Nome de Usuário</label>
                            <input type="text" name="username" class="form-control" required>
                        </div>
                        
                        <div class="mb-3">
                            <label class="form-label">Nome Completo</label>
                            <input type="text" name="nome_completo" class="form-control">
                        </div>
                        
                        <div class="mb-3">
                            <label class="form-label">E-mail</label>
                            <input type="email" name="email" class="form-control" required>
                        </div>
                        
                        <div class="mb-3">
                            <label class="form-label">Senha</label>
                            <input type="password" name="senha" class="form-control" required minlength="6">
                        </div>
                        
                        <button type="submit" class="btn btn-primary w-100 py-2">
                            <i class="fas fa-user-plus me-2"></i>Criar Conta
                        </button>
                    </form>
                    
                    <div class="text-center mt-4">
                        <p class="mb-0">Já tem uma conta? 
                            <a href="{{ url_for('login') }}" style="color: var(--primary-color);">Faça login</a>
                        </p>
                    </div>
                </div>
            </div>
        </div>
    </div>
</div>
{% endblock %}
```

### 5.6 templates/dashboard.html

```html
{% extends "base.html" %}

{% block title %}Dashboard - To-Do Pro{% endblock %}

{% block content %}
<div class="container-fluid p-4">
    <h2 class="mb-4">
        <i class="fas fa-chart-line me-2"></i>Dashboard
    </h2>
    
    <!-- Estatísticas -->
    <div class="row mb-4">
        <div class="col-md-3">
            <div class="card task-card">
                <div class="card-body">
                    <div class="d-flex justify-content-between align-items-center">
                        <div>
                            <p class="text-muted mb-0">Total de Tarefas</p>
                            <h2 class="mb-0">{{ total }}</h2>
                        </div>
                        <div class="fs-1 text-primary opacity-50">
                            <i class="fas fa-tasks"></i>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        
        <div class="col-md-3">
            <div class="card task-card">
                <div class="card-body">
                    <div class="d-flex justify-content-between align-items-center">
                        <div>
                            <p class="text-muted mb-0">Pendentes</p>
                            <h2 class="mb-0" style="color: #f59e0b;">{{ pendentes }}</h2>
                        </div>
                        <div class="fs-1 text-warning opacity-50">
                            <i class="fas fa-clock"></i>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        
        <div class="col-md-3">
            <div class="card task-card">
                <div class="card-body">
                    <div class="d-flex justify-content-between align-items-center">
                        <div>
                            <p class="text-muted mb-0">Em Andamento</p>
                            <h2 class="mb-0" style="color: #6366f1;">{{ andamento }}</h2>
                        </div>
                        <div class="fs-1 text-primary opacity-50">
                            <i class="fas fa-spinner"></i>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        
        <div class="col-md-3">
            <div class="card task-card">
                <div class="card-body">
                    <div class="d-flex justify-content-between align-items-center">
                        <div>
                            <p class="text-muted mb-0">Concluídas</p>
                            <h2 class="mb-0" style="color: #10b981;">{{ concluidas }}</h2>
                        </div>
                        <div class="fs-1 text-success opacity-50">
                            <i class="fas fa-check-circle"></i>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
    
    <!-- Alertas -->
    {% if atrasadas %}
    <div class="alert alert-danger mb-4">
        <h5><i class="fas fa-exclamation-triangle me-2"></i>Você tem {{ atrasadas|length }} tarefa(s) atrasada(s)!</h5>
        <ul class="mb-0">
            {% for tarefa in atrasadas[:3] %}
            <li>{{ tarefa.titulo }} - {{ tarefa.pasta.icone if tarefa.pasta else '' }} {{ tarefa.pasta.nome if tarefa.pasta else 'Sem pasta' }}</li>
            {% endfor %}
        </ul>
    </div>
    {% endif %}
    
    <div class="row">
        <!-- Próximas Tarefas -->
        <div class="col-md-8">
            <div class="card task-card">
                <div class="card-header bg-white py-3">
                    <h5 class="mb-0"><i class="fas fa-list-check me-2"></i>Próximas Tarefas</h5>
                </div>
                <div class="card-body">
                    {% if tarefas_proximas %}
                    <div class="list-group list-group-flush">
                        {% for tarefa in tarefas_proximas %}
                        <div class="list-group-item border-0 px-0">
                            <div class="d-flex justify-content-between align-items-start">
                                <div class="form-check">
                                    <input type="checkbox" class="form-check-input" 
                                           onclick="window.location='{{ url_for('toggle_tarefa', tarefa_id=tarefa.id) }}'"
                                           {% if tarefa.status == 'concluida' %}checked{% endif %}>
                                    <label class="form-check-label {% if tarefa.status == 'concluida' %}text-decoration-line-through text-muted{% endif %}">
                                        {{ tarefa.titulo }}
                                    </label>
                                </div>
                                <div class="dropdown">
                                    <button class="btn btn-sm btn-light" data-bs-toggle="dropdown">
                                        <i class="fas fa-ellipsis-v"></i>
                                    </button>
                                    <ul class="dropdown-menu">
                                        <li><a class="dropdown-item" href="{{ url_for('editar_tarefa', tarefa_id=tarefa.id) }}">Editar</a></li>
                                        <li><a class="dropdown-item text-danger" href="{{ url_for('excluir_tarefa', tarefa_id=tarefa.id) }}">Excluir</a></li>
                                    </ul>
                                </div>
                            </div>
                            <small class="text-muted">
                                {% if tarefa.pasta %}{{ tarefa.pasta.icone }} {{ tarefa.pasta.nome }} | {% endif %}
                                <span class="priority-{{ tarefa.prioridade }}">{{ tarefa.prioridade.upper() }}</span>
                                {% if tarefa.deadline %}
                                | <span class="{% if tarefa.esta_atrasada() %}deadline-atrasada{% elif tarefa.tempo_restante() == 'Atrasada' %}deadline-atrasada{% else %}deadline-proxima{% endif %}">
                                    <i class="fas fa-calendar me-1"></i>{{ tarefa.tempo_restante() }}
                                </span>
                                {% endif %}
                            </small>
                        </div>
                        {% endfor %}
                    </div>
                    {% else %}
                    <p class="text-center text-muted py-4">
                        <i class="fas fa-check-circle fa-3x mb-3 d-block"></i>
                        Nenhuma tarefa pendente!
                    </p>
                    {% endif %}
                    
                    <a href="{{ url_for('tarefas') }}" class="btn btn-outline-primary mt-3">
                        Ver todas as tarefas <i class="fas fa-arrow-right ms-1"></i>
                    </a>
                </div>
            </div>
        </div>
        
        <!-- Ações Rápidas -->
        <div class="col-md-4">
            <div class="card task-card">
                <div class="card-header bg-white py-3">
                    <h5 class="mb-0"><i class="fas fa-bolt me-2"></i>Ações Rápidas</h5>
                </div>
                <div class="card-body">
                    <div class="d-grid gap-2">
                        <a href="{{ url_for('nova_tarefa') }}" class="btn btn-primary">
                            <i class="fas fa-plus me-2"></i>Nova Tarefa
                        </a>
                        <a href="{{ url_for('nova_pasta') }}" class="btn btn-outline-secondary">
                            <i class="fas fa-folder-plus me-2"></i>Nova Pasta
                        </a>
                        <a href="{{ url_for('settings') }}" class="btn btn-outline-secondary">
                            <i class="fas fa-cog me-2"></i>Configurações
                        </a>
                    </div>
                </div>
            </div>
            
            <!-- Pastas -->
            <div class="card task-card mt-3">
                <div class="card-header bg-white py-3">
                    <h5 class="mb-0"><i class="fas fa-folder me-2"></i>Suas Pastas</h5>
                </div>
                <div class="card-body">
                    {% if current_user.pastas %}
                    <div class="d-flex flex-wrap gap-2">
                        {% for pasta in current_user.pastas[:6] %}
                        <a href="{{ url_for('tarefas', pasta_id=pasta.id) }}" class="badge" style="background-color: {{ pasta.cor }}; font-size: 0.9rem;">
                            {{ pasta.icone }} {{ pasta.nome }}
                        </a>
                        {% endfor %}
                    </div>
                    {% else %}
                    <p class="text-muted text-center">Nenhuma pasta criada</p>
                    {% endif %}
                    
                    <a href="{{ url_for('pastas') }}" class="btn btn-outline-primary mt-3 w-100">
                        Gerenciar Pastas
                    </a>
                </div>
            </div>
        </div>
    </div>
</div>
{% endblock %}
```

### 5.7 templates/tarefas.html

```html
{% extends "base.html" %}

{% block title %}Tarefas - To-Do Pro{% endblock %}

{% block content %}
<div class="container-fluid p-4">
    <div class="d-flex justify-content-between align-items-center mb-4">
        <h2><i class="fas fa-tasks me-2"></i>Minhas Tarefas</h2>
        <a href="{{ url_for('nova_tarefa') }}" class="btn btn-primary">
            <i class="fas fa-plus me-2"></i>Nova Tarefa
        </a>
    </div>
    
    <!-- Filtros -->
    <div class="card mb-4">
        <div class="card-body">
            <form method="GET" class="row g-3">
                <div class="col-md-3">
                    <select name="status" class="form-select">
                        <option value="">Todos os Status</option>
                        <option value="pendente" {% if request.args.get('status') == 'pendente' %}selected{% endif %}>Pendente</option>
                        <option value="em_andamento" {% if request.args.get('status') == 'em_andamento' %}selected{% endif %}>Em Andamento</option>
                        <option value="concluida" {% if request.args.get('status') == 'concluida' %}selected{% endif %}>Concluída</option>
                    </select>
                </div>
                <div class="col-md-3">
                    <select name="prioridade" class="form-select">
                        <option value="">Todas as Prioridades</option>
                        <option value="baixa" {% if request.args.get('prioridade') == 'baixa' %}selected{% endif %}>Baixa</option>
                        <option value="media" {% if request.args.get('prioridade') == 'media' %}selected{% endif %}>Média</option>
                        <option value="alta" {% if request.args.get('prioridade') == 'alta' %}selected{% endif %}>Alta</option>
                        <option value="urgente" {% if request.args.get('prioridade') == 'urgente' %}selected{% endif %}>Urgente</option>
                    </select>
                </div>
                <div class="col-md-3">
                    <select name="pasta_id" class="form-select">
                        <option value="">Todas as Pastas</option>
                        {% for pasta in pastas %}
                        <option value="{{ pasta.id }}" {% if pasta_selecionada == pasta.id %}selected{% endif %}>
                            {{ pasta.icone }} {{ pasta.nome }}
                        </option>
                        {% endfor %}
                    </select>
                </div>
                <div class="col-md-3">
                    <button type="submit" class="btn btn-outline-primary w-100">
                        <i class="fas fa-filter me-2"></i>Filtrar
                    </button>
                </div>
            </form>
        </div>
    </div>
    
    <!-- Lista de Tarefas -->
    {% if tarefas %}
    <div class="row">
        {% for tarefa in tarefas %}
        <div class="col-md-6 col-lg-4 mb-3">
            <div class="card task-card status-{{ tarefa.status }}">
                <div class="card-body">
                    <div class="d-flex justify-content-between align-items-start mb-2">
                        <div class="form-check">
                            <input type="checkbox" class="form-check-input" 
                                   onclick="window.location='{{ url_for('toggle_tarefa', tarefa_id=tarefa.id) }}'"
                                   {% if tarefa.status == 'concluida' %}checked{% endif %}>
                            <h6 class="card-title d-inline {% if tarefa.status == 'concluida' %}text-decoration-line-through text-muted{% endif %}">
                                {{ tarefa.titulo }}
                            </h6>
                        </div>
                        <div class="dropdown">
                            <button class="btn btn-sm btn-light" data-bs-toggle="dropdown">
                                <i class="fas fa-ellipsis-v"></i>
                            </button>
                            <ul class="dropdown-menu">
                                <li><a class="dropdown-item" href="{{ url_for('editar_tarefa', tarefa_id=tarefa.id) }}">Editar</a></li>
                                <li><hr class="dropdown-divider"></li>
                                <li><a class="dropdown-item text-danger" href="{{ url_for('excluir_tarefa', tarefa_id=tarefa.id) }}">Excluir</a></li>
                            </ul>
                        </div>
                    </div>
                    
                    {% if tarefa.descricao %}
                    <p class="card-text text-muted small">{{ tarefa.descricao[:100] }}{% if tarefa.descricao|length > 100 %}...{% endif %}</p>
                    {% endif %}
                    
                    <div class="d-flex flex-wrap gap-2 mb-2">
                        {% if tarefa.pasta %}
                        <span class="badge" style="background-color: {{ tarefa.pasta.cor }};">
                            {{ tarefa.pasta.icone }} {{ tarefa.pasta.nome }}
                        </span>
                        {% endif %}
                        
                        <span class="badge bg-{% if tarefa.status == 'concluida' %}success{% elif tarefa.status == 'em_andamento' %}primary{% else %}warning{% endif %}">
                            {{ tarefa.status.replace('_', ' ').title() }}
                        </span>
                        
                        <span class="badge bg-{% if tarefa.prioridade == 'urgente' %}danger{% elif tarefa.prioridade == 'alta' %}warning{% elif tarefa.prioridade == 'media' %}primary{% else %}success{% endif %}">
                            {{ tarefa.prioridade.title() }}
                        </span>
                    </div>
                    
                    {% if tarefa.deadline %}
                    <small class="{% if tarefa.esta_atrasada() %}deadline-atrasada{% else %}deadline-proxima{% endif %}">
                        <i class="fas fa-calendar me-1"></i>
                        {% if tarefa.esta_atrasada() %}ATRASADA{% else %}{{ tarefa.tempo_restante() }}{% endif %}
                    </small>
                    {% endif %}
                </div>
            </div>
        </div>
        {% endfor %}
    </div>
    {% else %}
    <div class="text-center py-5">
        <i class="fas fa-clipboard-list fa-4x text-muted mb-3"></i>
        <h4>Nenhuma tarefa encontrada</h4>
        <p class="text-muted">Crie sua primeira tarefa para começar!</p>
        <a href="{{ url_for('nova_tarefa') }}" class="btn btn-primary">
            <i class="fas fa-plus me-2"></i>Criar Tarefa
        </a>
    </div>
    {% endif %}
</div>
{% endblock %}
```

### 5.8 templates/tarefa_nova.html

```html
{% extends "base.html" %}

{% block title %}Nova Tarefa - To-Do Pro{% endblock %}

{% block content %}
<div class="container">
    <div class="row justify-content-center">
        <div class="col-md-8">
            <div class="card task-card">
                <div class="card-header bg-white py-3">
                    <h4 class="mb-0"><i class="fas fa-plus me-2"></i>Nova Tarefa</h4>
                </div>
                <div class="card-body">
                    <form method="POST">
                        <div class="mb-3">
                            <label class="form-label">Título da Tarefa *</label>
                            <input type="text" name="titulo" class="form-control" required 
                                   placeholder="O que você precisa fazer?">
                        </div>
                        
                        <div class="mb-3">
                            <label class="form-label">Descrição</label>
                            <textarea name="descricao" class="form-control" rows="3" 
                                      placeholder="Detalhes adicionais (opcional)"></textarea>
                        </div>
                        
                        <div class="row">
                            <div class="col-md-6 mb-3">
                                <label class="form-label">Pasta (Categoria)</label>
                                <select name="pasta_id" class="form-select">
                                    <option value="">Sem pasta</option>
                                    {% for pasta in pastas %}
                                    <option value="{{ pasta.id }}">{{ pasta.icone }} {{ pasta.nome }}</option>
                                    {% endfor %}
                                </select>
                            </div>
                            
                            <div class="col-md-6 mb-3">
                                <label class="form-label">Prioridade</label>
                                <select name="prioridade" class="form-select">
                                    <option value="baixa">Baixa</option>
                                    <option value="media" selected>Média</option>
                                    <option value="alta">Alta</option>
                                    <option value="urgente">Urgente</option>
                                </select>
                            </div>
                        </div>
                        
                        <div class="mb-3">
                            <label class="form-label">Data Limite (Deadline)</label>
                            <input type="datetime-local" name="deadline" class="form-control">
                            <small class="text-muted">Defina um prazo para esta tarefa (opcional)</small>
                        </div>
                        
                        <div class="d-flex gap-2">
                            <button type="submit" class="btn btn-primary">
                                <i class="fas fa-check me-2"></i>Criar Tarefa
                            </button>
                            <a href="{{ url_for('tarefas') }}" class="btn btn-outline-secondary">Cancelar</a>
                        </div>
                    </form>
                </div>
            </div>
        </div>
    </div>
</div>
{% endblock %}
```

### 5.9 templates/tarefa_editar.html

```html
{% extends "base.html" %}

{% block title %}Editar Tarefa - To-Do Pro{% endblock %}

{% block content %}
<div class="container">
    <div class="row justify-content-center">
        <div class="col-md-8">
            <div class="card task-card">
                <div class="card-header bg-white py-3">
                    <h4 class="mb-0"><i class="fas fa-edit me-2"></i>Editar Tarefa</h4>
                </div>
                <div class="card-body">
                    <form method="POST">
                        <div class="mb-3">
                            <label class="form-label">Título da Tarefa *</label>
                            <input type="text" name="titulo" class="form-control" required 
                                   value="{{ tarefa.titulo }}">
                        </div>
                        
                        <div class="mb-3">
                            <label class="form-label">Descrição</label>
                            <textarea name="descricao" class="form-control" rows="3">{{ tarefa.descricao or '' }}</textarea>
                        </div>
                        
                        <div class="row">
                            <div class="col-md-6 mb-3">
                                <label class="form-label">Pasta (Categoria)</label>
                                <select name="pasta_id" class="form-select">
                                    <option value="">Sem pasta</option>
                                    {% for pasta in pastas %}
                                    <option value="{{ pasta.id }}" {% if tarefa.pasta_id == pasta.id %}selected{% endif %}>
                                        {{ pasta.icone }} {{ pasta.nome }}
                                    </option>
                                    {% endfor %}
                                </select>
                            </div>
                            
                            <div class="col-md-6 mb-3">
                                <label class="form-label">Prioridade</label>
                                <select name="prioridade" class="form-select">
                                    <option value="baixa" {% if tarefa.prioridade == 'baixa' %}selected{% endif %}>Baixa</option>
                                    <option value="media" {% if tarefa.prioridade == 'media' %}selected{% endif %}>Média</option>
                                    <option value="alta" {% if tarefa.prioridade == 'alta' %}selected{% endif %}>Alta</option>
                                    <option value="urgente" {% if tarefa.prioridade == 'urgente' %}selected{% endif %}>Urgente</option>
                                </select>
                            </div>
                        </div>
                        
                        <div class="mb-3">
                            <label class="form-label">Status</label>
                            <select name="status" class="form-select">
                                <option value="pendente" {% if tarefa.status == 'pendente' %}selected{% endif %}>Pendente</option>
                                <option value="em_andamento" {% if tarefa.status == 'em_andamento' %}selected{% endif %}>Em Andamento</option>
                                <option value="concluida" {% if tarefa.status == 'concluida' %}selected{% endif %}>Concluída</option>
                            </select>
                        </div>
                        
                        <div class="mb-3">
                            <label class="form-label">Data Limite (Deadline)</label>
                            <input type="datetime-local" name="deadline" class="form-control" 
                                   value="{{ tarefa.deadline.strftime('%Y-%m-%dT%H:%M') if tarefa.deadline else '' }}">
                        </div>
                        
                        <div class="d-flex gap-2">
                            <button type="submit" class="btn btn-primary">
                                <i class="fas fa-save me-2"></i>Salvar Alterações
                            </button>
                            <a href="{{ url_for('tarefas') }}" class="btn btn-outline-secondary">Cancelar</a>
                        </div>
                    </form>
                </div>
            </div>
        </div>
    </div>
</div>
{% endblock %}
```

### 5.10 templates/pastas.html

```html
{% extends "base.html" %}

{% block title %}Pastas - To-Do Pro{% endblock %}

{% block content %}
<div class="container-fluid p-4">
    <div class="d-flex justify-content-between align-items-center mb-4">
        <h2><i class="fas fa-folder me-2"></i>Minhas Pastas</h2>
        <a href="{{ url_for('nova_pasta') }}" class="btn btn-primary">
            <i class="fas fa-plus me-2"></i>Nova Pasta
        </a>
    </div>
    
    {% if pastas %}
    <div class="row">
        {% for pasta in pastas %}
        <div class="col-md-6 col-lg-4 mb-4">
            <div class="card task-card h-100">
                <div class="card-body" style="border-top: 4px solid {{ pasta.cor }};">
                    <div class="d-flex justify-content-between align-items-start">
                        <div>
                            <h5 class="card-title">
                                <span class="fs-4 me-2">{{ pasta.icone }}</span>
                                {{ pasta.nome }}
                            </h5>
                            {% if pasta.descricao %}
                            <p class="text-muted small">{{ pasta.descricao }}</p>
                            {% endif %}
                        </div>
                        <div class="dropdown">
                            <button class="btn btn-sm btn-light" data-bs-toggle="dropdown">
                                <i class="fas fa-ellipsis-v"></i>
                            </button>
                            <ul class="dropdown-menu">
                                <li><a class="dropdown-item" href="{{ url_for('nova_pasta', pasta_pai_id=pasta.id) }}">Criar Subpasta</a></li>
                                <li><a class="dropdown-item" href="{{ url_for('editar_pasta', pasta_id=pasta.id) }}">Editar</a></li>
                                <li><hr class="dropdown-divider"></li>
                                <li><a class="dropdown-item text-danger" href="{{ url_for('excluir_pasta', pasta_id=pasta.id) }}">Excluir</a></li>
                            </ul>
                        </div>
                    </div>
                    
                    <div class="mt-3">
                        <span class="badge bg-secondary">{{ pasta.tarefas|length }} tarefa(s)</span>
                        {% if pasta.subpastas %}
                        <span class="badge bg-info">{{ pasta.subpastas|length }} subpasta(s)</span>
                        {% endif %}
                    </div>
                    
                    <div class="mt-3">
                        <a href="{{ url_for('tarefas', pasta_id=pasta.id) }}" class="btn btn-sm btn-outline-primary">
                            <i class="fas fa-tasks me-1"></i>Ver Tarefas
                        </a>
                    </div>
                    
                    <!-- Subpastas -->
                    {% if pasta.subpastas %}
                    <div class="mt-3 pt-3 border-top">
                        <small class="text-muted d-block mb-2">Subpastas:</small>
                        {% for subpasta in pasta.subpastas %}
                        <a href="{{ url_for('tarefas', pasta_id=subpasta.id) }}" class="badge text-decoration-none me-1" 
                           style="background-color: {{ subpasta.cor }};">
                            {{ subpasta.icone }} {{ subpasta.nome }}
                        </a>
                        {% endfor %}
                    </div>
                    {% endif %}
                </div>
            </div>
        </div>
        {% endfor %}
    </div>
    {% else %}
    <div class="text-center py-5">
        <i class="fas fa-folder-open fa-4x text-muted mb-3"></i>
        <h4>Nenhuma pasta criada</h4>
        <p class="text-muted">Crie pastas para organizar suas tarefas!</p>
        <a href="{{ url_for('nova_pasta') }}" class="btn btn-primary">
            <i class="fas fa-plus me-2"></i>Criar Primeira Pasta
        </a>
    </div>
    {% endif %}
</div>
{% endblock %}
```

### 5.11 templates/pasta_nova.html

```html
{% extends "base.html" %}

{% block title %}Nova Pasta - To-Do Pro{% endblock %}

{% block content %}
<div class="container">
    <div class="row justify-content-center">
        <div class="col-md-6">
            <div class="card task-card">
                <div class="card-header bg-white py-3">
                    <h4 class="mb-0">
                        {% if pasta_pai %}
                        <i class="fas fa-folder-plus me-2"></i>Nova Subpasta
                        {% else %}
                        <i class="fas fa-folder-plus me-2"></i>Nova Pasta
                        {% endif %}
                    </h4>
                </div>
                <div class="card-body">
                    {% if pasta_pai %}
                    <div class="alert alert-info">
                        <i class="fas fa-info-circle me-2"></i>
                        Criando subpasta dentro de: <strong>{{ pasta_pai.icone }} {{ pasta_pai.nome }}</strong>
                    </div>
                    {% endif %}
                    
                    <form method="POST">
                        <input type="hidden" name="pasta_pai_id" value="{{ pasta_pai.id if pasta_pai else '' }}">
                        
                        <div class="mb-3">
                            <label class="form-label">Nome da Pasta *</label>
                            <input type="text" name="nome" class="form-control" required 
                                   placeholder="Ex: Trabalho, Pessoal, Estudos">
                        </div>
                        
                        <div class="mb-3">
                            <label class="form-label">Descrição</label>
                            <textarea name="descricao" class="form-control" rows="2" 
                                      placeholder="Descrição opcional"></textarea>
                        </div>
                        
                        <div class="mb-3">
                            <label class="form-label">Ícone</label>
                            <select name="icone" class="form-select">
                                <option value="📁">📁 Pasta</option>
                                <option value="💼">💼 Trabalho</option>
                                <option value="🏠">🏠 Casa</option>
                                <option value="🎓">🎓 Estudos</option>
                                <option value="💰">💰 Financeiro</option>
                                <option value="🏃">🏃 Pessoal</option>
                                <option value="🛒">🛒 Compras</option>
                                <option value="🎯">🎯 Projetos</option>
                                <option value="📚">📚 Livros</option>
                                <option value="🎮">🎮 Jogos</option>
                                <option value="✈️">✈️ Viagens</option>
                                <option value="❤️">❤️ Saúde</option>
                            </select>
                        </div>
                        
                        <div class="mb-3">
                            <label class="form-label">Cor</label>
                            <div class="d-flex flex-wrap gap-2">
                                <input type="radio" class="btn-check" name="cor" id="cor1" value="#6366f1" checked>
                                <label class="btn btn-outline-primary btn-sm" for="cor1">Indigo</label>
                                
                                <input type="radio" class="btn-check" name="cor" id="cor2" value="#10b981">
                                <label class="btn btn-outline-success btn-sm" for="cor2">Green</label>
                                
                                <input type="radio" class="btn-check" name="cor" id="cor3" value="#f59e0b">
                                <label class="btn btn-outline-warning btn-sm" for="cor3">Amber</label>
                                
                                <input type="radio" class="btn-check" name="cor" id="cor4" value="#ef4444">
                                <label class="btn btn-outline-danger btn-sm" for="cor4">Red</label>
                                
                                <input type="radio" class="btn-check" name="cor" id="cor5" value="#8b5cf6">
                                <label class="btn btn-outline-purple btn-sm" for="cor5">Purple</label>
                                
                                <input type="radio" class="btn-check" name="cor" id="cor6" value="#06b6d4">
                                <label class="btn btn-outline-info btn-sm" for="cor6">Cyan</label>
                            </div>
                        </div>
                        
                        <div class="d-flex gap-2">
                            <button type="submit" class="btn btn-primary">
                                <i class="fas fa-check me-2"></i>Criar Pasta
                            </button>
                            <a href="{{ url_for('pastas') }}" class="btn btn-outline-secondary">Cancelar</a>
                        </div>
                    </form>
                </div>
            </div>
        </div>
    </div>
</div>
{% endblock %}
```

### 5.12 templates/pasta_editar.html

```html
{% extends "base.html" %}

{% block title %}Editar Pasta - To-Do Pro{% endblock %}

{% block content %}
<div class="container">
    <div class="row justify-content-center">
        <div class="col-md-6">
            <div class="card task-card">
                <div class="card-header bg-white py-3">
                    <h4 class="mb-0"><i class="fas fa-edit me-2"></i>Editar Pasta</h4>
                </div>
                <div class="card-body">
                    <form method="POST">
                        <div class="mb-3">
                            <label class="form-label">Nome da Pasta *</label>
                            <input type="text" name="nome" class="form-control" required value="{{ pasta.nome }}">
                        </div>
                        
                        <div class="mb-3">
                            <label class="form-label">Descrição</label>
                            <textarea name="descricao" class="form-control" rows="2">{{ pasta.descricao or '' }}</textarea>
                        </div>
                        
                        <div class="mb-3">
                            <label class="form-label">Ícone</label>
                            <select name="icone" class="form-select">
                                {% set icons = [('📁', 'Pasta'), ('💼', 'Trabalho'), ('🏠', 'Casa'), ('🎓', 'Estudos'), ('💰', 'Financeiro'), ('🏃', 'Pessoal'), ('🛒', 'Compras'), ('🎯', 'Projetos'), ('📚', 'Livros'), ('🎮', 'Jogos'), ('✈️', 'Viagens'), ('❤️', 'Saúde')] %}
                                {% for icon, name in icons %}
                                <option value="{{ icon }}" {% if pasta.icone == icon %}selected{% endif %}>{{ icon }} {{ name }}</option>
                                {% endfor %}
                            </select>
                        </div>
                        
                        <div class="mb-3">
                            <label class="form-label">Cor</label>
                            {% set colors = [('#6366f1', 'Indigo'), ('#10b981', 'Green'), ('#f59e0b', 'Amber'), ('#ef4444', 'Red'), ('#8b5cf6', 'Purple'), ('#06b6d4', 'Cyan')] %}
                            <div class="d-flex flex-wrap gap-2">
                                {% for color, name in colors %}
                                <input type="radio" class="btn-check" name="cor" id="cor{{ loop.index }}" value="{{ color }}" {% if pasta.cor == color %}checked{% endif %}>
                                <label class="btn btn-sm {% if color == '#8b5cf6' %}btn-outline-purple{% elif color == '#06b6d4' %}btn-outline-info{% else %}btn-outline-{{ name.lower() }}{% endif %}" for="cor{{ loop.index }}">{{ name }}</label>
                                {% endfor %}
                            </div>
                        </div>
                        
                        <div class="d-flex gap-2">
                            <button type="submit" class="btn btn-primary">
                                <i class="fas fa-save me-2"></i>Salvar Alterações
                            </button>
                            <a href="{{ url_for('pastas') }}" class="btn btn-outline-secondary">Cancelar</a>
                        </div>
                    </form>
                </div>
            </div>
        </div>
    </div>
</div>
{% endblock %}
```

### 5.13 templates/settings.html

```html
{% extends "base.html" %}

{% block title %}Configurações - To-Do Pro{% endblock %}

{% block content %}
<div class="container-fluid p-4">
    <h2 class="mb-4"><i class="fas fa-cog me-2"></i>Configurações</h2>
    
    <div class="row">
        <div class="col-lg-8">
            <div class="card task-card mb-4">
                <div class="card-header bg-white py-3">
                    <h5 class="mb-0"><i class="fas fa-user me-2"></i>Informações Pessoais</h5>
                </div>
                <div class="card-body">
                    <form method="POST">
                        <div class="row">
                            <div class="col-md-6 mb-3">
                                <label class="form-label">Nome de Usuário</label>
                                <input type="text" class="form-control" value="{{ current_user.username }}" disabled>
                                <small class="text-muted">O nome de usuário não pode ser alterado</small>
                            </div>
                            
                            <div class="col-md-6 mb-3">
                                <label class="form-label">Nome Completo</label>
                                <input type="text" name="nome_completo" class="form-control" value="{{ current_user.nome_completo or '' }}">
                            </div>
                        </div>
                        
                        <div class="mb-3">
                            <label class="form-label">E-mail</label>
                            <input type="email" name="email" class="form-control" value="{{ current_user.email }}">
                        </div>
                        
                        <div class="mb-3">
                            <label class="form-label">Nova Senha</label>
                            <input type="password" name="nova_senha" class="form-control" placeholder="Deixe em branco para manter a atual">
                        </div>
                        
                        <button type="submit" class="btn btn-primary">
                            <i class="fas fa-save me-2"></i>Salvar Informações
                        </button>
                    </form>
                </div>
            </div>
            
            <div class="card task-card mb-4">
                <div class="card-header bg-white py-3">
                    <h5 class="mb-0"><i class="fas fa-palette me-2"></i>Personalização</h5>
                </div>
                <div class="card-body">
                    <form method="POST">
                        <!-- Avatar Emoji -->
                        <div class="mb-4">
                            <label class="form-label">Avatar (Emoji)</label>
                            <div class="d-flex flex-wrap gap-2">
                                {% set emojis = ['👤', '👨', '👩', '🧑', '👨‍💻', '👩‍💻', '🦸', '🦹', '🧙', '🧚', '🧛', '🧜', '🧝', '🧞', '🐱', '🐶', '🦊', '🐼', '🐨', '🦁', '🐯', '🐲', '🌟', '💫'] %}
                                {% for emoji in emojis %}
                                <input type="radio" class="btn-check" name="avatar_emoji" id="emoji{{ loop.index }}" value="{{ emoji }}" {% if current_user.avatar_emoji == emoji %}checked{% endif %}>
                                <label class="btn btn-outline-secondary btn-sm fs-5" for="emoji{{ loop.index }}">{{ emoji }}</label>
                                {% endfor %}
                            </div>
                        </div>
                        
                        <!-- Cor do Avatar -->
                        <div class="mb-4">
                            <label class="form-label">Cor do Avatar</label>
                            <div class="d-flex flex-wrap gap-2">
                                {% set avatar_colors = ['#6366f1', '#8b5cf6', '#ec4899', '#ef4444', '#f59e0b', '#10b981', '#06b6d4', '#3b82f6'] %}
                                {% for av_color in avatar_colors %}
                                <input type="radio" class="btn-check" name="avatar_cor" id="avcolor{{ loop.index }}" value="{{ av_color }}" {% if current_user.avatar_cor == av_color %}checked{% endif %}>
                                <label class="btn btn-sm" style="background-color: {{ av_color }}; border-color: {{ av_color }};" for="avcolor{{ loop.index }}">
                                    <i class="fas fa-check text-white" {% if current_user.avatar_cor != av_color %}style="display:none"{% endif %}></i>
                                </label>
                                {% endfor %}
                            </div>
                        </div>
                        
                        <!-- Cor do Tema -->
                        <div class="mb-4">
                            <label class="form-label">Cor Principal do Tema</label>
                            <div class="d-flex flex-wrap gap-2">
                                {% set theme_colors = [('#6366f1', 'Indigo'), ('#8b5cf6', 'Purple'), ('#ec4899', 'Pink'), ('#ef4444', 'Red'), ('#f59e0b', 'Amber'), ('#10b981', 'Emerald'), ('#06b6d4', 'Cyan'), ('#3b82f6', 'Blue')] %}
                                {% for t_color, t_name in theme_colors %}
                                <input type="radio" class="btn-check" name="tema_cor" id="tema{{ loop.index }}" value="{{ t_color }}" {% if current_user.tema_cor_principal == t_color %}checked{% endif %}>
                                <label class="btn btn-sm btn-outline-{{ t_name.lower() }}" for="tema{{ loop.index }}">{{ t_name }}</label>
                                {% endfor %}
                            </div>
                        </div>
                        
                        <!-- Modo Escuro -->
                        <div class="mb-4">
                            <div class="form-check form-switch">
                                <input class="form-check-input" type="checkbox" name="modo_escuro" id="modo_escuro" {% if current_user.modo_escuro %}checked{% endif %}>
                                <label class="form-check-label" for="modo_escuro">
                                    <i class="fas fa-moon me-1"></i>Modo Escuro
                                </label>
                            </div>
                        </div>
                        
                        <button type="submit" class="btn btn-primary">
                            <i class="fas fa-save me-2"></i>Salvar Personalização
                        </button>
                    </form>
                </div>
            </div>
        </div>
        
        <!-- Preview -->
        <div class="col-lg-4">
            <div class="card task-card">
                <div class="card-header bg-white py-3">
                    <h5 class="mb-0"><i class="fas fa-eye me-2"></i>Preview</h5>
                </div>
                <div class="card-body text-center">
                    <div class="avatar mx-auto mb-3" style="width:80px;height:80px;font-size:3rem; background-color: {{ current_user.avatar_cor }};">
                        {{ current_user.avatar_emoji }}
                    </div>
                    <h5>{{ current_user.username }}</h5>
                    <p class="text-muted">{{ current_user.nome_completo or 'Seu nome' }}</p>
                    
                    <hr>
                    
                    <div class="text-start">
                        <p class="mb-1"><strong>Cor do tema:</strong> 
                            <span class="badge" style="background-color: {{ current_user.tema_cor_principal }};">{{ current_user.tema_cor_principal }}</span>
                        </p>
                        <p class="mb-0"><strong>Modo escuro:</strong> 
                            {% if current_user.modo_escuro %}
                            <span class="badge bg-success">Ativado</span>
                            {% else %}
                            <span class="badge bg-secondary">Desativado</span>
                            {% endif %}
                        </p>
                    </div>
                </div>
            </div>
        </div>
    </div>
</div>
{% endblock %}
```

### 5.14 static/style.css (Estilos Adicionais)

```css
/* Estilos extras para o To-Do Pro */

/* Animações */
@keyframes fadeIn {
    from { opacity: 0; transform: translateY(10px); }
    to { opacity: 1; transform: translateY(0); }
}

.card.task-card {
    animation: fadeIn 0.3s ease-out;
}

/* Hover nos cards de tarefas */
.card.task-card:hover {
    transform: translateY(-3px);
    box-shadow: 0 8px 25px rgba(0,0,0,0.12);
}

/* Status indicators */
.status-dot {
    width: 10px;
    height: 10px;
    border-radius: 50%;
    display: inline-block;
    margin-right: 8px;
}

.status-dot.pendente { background-color: #f59e0b; }
.status-dot.em_andamento { background-color: #6366f1; }
.status-dot.concluida { background-color: #10b981; }

/* Badges personalizados */
.badge-prioridade {
    font-size: 0.7rem;
    padding: 4px 8px;
    text-transform: uppercase;
    font-weight: 600;
}

/* Deadline styling */
.deadline-badge {
    font-size: 0.75rem;
    padding: 3px 8px;
    border-radius: 12px;
}

.deadline-badge.atrasada {
    background-color: rgba(239, 68, 68, 0.1);
    color: #ef4444;
    border: 1px solid #ef4444;
}

.deadline-badge.proxima {
    background-color: rgba(245, 158, 11, 0.1);
    color: #f59e0b;
    border: 1px solid #f59e0b;
}

.deadline-badge.normal {
    background-color: rgba(16, 185, 129, 0.1);
    color: #10b981;
    border: 1px solid #10b981;
}

/* Sidebar para mobile */
@media (max-width: 768px) {
    .sidebar {
        position: fixed;
        z-index: 1000;
        width: 250px;
        transform: translateX(-100%);
        transition: transform 0.3s ease;
    }
    
    .sidebar.show {
        transform: translateX(0);
    }
}

/* Custom scrollbar */
::-webkit-scrollbar {
    width: 8px;
    height: 8px;
}

::-webkit-scrollbar-track {
    background: #f1f1f1;
}

::-webkit-scrollbar-thumb {
    background: #c1c1c1;
    border-radius: 4px;
}

::-webkit-scrollbar-thumb:hover {
    background: #a1a1a1;
}

/* Dark mode scrollbar */
[data-bs-theme="dark"] ::-webkit-scrollbar-track {
    background: #1e293b;
}

[data-bs-theme="dark"] ::-webkit-scrollbar-thumb {
    background: #475569;
}

/* Form controls */
.form-control:focus, .form-select:focus {
    border-color: var(--primary-color);
    box-shadow: 0 0 0 0.2rem rgba(var(--bs-primary-rgb), 0.25);
}

/* Checkbox customizado */
.form-check-input:checked {
    background-color: var(--primary-color);
    border-color: var(--primary-color);
}

/* Dropdown */
.dropdown-item:hover {
    background-color: var(--primary-color);
    color: white;
}

/* Loading spinner */
.spinner {
    width: 40px;
    height: 40px;
    border: 4px solid #f3f3f3;
    border-top: 4px solid var(--primary-color);
    border-radius: 50%;
    animation: spin 1s linear infinite;
}

@keyframes spin {
    0% { transform: rotate(0deg); }
    100% { transform: rotate(360deg); }
}
```

---

## 6. EXECUTANDO O PROJETO

### 6.1 Executar Localmente

```bash
# Ativar o ambiente virtual (se ainda não estiver ativo)
.\venv\Scripts\Activate

# Executar o projeto
python app/main.py
```

O servidor akan dimulai di `http://localhost:5000`.

### 6.2 Executar com Flask

```bash
# Definir variáveis de ambiente
set FLASK_APP=app/main.py
set FLASK_ENV=development

# Executar
python -m flask run
```

---

## 7. FUNCIONALIDADES IMPLEMENTADAS

### 7.1 Sistema de Autenticação
- ✅ Cadastro de múltiplos usuários
- ✅ Login com senha hasheada (segurança)
- ✅ Logout
- ✅ **Isolamento total** - Cada usuário vê apenas suas próprias tarefas

### 7.2 CRUD de Tarefas
| Operação | Descrição | Rota |
|----------|------------|------|
| **Create** | Criar nova tarefa | `/tarefa/nova` |
| **Read** | Listar tarefas | `/tarefas` |
| **Update** | Editar tarefa | `/tarefa/editar/<id>` |
| **Delete** | Excluir tarefa | `/tarefa/excluir/<id>` |

### 7.3 Sistema de Pastas/Categorias
- ✅ Criar pastas raiz
- ✅ Criar subpastas (aninhamento)
- ✅ Ícones e cores personalizáveis
- ✅ Associar tarefas às pastas

### 7.4 Status e Prioridades
| Status | Descrição |
|--------|-----------|
| Pendente | Tarefa ainda não iniciada |
| Em Andamento | Tarefa em execução |
| Concluída | Tarefa finalizada |

| Prioridade | Cor |
|------------|-----|
| Baixa | Verde |
| Média | Indigo |
| Alta | Amarelo |
| Urgente | Vermelho |

### 7.5 Deadline/Prazos
- ✅ Data limite opcional
- ✅ Tempo restante calculado automaticamente
- ✅ Alerta de tarefas atrasadas
- ✅ Dashboard com tarefas próximas do prazo

---

## 8. PERSONALIZAÇÃO (SETTINGS)

A página de configurações permite:

### 8.1 Informações Pessoais
- Alterar nome completo
- Alterar e-mail
- Alterar senha

### 8.2 Personalização
- **Avatar Emoji** - 24 opções de emojis
- **Cor do Avatar** - 8 cores disponíveis
- **Cor do Tema** - 8 cores para a navbar
- **Modo Escuro** - Toggle para tema escuro

---

## 9. IMPLANTAÇÃO (DEPLOY)

### 9.1 Arquivos Necessários para Deploy

**runtime.txt:**
```
python-3.11.10
```

**Procfile:**
```
web: pip install -r requirements.txt && python app/main.py
```

**.gitignore:**
```
__pycache__/
*.pyc
venv/
.venv/
instance/
*.db
.env
```

### 9.2 Deploy no Render (Gratuito)

1. **Crie uma conta no Render**: https://render.com
2. **Conecte seu GitHub**
3. **Crie um Web Service**:
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `python app/main.py`
4. **Variáveis de Ambiente**:
   - `SECRET_KEY`: Uma chave segura
   - `FLASK_ENV`: `production`

### 9.3 Comandos Git

```bash
# Inicializar git
git init

# Adicionar arquivos
git add .

# Commit
git commit -m "To-Do Pro v1.0 - Completo"

# Renomear branch
git branch -M main

# Adicionar remoto
git remote add origin https://github.com/SEU_USUARIO/todo-pro.git

# Enviar
git push -u origin main
```

---

## 10. DEMONSTRANDO SUAS HABILIDADES

Este projeto demonstra as seguintes habilidades de CRUD e mais:

### ✅ CRUD Completo
- **Create**: Criar tarefas, pastas, usuários
- **Read**: Ler/listar tarefas, estatísticas
- **Update**: Editar tarefas, pastas, configurações
- **Delete**: Excluir tarefas e pastas

### ✅ Banco de Dados Relacional
- SQLAlchemy ORM
- Relacionamentos (User → Pasta → Tarefa)
- Foreign Keys e Cascade Delete

### ✅ Autenticação e Autorização
- Flask-Login
- Senhas hasheadas com Werkzeug
- Rotas protegidas com @login_required

### ✅ Design Moderno
- Bootstrap 5
- CSS Custom Properties
- Interface responsiva
- Modo escuro

### ✅ Boas Práticas
- Código organizado
- Separação de responsabilidades
- Validação de dados
- Mensagens de feedback (Flash)

---

## 📚 Resumo dos Comandos

```bash
# Criar ambiente virtual
python -m venv venv

# Ativar (Windows)
.\venv\Scripts\Activate

# Instalar dependências
pip install Flask==3.0.0 Flask-SQLAlchemy==3.1.1 Flask-Login==0.6.3 Werkzeug==3.0.1

# Executar
python app/main.py

# Acessar
http://localhost:5000
```

---

## ✅ Checklist Final

- [x] Ambiente virtual criado
- [x] Dependências instaladas
- [x] Banco de dados criado automaticamente
- [x] Aplicação rodando em localhost:5000
- [x] Cadastro de usuário funcionando
- [x] CRUD de tarefas completo
- [x] Sistema de pastas implementado
- [x] Deadline funcionando
- [x] Dashboard com estatísticas
- [x] Settings com personalização
- [x] Modo escuro disponível
- [x] Deploy no GitHub (opcional)
- [x] Deploy no Render (opcional)

---

**Projeto desenvolvido com ❤️ usando Python e Flask**

Este To-Do List completo demonstra suas habilidades avançadas em:
- Programação Python
- Desenvolvimento Web com Flask
- Banco de Dados SQLAlchemy
- Autenticação e Autorização
- Design de Interface Moderna
- boas práticas de Desenvolvimento
