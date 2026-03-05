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
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'sua-chave-secreta-aqui-mude-para-producao')

# Configurar o caminho do banco de dados
import os
db_path = os.environ.get('DATABASE_PATH')
if db_path:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_path
else:
    # Para desenvolvimento local
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    instance_dir = os.path.join(base_dir, 'instance')
    os.makedirs(instance_dir, exist_ok=True)
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{os.path.join(instance_dir, "todolist.db")}'
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

db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# ============== MODELOS DO BANCO DE DADOS ==============

# Modelo de Usuário
class Usuario(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    senha = db.Column(db.String(150), nullable=False)
    nome_completo = db.Column(db.String(200))
    
    # Avatar e Tema
    avatar_color = db.Column(db.String(20), default='#6366f1')
    avatar_emoji = db.Column(db.String(10), default='👤')  # Emoji do avatar
    tema_cor_principal = db.Column(db.String(20), default='#6366f1')  # Cor principal do tema
    
    # Configurações do usuário
    tema_escuro = db.Column(db.Boolean, default=False)
    notificacoes_email = db.Column(db.Boolean, default=True)
    idioma = db.Column(db.String(10), default='pt-BR')
    
    # Relacionamentos
    pastas = db.relationship('Pasta', backref='dono', lazy=True)
    tarefas = db.relationship('Tarefa', backref='dono', lazy=True)

# Modelo de Pasta (Categoria/Grupo de tarefas)
class Pasta(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    descricao = db.Column(db.Text)
    cor = db.Column(db.String(20), default='#6366f1')
    icone = db.Column(db.String(50), default='📁')
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)
    pasta_pai_id = db.Column(db.Integer, db.ForeignKey('pasta.id'), nullable=True)
    data_criacao = db.Column(db.DateTime, default=datetime.now)
    ordem = db.Column(db.Integer, default=0)
    
    # Relacionamento para subpastas
    subpastas = db.relationship('Pasta', backref=db.backref('pasta_pai', remote_side=[id]), lazy=True)
    tarefas = db.relationship('Tarefa', backref='pasta', lazy=True)

# Modelo de Tarefa
class Tarefa(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(200), nullable=False)
    descricao = db.Column(db.Text)
    prioridade = db.Column(db.String(20), default='media')  # baixa, media, alta, urgente
    status = db.Column(db.String(20), default='pendente')  # pendente, em_progresso, concluida
    
    # Datas
    data_criacao = db.Column(db.DateTime, default=datetime.now)
    data_conclusao = db.Column(db.DateTime, nullable=True)
    deadline = db.Column(db.DateTime, nullable=True)  # Data limite
    
    # Relacionamentos
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)
    pasta_id = db.Column(db.Integer, db.ForeignKey('pasta.id'), nullable=True)
    
    # Lembretes
    lembrete_enviado = db.Column(db.Boolean, default=False)

