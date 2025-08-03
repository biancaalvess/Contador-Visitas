"""
Configurações da API do Contador de Visitas
"""

import os

# Configurações do arquivo de dados
ARQUIVO_VISITAS = os.getenv('ARQUIVO_VISITAS', 'visitas.json')

# Configurações do servidor
HOST = os.getenv('HOST', '0.0.0.0')
PORT = int(os.getenv('PORT', 5000))
DEBUG = os.getenv('DEBUG', 'True').lower() == 'true'

# Configurações da API
API_VERSION = '1.0.0'
API_NAME = 'API Contador de Visitas'
API_DESCRIPTION = 'API para contagem e registro de visitas'

# Configurações de formato padrão
FORMATO_PADRAO = os.getenv('FORMATO_PADRAO', 'real')  # 'real' ou 'compacto'

# Configurações de CORS
CORS_ORIGINS = os.getenv('CORS_ORIGINS', '*')

# Configurações de backup automático
BACKUP_AUTOMATICO = os.getenv('BACKUP_AUTOMATICO', 'False').lower() == 'true'
BACKUP_INTERVALO_HORAS = int(os.getenv('BACKUP_INTERVALO_HORAS', 24))

# Configurações de log
LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
LOG_FILE = os.getenv('LOG_FILE', 'api.log')

# Configurações de rate limiting (futuro)
RATE_LIMIT_ENABLED = os.getenv('RATE_LIMIT_ENABLED', 'False').lower() == 'true'
RATE_LIMIT_PER_MINUTE = int(os.getenv('RATE_LIMIT_PER_MINUTE', 60))