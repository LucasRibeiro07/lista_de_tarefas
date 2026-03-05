# 🚨 Solução: Problema com Python 3.14 no Render

## Problema
O Render está usando Python 3.14 por padrão, mas o SQLAlchemy não é compatível com Python 3.14.

## Solução - Faça no Render:

### Opção 1: Limpar Cache e Deploy (Recomendado)
1. Vá no seu Web Service no Render
2. Clique em **Settings** (abaixo do nome do serviço)
3. Desça até **"Clear Build Cache"** e clique no botão
4. Vá em **"Deploy"** → **"Clear cache and deploy"**

### Opção 2: Recriar o Serviço
1. Delete o Web Service atual
2. Crie um novo Web Service:
   - Nome: `todo-pro`
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `python app/main.py`
3. Adicione a variável `SECRET_KEY`

### Opção 3: Definir Python Explicitamente
No arquivo `runtime.txt`, garanta que está assim:
```
python-3.11.10
```

E no Render, ao criar o serviço, verifique se o Python correto será usado.

---

## Verificar Versão do Python
Após o deploy, nos logs você deve ver:
```
==> Using Python-3.11.10 (requested: python-3.11.10)
```

Se aparecer `Python-3.14.x`, o cache não foi limpo corretamente.

---

## Se ainda tiver problemas
Pode ser que o Render precise de um tempo para atualizar. Espere 2-3 minutos e tente novamente.
