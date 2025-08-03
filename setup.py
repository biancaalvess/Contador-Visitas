#!/usr/bin/env python3
"""
Script de setup para a API do Contador de Visitas
"""

import subprocess
import sys
import os
import json
from datetime import datetime

def executar_comando(comando, descricao, falha_critica=True):
    """Executa um comando do sistema"""
    print(f"🔄 {descricao}...")
    try:
        resultado = subprocess.run(comando, shell=True, capture_output=True, text=True)
        if resultado.returncode == 0:
            print(f"✅ {descricao} - Concluído")
            return True
        else:
            print(f"❌ {descricao} - Erro: {resultado.stderr}")
            if falha_critica:
                print("🛑 Falha crítica, parando setup")
                sys.exit(1)
            return False
    except Exception as e:
        print(f"❌ {descricao} - Exceção: {e}")
        if falha_critica:
            sys.exit(1)
        return False

def verificar_python():
    """Verifica se a versão do Python é adequada"""
    print("🐍 Verificando versão do Python...")
    
    versao = sys.version_info
    print(f"   Versão atual: {versao.major}.{versao.minor}.{versao.micro}")
    
    if versao.major < 3 or (versao.major == 3 and versao.minor < 7):
        print("❌ Python 3.7+ é necessário")
        sys.exit(1)
    
    print("✅ Versão do Python adequada")

def instalar_dependencias():
    """Instala as dependências Python"""
    print("📦 Instalando dependências...")
    
    if not os.path.exists('requirements.txt'):
        print("❌ Arquivo requirements.txt não encontrado")
        sys.exit(1)
    
    executar_comando(
        f"{sys.executable} -m pip install -r requirements.txt",
        "Instalando pacotes Python"
    )

def criar_arquivo_inicial():
    """Cria arquivo inicial de visitas se não existir"""
    print("📄 Configurando arquivo de dados...")
    
    if not os.path.exists('visitas.json'):
        dados_iniciais = []
        with open('visitas.json', 'w') as f:
            json.dump(dados_iniciais, f, indent=2)
        print("✅ Arquivo visitas.json criado")
    else:
        print("ℹ️  Arquivo visitas.json já existe")

def verificar_porta():
    """Verifica se a porta 5000 está disponível"""
    print("🌐 Verificando disponibilidade da porta 5000...")
    
    try:
        import socket
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            resultado = s.connect_ex(('localhost', 5000))
            if resultado == 0:
                print("⚠️  Porta 5000 já está em uso")
                print("   A API pode ter conflitos. Considere parar outros serviços.")
            else:
                print("✅ Porta 5000 disponível")
    except Exception as e:
        print(f"ℹ️  Não foi possível verificar a porta: {e}")

def criar_estrutura_diretorios():
    """Cria estrutura de diretórios necessária"""
    print("📁 Criando estrutura de diretórios...")
    
    diretorios = [
        'data',
        'logs',
        'backups'
    ]
    
    for diretorio in diretorios:
        if not os.path.exists(diretorio):
            os.makedirs(diretorio)
            print(f"   ✅ Criado: {diretorio}/")
        else:
            print(f"   ℹ️  Já existe: {diretorio}/")

def testar_api():
    """Testa se a API está funcionando"""
    print("🧪 Testando API...")
    
    print("   Iniciando servidor em background...")
    processo = subprocess.Popen([sys.executable, 'app.py'], 
                               stdout=subprocess.PIPE, 
                               stderr=subprocess.PIPE)
    
    # Aguarda um pouco para o servidor iniciar
    import time
    time.sleep(3)
    
    try:
        import requests
        response = requests.get('http://localhost:5000/', timeout=5)
        if response.status_code == 200:
            print("✅ API respondendo corretamente")
        else:
            print(f"⚠️  API retornou status {response.status_code}")
    except ImportError:
        print("ℹ️  Requests não disponível, pulando teste HTTP")
    except Exception as e:
        print(f"⚠️  Erro ao testar API: {e}")
    finally:
        # Para o processo
        processo.terminate()
        processo.wait()

def mostrar_informacoes_finais():
    """Mostra informações finais do setup"""
    print("\n" + "="*60)
    print("🎉 Setup concluído com sucesso!")
    print("="*60)
    print()
    print("📋 Próximos passos:")
    print("   1. Execute: python app.py")
    print("   2. Acesse: http://localhost:5000")
    print("   3. Teste: python test_api.py")
    print()
    print("📚 Arquivos importantes:")
    print("   • app.py - Aplicação principal")
    print("   • config.py - Configurações")
    print("   • test_api.py - Testes da API")
    print("   • backup_script.py - Backup dos dados")
    print("   • deploy.py - Script de deploy")
    print()
    print("🐳 Para usar Docker:")
    print("   docker-compose up --build")
    print()
    print("☁️  Para deploy no Heroku:")
    print("   python deploy.py")
    print()

def main():
    """Função principal do setup"""
    print("🚀 Setup da API do Contador de Visitas")
    print("="*60)
    print(f"🕒 Iniciado em: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # Executa todas as etapas
    verificar_python()
    print()
    
    instalar_dependencias()
    print()
    
    criar_estrutura_diretorios()
    print()
    
    criar_arquivo_inicial()
    print()
    
    verificar_porta()
    print()
    
    # Teste opcional
    resposta = input("🧪 Deseja testar a API agora? (s/N): ").strip().lower()
    if resposta in ['s', 'sim', 'y', 'yes']:
        testar_api()
        print()
    
    mostrar_informacoes_finais()

if __name__ == '__main__':
    main()