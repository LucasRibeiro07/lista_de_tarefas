# 🚨 Solução Definitiva: Deploy no Render

## Problema Atual
O Render está usando Python 3.14 por padrão e ignorando o arquivo runtime.txt. O Flask-SQLAlchemy não é compatível com Python 3.14.

## SOLUÇÃO PASSO A PASSO

### Passo 1: Limpar o Cache do Build no Render

1. Acesse seu dashboard no Render
2. Clique no seu Web Service
3. Vá em **Settings** (abaixo do nome)
4. Desça até **"Clear Build Cache"**
5. Clique no botão **"Clear Cache"**

### Passo 2: Fazer Deploy Novamente

1. Vá na aba **"Deploy"**
2. Clique em **"Clear cache and deploy"**
3. Marque a opção **"Clear cache"**
4. Clique em **"Deploy"**

### Passo 3: Verificar os Logs

Nos logs, procure por:
```
==> Using Python-3.11.10 (requested: python-3.11.10)
```

Se aparecer `Python-3.14.x`, o cache não foi limpo.

---

## Se Ainda Não Funcionar

### Opção A: Forçar Versão no Procfile

Altere o Procfile para:

```bash
web: pip install --force-reinstall 'setuptools<70' wheel && pip install -r requirements.txt && python app/main.py
```

### Opção B: Usar Gunicorn (Recomendado)

1. Adicione ao requirements.txt:
```
gunicorn==21.2.0
```

2. Altere o Procfile:
```
web: gunicorn app.main:app --worker-class sync --workers 1 --bind 0.0.0.0:$PORT
```

### Opção C: Usar Versões Compatíveis

Se nada funcionar, use versões que funcionam com Python 3.14:

No requirements.txt:
```
Flask==3.1.0
Flask-SQLAlchemy==3.1.1
Flask-Login==0.6.3
Werkzeug==3.1.3
SQLAlchemy==2.0.36
```

---

## Verificando a Versão do Python no Render

Após o deploy, nos logs você DEVE ver:
```
==> Using Python-3.11.10 (requested: python-3.11.10)
```

Se vir:
```
==> Using Python-3.14.x (system)
```

O cache não foi limpo corretamente. Repita o Passo 1 e 2.

---

## Erro Específico: "ExtensionNotFound"

Se der erro:
```
ExtensionNotFound: 'sqlalchemy'
```

Execute:
```
pip uninstall flask-sqlalchemy -y
pip install flask-sqlalchemy==3.1.1
```

---

## Configuração Correta dos Arquivos

### runtime.txt (exatamente assim):
```
python-3.11.10
```

### Procfile:
```
web: pip install --upgrade pip setuptools wheel && pip install -r requirements.txt && python app/main.py
```

### requirements.txt:
```
Flask==3.0.0
Flask-SQLAlchemy==3.1.1
Flask-Login==0.6.3
Werkzeug==3.0.1
SQLAlchemy==2.0.23
python-dotenv==1.0.0
```

---

## Checklist de Deploy

- [ ] runtime.txt com python-3.11.10
- [ ] Procfile correto
- [ ] requirements.txt com versões compatíveis
- [ ] Limpar cache do build no Render
- [ ] Deploy com "Clear cache and deploy"

---

## Se Mesmo Assim Não Funcionar

Entre em contato com o suporte do Render ou considere usar outro serviço como Railway ou Fly.io.
