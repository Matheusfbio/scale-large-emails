# 🐳 Deploy Docker no Render - Sistema de Classificação de Emails

## 🚀 Deploy Automático no Render

### **1. Preparação do Projeto**

✅ **Arquivos Docker criados:**
- `Dockerfile` - Container de produção otimizado
- `docker-compose.yml` - Desenvolvimento local com PostgreSQL
- `.dockerignore` - Arquivos excluídos do build

### **2. Deploy no Render com Docker**

#### **Método 1: Deploy Automático (Recomendado)**

1. **Acesse [render.com](https://render.com)**
2. **Clique "New +" → "Web Service"**
3. **Conecte repositório GitHub**
4. **Configure o serviço:**
   ```
   Name: email-classifier-docker
   Runtime: Docker
   Branch: main
   Root Directory: . (deixe vazio)
   ```

5. **Variáveis de Ambiente:**
   ```
   SECRET_KEY=django-insecure-sua-chave-secreta-super-longa-aqui
   DEBUG=False
   ALLOWED_HOSTS=*.onrender.com
   DATABASE_URL=postgres://username:password@hostname:port/database
   PORT=10000
   ```

6. **Render detecta o Dockerfile automaticamente!**
7. **Deploy em ~5-10 minutos**

#### **Método 2: Deploy via CLI**

```bash
# Instalar Render CLI
npm install -g @render/cli

# Login
render auth login

# Deploy
render service create --name email-classifier --type web \
  --repo https://github.com/seu-usuario/seu-repo \
  --branch main \
  --runtime docker \
  --env SECRET_KEY=sua-chave \
  --env DEBUG=False
```

### **3. Desenvolvimento Local com Docker**

#### **Executar localmente:**

```bash
# Build e start todos os serviços
docker-compose up --build

# Em background
docker-compose up -d

# Ver logs
docker-compose logs -f web

# Parar serviços
docker-compose down
```

#### **Comandos úteis:**

```bash
# Executar migrações
docker-compose exec web python manage.py migrate

# Criar superuser
docker-compose exec web python manage.py createsuperuser

# Coletar static files
docker-compose exec web python manage.py collectstatic

# Shell Django
docker-compose exec web python manage.py shell

# Bash no container
docker-compose exec web bash
```

### **4. Configuração PostgreSQL no Render**

#### **Criar banco de dados:**
1. **No painel Render → "New +" → "PostgreSQL"**
2. **Configure:**
   ```
   Name: email-classifier-db
   Database: emailclassifier
   User: admin
   Plan: Free
   ```
3. **Copie a DATABASE_URL**
4. **Cole nas variáveis de ambiente do Web Service**

### **5. Vantagens do Docker**

| Vantagem | Descrição |
|----------|-----------|
| **Consistência** | Mesmo ambiente dev/prod |
| **Isolamento** | Dependências isoladas |
| **Portabilidade** | Roda em qualquer lugar |
| **Escalabilidade** | Fácil de escalar |
| **Debugging** | Logs centralizados |

### **6. Monitoramento**

#### **Health Check:**
```bash
# Verificar saúde do container
curl -f http://seu-app.onrender.com/health

# Logs em tempo real
render logs --service=email-classifier --follow
```

#### **Métricas no Render:**
- CPU/Memory usage
- Request rate
- Response time
- Error rate

### **7. Troubleshooting**

#### **Build falhou:**
```bash
# Ver logs detalhados
render logs --service=email-classifier --build

# Testar build local
docker build -t email-classifier .
docker run -p 8000:8000 email-classifier
```

#### **Container não inicia:**
```bash
# Verificar variáveis de ambiente
render env list --service=email-classifier

# Debug container
docker run -it email-classifier bash
```

#### **Banco não conecta:**
```bash
# Testar conexão
docker-compose exec web python manage.py dbshell

# Ver configuração
docker-compose exec web python manage.py shell
>>> from django.conf import settings
>>> print(settings.DATABASES)
```

### **8. Segurança Docker**

✅ **Configurações aplicadas:**
- Non-root user (`appuser`)
- Multi-stage build (otimizado)
- Health checks
- Security scan automático
- Minimal base image (`python:3.11-slim`)

### **9. Deploy Checklist**

- [ ] Dockerfile criado
- [ ] .dockerignore configurado
- [ ] requirements.txt atualizado
- [ ] Variáveis de ambiente definidas
- [ ] PostgreSQL configurado
- [ ] Código commitado no GitHub
- [ ] Render conectado ao repo
- [ ] Deploy executado com sucesso
- [ ] Health check passou
- [ ] Site funcionando

### **10. URLs Finais**

Após o deploy, você terá:
- **App:** `https://email-classifier-docker.onrender.com`
- **Admin:** `https://email-classifier-docker.onrender.com/admin/`
- **API:** `https://email-classifier-docker.onrender.com/classify/`

### **11. Próximos Passos**

1. **Configurar domínio customizado**
2. **Implementar CI/CD com GitHub Actions**
3. **Adicionar monitoring (Sentry)**
4. **Configurar backup automático**
5. **Implementar cache (Redis)**

---

## 🏆 Por que Docker + Render?

- ✅ **Facilidade:** Deploy com 1 clique
- ✅ **Confiabilidade:** Container isolado
- ✅ **Performance:** Otimizado para produção
- ✅ **Manutenção:** Updates automáticos
- ✅ **Custo:** Free tier generoso
- ✅ **ML Support:** Suporte completo a modelos

**Seu projeto está pronto para produção! 🚀**
