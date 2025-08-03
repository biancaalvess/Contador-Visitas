#!/usr/bin/env python3
"""
Testes básicos para a API do Contador de Visitas
"""

import requests
import json
import time
from datetime import datetime

# Configurações
BASE_URL = 'http://localhost:5000'
HEADERS = {'Content-Type': 'application/json'}

def testar_endpoint(metodo, endpoint, dados=None, params=None):
    """Testa um endpoint específico"""
    url = f"{BASE_URL}{endpoint}"
    
    try:
        print(f"🔄 Testando {metodo} {endpoint}...")
        
        if metodo == 'GET':
            response = requests.get(url, params=params)
        elif metodo == 'POST':
            response = requests.post(url, json=dados, headers=HEADERS)
        else:
            print(f"❌ Método {metodo} não suportado")
            return False
        
        print(f"   Status: {response.status_code}")
        
        if response.status_code == 200:
            try:
                data = response.json()
                print(f"   ✅ Resposta JSON válida")
                print(f"   📄 Dados: {json.dumps(data, indent=2, ensure_ascii=False)}")
                return True
            except json.JSONDecodeError:
                print(f"   ❌ Resposta não é JSON válido")
                print(f"   📄 Conteúdo: {response.text}")
                return False
        else:
            print(f"   ❌ Status code inesperado: {response.status_code}")
            print(f"   📄 Resposta: {response.text}")
            return False
            
    except requests.exceptions.ConnectionError:
        print(f"   ❌ Erro de conexão - API não está rodando?")
        return False
    except Exception as e:
        print(f"   ❌ Erro: {e}")
        return False

def executar_testes():
    """Executa todos os testes"""
    print("🧪 Iniciando testes da API do Contador de Visitas")
    print("=" * 60)
    print(f"🌐 URL Base: {BASE_URL}")
    print(f"🕒 Horário: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    testes_passaram = 0
    total_testes = 0
    
    # Lista de testes
    testes = [
        {
            'nome': 'Informações da API',
            'metodo': 'GET',
            'endpoint': '/'
        },
        {
            'nome': 'Status da API',
            'metodo': 'GET',
            'endpoint': '/api/status'
        },
        {
            'nome': 'Status da API (formato compacto)',
            'metodo': 'GET',
            'endpoint': '/api/status',
            'params': {'formato': 'compacto'}
        },
        {
            'nome': 'Total de visitas',
            'metodo': 'GET',
            'endpoint': '/api/visitas/total'
        },
        {
            'nome': 'Total de visitas (formato compacto)',
            'metodo': 'GET',
            'endpoint': '/api/visitas/total',
            'params': {'formato': 'compacto'}
        },
        {
            'nome': 'Visitas hoje',
            'metodo': 'GET',
            'endpoint': '/api/visitas/hoje'
        },
        {
            'nome': 'Registrar visita',
            'metodo': 'POST',
            'endpoint': '/api/visitas/registrar'
        },
        {
            'nome': 'Todas as visitas',
            'metodo': 'GET',
            'endpoint': '/api/visitas/todas'
        }
    ]
    
    for teste in testes:
        total_testes += 1
        print(f"📋 Teste {total_testes}: {teste['nome']}")
        
        if testar_endpoint(
            teste['metodo'], 
            teste['endpoint'], 
            teste.get('dados'),
            teste.get('params')
        ):
            testes_passaram += 1
            print("   ✅ PASSOU\n")
        else:
            print("   ❌ FALHOU\n")
        
        # Pequena pausa entre testes
        time.sleep(0.5)
    
    # Resumo
    print("=" * 60)
    print(f"📊 Resumo dos Testes:")
    print(f"   ✅ Passaram: {testes_passaram}")
    print(f"   ❌ Falharam: {total_testes - testes_passaram}")
    print(f"   📈 Taxa de sucesso: {(testes_passaram/total_testes)*100:.1f}%")
    
    if testes_passaram == total_testes:
        print("🎉 Todos os testes passaram!")
        return True
    else:
        print("⚠️  Alguns testes falharam")
        return False

def testar_performance():
    """Testa a performance da API"""
    print("\n⚡ Teste de Performance")
    print("-" * 30)
    
    # Testa múltiplas requisições
    num_requisicoes = 10
    tempos = []
    
    for i in range(num_requisicoes):
        start_time = time.time()
        response = requests.get(f"{BASE_URL}/api/visitas/total")
        end_time = time.time()
        
        tempo = (end_time - start_time) * 1000  # em milissegundos
        tempos.append(tempo)
        
        print(f"   Requisição {i+1}: {tempo:.2f}ms")
    
    # Estatísticas
    tempo_medio = sum(tempos) / len(tempos)
    tempo_min = min(tempos)
    tempo_max = max(tempos)
    
    print(f"\n📊 Estatísticas ({num_requisicoes} requisições):")
    print(f"   ⏱️  Tempo médio: {tempo_medio:.2f}ms")
    print(f"   🚀 Mais rápida: {tempo_min:.2f}ms")
    print(f"   🐌 Mais lenta: {tempo_max:.2f}ms")

if __name__ == '__main__':
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == 'performance':
        testar_performance()
    else:
        if executar_testes():
            print("\n🎯 Executando teste de performance...")
            testar_performance()
        else:
            print("\n⚠️  Pulando teste de performance devido a falhas nos testes básicos")