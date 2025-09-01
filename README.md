# Sistema de Classificação de Emails com IA

Um sistema Django completo para classificação automática de emails como **Produtivo** ou **Improdutivo** usando técnicas de Processamento de Linguagem Natural (NLP) e Inteligência Artificial.

## 🚀 Funcionalidades

### **Backend em Python**
- **Leitura e Processamento**: Script Python que processa conteúdo de emails
- **NLP**: Pré-processamento de texto (remoção de stop words, stemming, etc.)
- **Classificação**: Algoritmo que categoriza emails automaticamente
- **IA**: Integração com Hugging Face Transformers para análise avançada
- **Geração de Respostas**: Sugestões automáticas baseadas na categoria

### **Interface Web**
- **Formulário de Entrada**: Interface para inserir emails
- **Resultados em Tempo Real**: Exibição da classificação e resposta sugerida
- **Lista de Emails**: Histórico de todos os emails processados
- **Estatísticas**: Dashboard com gráficos e métricas
- **API REST**: Endpoint para integração com outros sistemas

## 🛠️ Tecnologias Utilizadas

- **Django 5.0.4**: Framework web Python
- **Transformers (Hugging Face)**: Modelos de IA para classificação
- **NLTK**: Processamento de linguagem natural
- **Scikit-learn**: Machine learning tradicional (fallback)
- **Bootstrap 5**: Interface responsiva
- **Chart.js**: Gráficos e visualizações
- **Font Awesome**: Ícones

## 📦 Instalação

### 1. Clone o repositório
```bash
git clone <url-do-repositorio>
cd django-template
```

### 2. Ative o ambiente virtual
```bash
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate     # Windows
```

### 3. Instale as dependências
```bash
pip install -r requirements.txt
```

### 4. Execute as migrações
```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. Crie um superusuário (opcional)
```bash
python manage.py createsuperuser
```

### 6. Execute o servidor
```bash
python manage.py runserver
```

## 🧪 Testando o Sistema

### Teste via Script Python
```bash
python test_email_system.py
```

### Teste via Interface Web
1. Acesse: http://localhost:8000/email/
2. Use os exemplos pré-carregados ou insira seus próprios emails
3. Veja a classificação automática e resposta sugerida

## 📱 Como Usar

### 1. **Processar Email**
- Acesse `/email/`
- Preencha: Remetente, Assunto e Conteúdo
- Clique em "Processar com IA"
- Veja a classificação e resposta sugerida

### 2. **Ver Histórico**
- Acesse `/email/list/`
- Visualize todos os emails processados
- Use filtros por categoria e data

### 3. **Analisar Estatísticas**
- Acesse `/email/analytics/`
- Veja gráficos de distribuição
- Analise métricas de produtividade

### 4. **API REST**
```bash
POST /api/email/process/
{
    "sender": "remetente@email.com",
    "subject": "Assunto do email",
    "content": "Conteúdo do email"
}
```

## 🧠 Como Funciona a IA

### **Classificação**
1. **Pré-processamento**: Limpeza de texto, remoção de stop words
2. **Análise**: Modelo Hugging Face para classificação de sentimento
3. **Fallback**: Classificador Naive Bayes se o modelo principal falhar
4. **Confiança**: Score de confiança para cada classificação

### **Geração de Respostas**
- **Emails Produtivos**: Respostas profissionais e acionáveis
- **Emails Improdutivos**: Respostas educadas de recusa
- **Contexto**: Análise de palavras-chave para respostas personalizadas

## 📊 Exemplos de Classificação

### ✅ **Emails Produtivos**
- Reuniões de projeto
- Solicitações de clientes
- Relatórios de trabalho
- Avaliações de performance

### ❌ **Emails Improdutivos**
- Correntes de email
- Spam e promoções
- Piadas e fofocas
- Marketing não solicitado

## 🔧 Configuração Avançada

### **Variáveis de Ambiente**
```bash
# Para usar modelos Hugging Face personalizados
export HF_MODEL_NAME="seu-modelo-personalizado"
export HF_API_TOKEN="seu-token"
```

### **Personalização de Classificadores**
Edite `hello/nlp_processor.py` para:
- Ajustar thresholds de classificação
- Adicionar novas categorias
- Personalizar respostas automáticas

## 📈 Monitoramento e Analytics

- **Dashboard em Tempo Real**: Métricas de produtividade
- **Histórico Completo**: Todos os emails processados
- **Gráficos Interativos**: Distribuição por categoria
- **Insights Automáticos**: Recomendações baseadas em dados

## 🚨 Solução de Problemas

### **Erro de Dependências**
```bash
pip install --upgrade pip
pip install -r requirements.txt --force-reinstall
```

### **Erro de Modelo Hugging Face**
- O sistema automaticamente usa o classificador fallback
- Verifique sua conexão com a internet
- Considere usar um modelo local

### **Performance Lenta**
- Primeira execução pode ser lenta (download do modelo)
- Use o classificador fallback para melhor performance
- Considere cache de modelos

## 🤝 Contribuindo

1. Fork o projeto
2. Crie uma branch para sua feature
3. Commit suas mudanças
4. Push para a branch
5. Abra um Pull Request

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo LICENSE para detalhes.

## 🆘 Suporte

Para dúvidas ou problemas:
1. Verifique a documentação
2. Execute os testes: `python test_email_system.py`
3. Abra uma issue no GitHub

---

**Desenvolvido com ❤️ usando Django e IA**
