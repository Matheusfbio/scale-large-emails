#!/usr/bin/env python3
"""
Configurações do Sistema de Classificação de Emails
"""

import os
from pathlib import Path

# Configurações do Django
DJANGO_SETTINGS_MODULE = 'web_django.settings'

# Configurações do Modelo de IA
HUGGING_FACE_MODEL = "nlptown/bert-base-multilingual-uncased-sentiment"
MODEL_MAX_LENGTH = 512  # Máximo de tokens para o modelo

# Configurações de Classificação
PRODUCTIVE_KEYWORDS = [
    'reunião', 'meeting', 'projeto', 'project', 'cliente', 'client',
    'trabalho', 'work', 'relatório', 'report', 'deadline', 'entrega',
    'solicitação', 'request', 'contrato', 'contract', 'avaliação',
    'performance', 'sprint', 'agenda', 'urgente', 'importante',
    'desenvolvimento', 'development', 'sistema', 'system', 'aplicação',
    'application', 'banco de dados', 'database', 'api', 'interface'
]

UNPRODUCTIVE_KEYWORDS = [
    'corrente', 'chain', 'reencaminhar', 'forward', 'spam', 'promoção',
    'desconto', 'discount', 'piada', 'joke', 'fofoca', 'gossip',
    'marketing', 'newsletter', 'propaganda', 'advertisement', 'loteria',
    'lottery', 'sorte', 'luck', 'reencaminhe', 'forward this',
    'boa sorte', 'good luck', 'imperdível', 'unmissable'
]

# Configurações de Resposta
PRODUCTIVE_RESPONSES = [
    "Obrigado pelo email. Vou analisar e retornar em breve.",
    "Recebi sua mensagem. Estou trabalhando nisso e te mantenho informado.",
    "Perfeito! Vou dar a atenção necessária a este assunto.",
    "Excelente iniciativa. Vamos agendar uma reunião para discutir os detalhes.",
    "Muito bem! Estou processando as informações e retorno em seguida.",
    "Entendido! Vou priorizar este atendimento.",
    "Perfeito! Vou revisar e te envio um status atualizado.",
    "Excelente! Vamos trabalhar nisso juntos."
]

UNPRODUCTIVE_RESPONSES = [
    "Obrigado, mas não posso participar de correntes de email.",
    "Agradeço o envio, mas não estou interessado neste tipo de conteúdo.",
    "Vou remover meu email desta lista de distribuição.",
    "Por favor, não me inclua em futuras correntes de email.",
    "Obrigado, mas não posso ajudar com este tipo de solicitação.",
    "Não participo de correntes de email.",
    "Não estou interessado em promoções."
]

# Configurações de Threshold
MIN_CONFIDENCE_THRESHOLD = 0.3
KEYWORD_BOOST_FACTOR = 0.1
MAX_KEYWORD_CONFIDENCE = 0.8

# Configurações de API
API_RATE_LIMIT = 100  # Requisições por hora
API_TIMEOUT = 30  # Segundos

# Configurações de Log
LOG_LEVEL = "INFO"
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

# Configurações de Cache
CACHE_TTL = 3600  # 1 hora em segundos
MODEL_CACHE_KEY = "email_classifier_model"

# Configurações de Monitoramento
METRICS_ENABLED = True
PERFORMANCE_TRACKING = True

# Configurações de Desenvolvimento
DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'
DEVELOPMENT_MODE = os.getenv('DEVELOPMENT_MODE', 'False').lower() == 'true'

# Configurações de Segurança
CSRF_ENABLED = True
API_KEY_REQUIRED = False  # Para uso interno
MAX_EMAIL_LENGTH = 10000  # Máximo de caracteres por email

# Configurações de Backup
BACKUP_ENABLED = True
BACKUP_FREQUENCY = "daily"  # daily, weekly, monthly
BACKUP_RETENTION_DAYS = 30

def get_config():
    """Retorna todas as configurações como dicionário"""
    return {
        'django_settings': DJANGO_SETTINGS_MODULE,
        'model': HUGGING_FACE_MODEL,
        'max_length': MODEL_MAX_LENGTH,
        'productive_keywords': PRODUCTIVE_KEYWORDS,
        'unproductive_keywords': UNPRODUCTIVE_KEYWORDS,
        'productive_responses': PRODUCTIVE_RESPONSES,
        'unproductive_responses': UNPRODUCTIVE_RESPONSES,
        'min_confidence': MIN_CONFIDENCE_THRESHOLD,
        'keyword_boost': KEYWORD_BOOST_FACTOR,
        'max_keyword_confidence': MAX_KEYWORD_CONFIDENCE,
        'api_rate_limit': API_RATE_LIMIT,
        'api_timeout': API_TIMEOUT,
        'log_level': LOG_LEVEL,
        'log_format': LOG_FORMAT,
        'cache_ttl': CACHE_TTL,
        'model_cache_key': MODEL_CACHE_KEY,
        'metrics_enabled': METRICS_ENABLED,
        'performance_tracking': PERFORMANCE_TRACKING,
        'debug': DEBUG,
        'development_mode': DEVELOPMENT_MODE,
        'csrf_enabled': CSRF_ENABLED,
        'api_key_required': API_KEY_REQUIRED,
        'max_email_length': MAX_EMAIL_LENGTH,
        'backup_enabled': BACKUP_ENABLED,
        'backup_frequency': BACKUP_FREQUENCY,
        'backup_retention_days': BACKUP_RETENTION_DAYS
    }

def print_config():
    """Imprime as configurações atuais"""
    config = get_config()
    print("⚙️  Configurações do Sistema de Emails")
    print("=" * 50)
    
    for key, value in config.items():
        if isinstance(value, list):
            print(f"{key}: {len(value)} itens")
        else:
            print(f"{key}: {value}")
    
    print("=" * 50)

if __name__ == "__main__":
    print_config()