# Modelo de Configurações do Sistema
class ConfiguracaoSistema(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    chave = db.Column(db.String(100), unique=True, nullable=False)
    valor = db.Column(db.Text)

# ============== HELPERS E DECORADORES ==============

@login_manager.user_loader
def load_user(user_id):
    return Usuario.query.get(int(user_id))

def admin_required(f):
    """Decorator para rotas que requerem admin"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            flash('Por favor, faça login para acessar esta página.', 'error')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

def get_config(key, default=None):
    """Obtém configuração do banco de dados ou usa valor padrão"""
    config = ConfiguracaoSistema.query.filter_by(chave=key).first()
    if config:
        return config.valor
    return default

def calcular_tempo_restante(deadline):
    """Calcula o tempo restante até o deadline"""
    if not deadline:
        return None
    
    agora = datetime.now()
    diferenca = deadline - agora
    
    if diferenca.total_seconds() < 0:
        return {'atrasada': True, 'dias': 0, 'horas': 0, 'minutos': 0}
    
    dias = diferenca.days
    horas = diferenca.seconds // 3600
    minutos = (diferenca.seconds % 3600) // 60
    
    return {
        'atrasada': False,
        'dias': dias,
        'horas': horas,
        'minutos': minutos,
        'total_horas': dias * 24 + horas
    }

# ============== ROTAS DE AUTENTICAÇÃO ==============

@app.route('/')
def index():
    """Página inicial - Redirect para login ou dashboard"""
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    """Página de cadastro de novos usuários"""
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        senha = request.form.get('senha')
        nome_completo = request.form.get('nome_completo')
        
        # Validações
        if Usuario.query.filter_by(username=username).first():
            flash('Nome de usuário já existe!', 'error')
            return render_template('cadastro.html')
        
        if Usuario.query.filter_by(email=email).first():
            flash('E-mail já cadastrado!', 'error')
            return render_template('cadastro.html')
        
        # Criar novo usuário
        cores_avatar = ['#6366f1', '#8b5cf6', '#06b6d4', '#10b981', '#f59e0b', '#ef4444']
        import random
        novo_usuario = Usuario(
            username=username,
            email=email,
            senha=generate_password_hash(senha),
            nome_completo=nome_completo,
            avatar_color=random.choice(cores_avatar)
        )
        
        db.session.add(novo_usuario)
        db.session.commit()
        
        # Criar pasta padrão "Geral" para o usuário
        pasta_geral = Pasta(
            nome='Geral',
            descricao='Tarefas gerais',
            cor='#6366f1',
            icone='📋',
            usuario_id=novo_usuario.id
        )
        db.session.add(pasta_geral)
        db.session.commit()
        
        flash('Conta criada com sucesso! Faça login para continuar.', 'success')
        return redirect(url_for('login'))
    
    return render_template('cadastro.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Página de login"""
    if request.method == 'POST':
        username = request.form.get('username')
        senha = request.form.get('senha')
        
        usuario = Usuario.query.filter_by(username=username).first()
        
        if usuario and check_password_hash(usuario.senha, senha):
            login_user(usuario)
            return redirect(url_for('dashboard'))
        else:
            flash('Nome de usuário ou senha incorretos!', 'error')
    
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    """Rota para logout"""
    logout_user()
    flash('Você foi desconectado com sucesso!', 'success')
    return redirect(url_for('login'))

# ============== ROTAS DO DASHBOARD ==============

@app.route('/dashboard')
@login_required
def dashboard():
    """Dashboard principal - mostra overview das tarefas"""
    # Estatísticas
    tarefas_total = Tarefa.query.filter_by(usuario_id=current_user.id).count()
    tarefas_concluidas = Tarefa.query.filter_by(usuario_id=current_user.id, status='concluida').count()
    tarefas_pendentes = Tarefa.query.filter_by(usuario_id=current_user.id, status='pendente').count()
    tarefas_em_andamento = Tarefa.query.filter_by(usuario_id=current_user.id, status='em_progresso').count()
    
    # Tarefas com deadline próximo (próximas 24 horas)
    agora = datetime.now()
    amanha = agora + timedelta(days=1)
    tarefas_proximas = Tarefa.query.filter(
        Tarefa.usuario_id == current_user.id,
        Tarefa.status != 'concluida',
        Tarefa.deadline != None,
        Tarefa.deadline <= amanha
    ).order_by(Tarefa.deadline).limit(5).all()
    
    # Tarefas atrasadas
    tarefas_atrasadas = Tarefa.query.filter(
        Tarefa.usuario_id == current_user.id,
        Tarefa.status != 'concluida',
        Tarefa.deadline != None,
        Tarefa.deadline < agora
    ).order_by(Tarefa.deadline).all()
    
    # Calcular tempo restante para tarefas próximas
    for tarefa in tarefas_proximas:
        tarefa.tempo_restante = calcular_tempo_restante(tarefa.deadline)
    
    for tarefa in tarefas_atrasadas:
        tarefa.tempo_restante = calcular_tempo_restante(tarefa.deadline)
    
    # Tarefas recentes
    tarefas_recentes = Tarefa.query.filter_by(usuario_id=current_user.id)\
        .order_by(Tarefa.data_criacao.desc()).limit(5).all()
    
    # Pastas do usuário
    pastas = Pasta.query.filter_by(usuario_id=current_user.id, pasta_pai_id=None)\
        .order_by(Pasta.ordem, Pasta.nome).all()
    
    return render_template('dashboard.html',
                         tarefas_total=tarefas_total,
                         tarefas_concluidas=tarefas_concluidas,
                         tarefas_pendentes=tarefas_pendentes,
                         tarefas_em_andamento=tarefas_em_andamento,
                         tarefas_proximas=tarefas_proximas,
                         tarefas_atrasadas=tarefas_atrasadas,
                         tarefas_recentes=tarefas_recentes,
                         pastas=pastas)

# ============== ROTAS DE TAREFAS ==============

@app.route('/tarefas')
@login_required
def listar_tarefas():
    """Lista todas as tarefas do usuário"""
    pasta_id = request.args.get('pasta_id', type=int)
    status = request.args.get('status')
    prioridade = request.args.get('prioridade')
    
    query = Tarefa.query.filter_by(usuario_id=current_user.id)
    
    if pasta_id:
        query = query.filter_by(pasta_id=pasta_id)
    
    if status:
        query = query.filter_by(status=status)
    
    if prioridade:
        query = query.filter_by(prioridade=prioridade)
    
    tarefas = query.order_by(Tarefa.deadline, Tarefa.prioridade.desc()).all()
    pastas = Pasta.query.filter_by(usuario_id=current_user.id).all()
    
    # Calcular tempo restante
    for tarefa in tarefas:
        tarefa.tempo_restante = calcular_tempo_restante(tarefa.deadline)
    
    return render_template('tarefas.html', tarefas=tarefas, pastas=pastas, pasta_selecionada=pasta_id)

@app.route('/tarefas/nova', methods=['GET', 'POST'])
@login_required
def nova_tarefa():
    """Criar nova tarefa"""
    if request.method == 'POST':
        titulo = request.form.get('titulo')
        descricao = request.form.get('descricao')
        prioridade = request.form.get('prioridade', 'media')
        pasta_id = request.form.get('pasta_id', type=int)
        deadline = request.form.get('deadline')
        deadline_hora = request.form.get('deadline_hora', '23:59')
        
        # Converter deadline
        deadline_dt = None
        if deadline:
            deadline_str = f"{deadline} {deadline_hora}"
            deadline_dt = datetime.strptime(deadline_str, '%Y-%m-%d %H:%M')
        
        tarefa = Tarefa(
            titulo=titulo,
            descricao=descricao,
            prioridade=prioridade,
            pasta_id=pasta_id if pasta_id else None,
            deadline=deadline_dt,
            usuario_id=current_user.id
        )
        
        db.session.add(tarefa)
        db.session.commit()
        
        flash('Tarefa criada com sucesso!', 'success')
        return redirect(url_for('listar_tarefas'))
    
    pastas = Pasta.query.filter_by(usuario_id=current_user.id).all()
    return render_template('tarefa_nova.html', pastas=pastas)

@app.route('/tarefas/editar/<int:id>', methods=['GET', 'POST'])
@login_required
def editar_tarefa(id):
    """Editar tarefa existente"""
    tarefa = Tarefa.query.get_or_404(id)
    
    if tarefa.usuario_id != current_user.id:
        flash('Você não tem permissão para editar esta tarefa!', 'error')
        return redirect(url_for('listar_tarefas'))
    
    if request.method == 'POST':
        tarefa.titulo = request.form.get('titulo')
        tarefa.descricao = request.form.get('descricao')
        tarefa.prioridade = request.form.get('prioridade')
        tarefa.pasta_id = request.form.get('pasta_id', type=int) or None
        tarefa.status = request.form.get('status', 'pendente')
        
        deadline = request.form.get('deadline')
        deadline_hora = request.form.get('deadline_hora', '23:59')
        
        if deadline:
            deadline_str = f"{deadline} {deadline_hora}"
            tarefa.deadline = datetime.strptime(deadline_str, '%Y-%m-%d %H:%M')
        else:
            tarefa.deadline = None
        
        db.session.commit()
        flash('Tarefa atualizada com sucesso!', 'success')
        return redirect(url_for('listar_tarefas'))
    
    pastas = Pasta.query.filter_by(usuario_id=current_user.id).all()
    return render_template('tarefa_editar.html', tarefa=tarefa, pastas=pastas)

@app.route('/tarefas/excluir/<int:id>')
@login_required
def excluir_tarefa(id):
    """Excluir tarefa"""
    tarefa = Tarefa.query.get_or_404(id)
    
    if tarefa.usuario_id != current_user.id:
        flash('Você não tem permissão para excluir esta tarefa!', 'error')
        return redirect(url_for('listar_tarefas'))
    
    db.session.delete(tarefa)
    db.session.commit()
    
    flash('Tarefa excluída com sucesso!', 'success')
    return redirect(url_for('listar_tarefas'))

@app.route('/tarefas/concluir/<int:id>')
@login_required
def concluir_tarefa(id):
    """Marcar tarefa como concluída"""
    tarefa = Tarefa.query.get_or_404(id)
    
    if tarefa.usuario_id != current_user.id:
        flash('Você não tem permissão para modificar esta tarefa!', 'error')
        return redirect(url_for('listar_tarefas'))
    
    tarefa.status = 'concluida'
    tarefa.data_conclusao = datetime.now()
    db.session.commit()
    
    flash('Tarefa concluída! 🎉', 'success')
    return redirect(request.referrer or url_for('listar_tarefas'))

@app.route('/tarefas/reativar/<int:id>')
@login_required
def reativar_tarefa(id):
    """Reativar tarefa concluída"""
    tarefa = Tarefa.query.get_or_404(id)
    
    if tarefa.usuario_id != current_user.id:
        flash('Você não tem permissão para modificar esta tarefa!', 'error')
        return redirect(url_for('listar_tarefas'))
    
    tarefa.status = 'pendente'
    tarefa.data_conclusao = None
    db.session.commit()
    
    flash('Tarefa reativada!', 'success')
    return redirect(request.referrer or url_for('listar_tarefas'))

@app.route('/tarefas/status/<int:id>/<status>')
@login_required
def alterar_status(id, status):
    """Alterar status da tarefa"""
    tarefa = Tarefa.query.get_or_404(id)
    
    if tarefa.usuario_id != current_user.id:
        flash('Você não tem permissão para modificar esta tarefa!', 'error')
        return redirect(url_for('listar_tarefas'))
    
    tarefa.status = status
    if status == 'concluida':
        tarefa.data_conclusao = datetime.now()
    else:
        tarefa.data_conclusao = None
    
    db.session.commit()
    flash('Status atualizado!', 'success')
    return redirect(request.referrer or url_for('listar_tarefas'))

# ============== ROTAS DE PASTAS ==============

@app.route('/pastas')
@login_required
def listar_pastas():
    """Lista todas as pastas do usuário"""
    pastas = Pasta.query.filter_by(usuario_id=current_user.id, pasta_pai_id=None)\
        .order_by(Pasta.ordem, Pasta.nome).all()
    
    # Contar tarefas em cada pasta
    for pasta in pastas:
        pasta.total_tarefas = Tarefa.query.filter_by(pasta_id=pasta.id).count()
        pasta.tarefas_pendentes = Tarefa.query.filter_by(pasta_id=pasta.id, status='pendente').count()
    
    return render_template('pastas.html', pastas=pastas)

@app.route('/pastas/nova', methods=['GET', 'POST'])
@login_required
def nova_pasta():
    """Criar nova pasta"""
    if request.method == 'POST':
        nome = request.form.get('nome')
        descricao = request.form.get('descricao')
        cor = request.form.get('cor', '#6366f1')
        icone = request.form.get('icone', '📁')
        pasta_pai_id = request.form.get('pasta_pai_id', type=int)
        
        # Verificar limite de subpastas
        if pasta_pai_id:
            pasta_pai = Pasta.query.get(pasta_pai_id)
            if pasta_pai and pasta_pai.pasta_pai_id:
                flash('Limite máximo de subpastas atingido!', 'error')
                return redirect(url_for('listar_pastas'))
        
        pasta = Pasta(
            nome=nome,
            descricao=descricao,
            cor=cor,
            icone=icone,
            pasta_pai_id=pasta_pai_id if pasta_pai_id else None,
            usuario_id=current_user.id
        )
        
        db.session.add(pasta)
        db.session.commit()
        
        flash('Pasta criada com sucesso!', 'success')
        return redirect(url_for('listar_pastas'))
    
    pastas = Pasta.query.filter_by(usuario_id=current_user.id, pasta_pai_id=None).all()
    return render_template('pasta_nova.html', pastas=pastas)

@app.route('/pastas/editar/<int:id>', methods=['GET', 'POST'])
@login_required
def editar_pasta(id):
    """Editar pasta existente"""
    pasta = Pasta.query.get_or_404(id)
    
    if pasta.usuario_id != current_user.id:
        flash('Você não tem permissão para editar esta pasta!', 'error')
        return redirect(url_for('listar_pastas'))
    
    if request.method == 'POST':
        pasta.nome = request.form.get('nome')
        pasta.descricao = request.form.get('descricao')
        pasta.cor = request.form.get('cor', '#6366f1')
        pasta.icone = request.form.get('icone', '📁')
        
        db.session.commit()
        flash('Pasta atualizada com sucesso!', 'success')
        return redirect(url_for('listar_pastas'))
    
    pastas_raiz = Pasta.query.filter_by(usuario_id=current_user.id, pasta_pai_id=None).all()
    return render_template('pasta_editar.html', pasta=pasta, pastas=pastas_raiz)

@app.route('/pastas/excluir/<int:id>')
@login_required
def excluir_pasta(id):
    """Excluir pasta"""
    pasta = Pasta.query.get_or_404(id)
    
    if pasta.usuario_id != current_user.id:
        flash('Você não tem permissão para excluir esta pasta!', 'error')
        return redirect(url_for('listar_pastas'))
    
    # Mover tarefas para a pasta "Geral" ou excluir
    tarefas_na_pasta = Tarefa.query.filter_by(pasta_id=id).all()
    pasta_geral = Pasta.query.filter_by(usuario_id=current_user.id, nome='Geral').first()
    
    for tarefa in tarefas_na_pasta:
        if pasta_geral:
            tarefa.pasta_id = pasta_geral.id
        else:
            tarefa.pasta_id = None
    
    # Excluir subpastas
    subpastas = Pasta.query.filter_by(pasta_pai_id=id).all()
    for subpasta in subpastas:
        db.session.delete(subpasta)
    
    db.session.delete(pasta)
    db.session.commit()
    
    flash('Pasta excluída! Tarefas foram movidas para Geral.', 'success')
    return redirect(url_for('listar_pastas'))

# ============== ROTAS DE CONFIGURAÇÕES ==============

@app.route('/settings', methods=['GET', 'POST'])
@login_required
def settings():
    """Página de configurações do usuário"""
    if request.method == 'POST':
        # Atualizar informações do perfil
        current_user.nome_completo = request.form.get('nome_completo')
        current_user.email = request.form.get('email')
        
        # Atualizar senha se fornecida
        nova_senha = request.form.get('nova_senha')
        if nova_senha:
            current_user.set_senha(nova_senha)
        
        # Atualizar configurações de tema
        current_user.modo_escuro = 'modo_escuro' in request.form
        
        # Atualizar cor do avatar
        current_user.avatar_cor = request.form.get('avatar_cor', '#6366f1')
        
        # Atualizar emoji do avatar
        current_user.avatar_emoji = request.form.get('avatar_emoji', '👤')
        
        # Atualizar cor principal do tema
        current_user.tema_cor_principal = request.form.get('tema_cor', '#6366f1')
        
        db.session.commit()
        flash('Configurações salvas com sucesso!', 'success')
        return redirect(url_for('settings'))
    
    return render_template('settings.html')

# ============== ROTAS DE API (JSON) ==============

@app.route('/api/tarefas/proximas')
@login_required
def api_tarefas_proximas():
    """API retorna tarefas com deadline próximo"""
    dias = request.args.get('dias', 3, type=int)
    agora = datetime.now()
    limite = agora + timedelta(days=dias)
    
    tarefas = Tarefa.query.filter(
        Tarefa.usuario_id == current_user.id,
        Tarefa.status != 'concluida',
        Tarefa.deadline != None,
        Tarefa.deadline <= limite,
        Tarefa.deadline >= agora
    ).order_by(Tarefa.deadline).all()
    
    return {
        'tarefas': [{
            'id': t.id,
            'titulo': t.titulo,
            'deadline': t.deadline.isoformat(),
            'prioridade': t.prioridade
        } for t in tarefas]
    }

# ============== INICIALIZAÇÃO ==============

def init_db():
    """Inicializa o banco de dados"""
    with app.app_context():
        db.create_all()
        print("Banco de dados criado com sucesso!")

if __name__ == '__main__':
    # Inicializar banco de dados
    with app.app_context():
        db.create_all()
    
    # Production mode - usa a porta do ambiente (necessário para o Render)
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
