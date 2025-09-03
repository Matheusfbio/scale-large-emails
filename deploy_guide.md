# 🚀 Guia de Deploy - Sistema de Classificação de Emails

## 📋 Pré-requisitos
- Conta no GitHub
- Projeto commitado no GitHub
- Python 3.11+

## 🛠️ Configurações Realizadas

### Arquivos Criados/Modificados:
- ✅ `Procfile` - Configuração do servidor
- ✅ `runtime.txt` - Versão do Python
- ✅ `requirements.txt` - Dependências atualizadas
- ✅ `settings.py` - Configurações de produção
- ✅ `.env.example` - Exemplo de variáveis de ambiente

## 🌐 Opções de Deploy Gratuito

### 1. Railway (RECOMENDADO) 🚄
**Vantagens:** 500h grátis/mês, PostgreSQL incluído, fácil configuração

**Deploy:**
1. Acesse: https://railway.app
2. Conecte com GitHub
3. Selecione seu repositório
4. Adicione variáveis de ambiente:
   ```
   SECRET_KEY=django-insecure-sua-chave-secreta-aqui
   DEBUG=False
   ALLOWED_HOSTS=*.railway.app
   ```
5. Deploy automático!

### 2. Render 🎨
**Vantagens:** 750h grátis/mês, PostgreSQL gratuito (90 dias)

**Deploy:**
1. Acesse: https://render.com
2. Conecte repositório GitHub
3. Crie "Web Service"
4. Configurações:
   - **Build Command:** 
     ```
     pip install -r requirements.txt && python manage.py collectstatic --noinput && python manage.py migrate
     ```
   - **Start Command:** 
     ```
     gunicorn web_django.wsgi:application
     ```
5. Adicione variáveis de ambiente (mesmo do Railway)

### 3. PythonAnywhere 🐍
**Vantagens:** Específico para Python, MySQL incluído

**Deploy:**
1. Acesse: https://www.pythonanywhere.com
2. Crie conta gratuita
3. Upload do código via Git
4. Configure Web App Django
5. Configure variáveis no arquivo settings

### 4. Fly.io ✈️
**Vantagens:** Docker-based, global CDN

**Deploy:**
1. Instale Fly CLI
2. `fly auth login`
3. `fly launch`
4. Configure variáveis: `fly secrets set SECRET_KEY=sua-chave`

## 🔧 Comandos Importantes

### Gerar SECRET_KEY:
```python
from django.core.management.utils import get_random_secret_key
print(get_random_secret_key())
```

### Testar localmente:
```bash
# Instalar dependências
pip install -r requirements.txt

# Aplicar migrações
python manage.py migrate

# Coletar arquivos estáticos
python manage.py collectstatic

# Testar servidor
gunicorn web_django.wsgi:application
```

## 🔒 Variáveis de Ambiente Obrigatórias

```
SECRET_KEY=django-insecure-sua-chave-secreta-super-longa
DEBUG=False
ALLOWED_HOSTS=*.railway.app,*.render.com,seu-dominio.com
DATABASE_URL=postgres://user:pass@host:port/db (se usar PostgreSQL)
```

## 📊 Recomendações por Caso de Uso

| Plataforma | Melhor Para | Limitações |
|------------|-------------|------------|
| Railway | Projetos com IA/ML | 500h/mês |
| Render | Apps tradicionais | Build time limitado |
| PythonAnywhere | Iniciantes Python | CPU limitado |
| Fly.io | Apps globais | Configuração complexa |

## 🎯 Deploy Recomendado: Railway

**Por que Railway?**
- ✅ Suporte nativo a modelos de ML
- ✅ PostgreSQL integrado
- ✅ Deploy automático via Git
- ✅ Logs detalhados
- ✅ Fácil escalabilidade

**Link final:** Após deploy, você receberá um link como:
`https://seu-projeto-production-xxxx.up.railway.app`

## 🔍 Troubleshooting

### Erro "Application Error":
1. Verifique logs da plataforma
2. Confirme variáveis de ambiente
3. Execute migrações: `python manage.py migrate`

### Arquivos estáticos não carregam:
1. Execute: `python manage.py collectstatic`
2. Verifique configuração do WhiteNoise

### Erro de banco de dados:
1. Configure DATABASE_URL
2. Execute migrações em produção

## 📞 Suporte
- Railway: https://docs.railway.app
- Render: https://render.com/docs
- Comunidade Django: https://docs.djangoproject.com/en/stable/howto/deployment/
