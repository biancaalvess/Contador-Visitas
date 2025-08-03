import json
from datetime import datetime
from threading import Lock
from flask import Flask, jsonify, request
from flask_cors import CORS

# Inicializa a aplicação Flask
app = Flask(__name__)
CORS(app)  # Permite requisições de outras origens

# Nome do arquivo onde as visitas serão armazenadas em formato JSON
ARQUIVO = 'visitas.json'

# Trava para evitar problemas de acesso concorrente ao arquivo
bloqueio = Lock()


def carregar_visitas():
    """
    Carrega a lista de visitas do arquivo JSON.
    Retorna uma lista vazia se o arquivo não existir.
    """
    try:
        with open(ARQUIVO, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return []


def salvar_visitas(visitas):
    """
    Salva a lista de visitas no arquivo JSON,
    formatando o arquivo com indentação para melhor leitura.
    """
    with open(ARQUIVO, 'w') as f:
        json.dump(visitas, f, indent=2)


def adicionar_visita(ip, user_agent):
    """
    Adiciona uma nova visita com IP e user agent,
    registrando a data e hora atual no formato ISO.
    A operação é protegida com um bloqueio para evitar
    acessos simultâneos conflitantes.
    """
    with bloqueio:
        visitas = carregar_visitas()
        visitas.append({
            'tempo': datetime.now().isoformat(),
            'ip': ip,
            'user_agent': user_agent
        })
        salvar_visitas(visitas)


def contar_visitas_hoje():
    """
    Conta quantas visitas foram feitas no dia atual,
    comparando a data da visita com a data atual.
    """
    with bloqueio:
        visitas = carregar_visitas()
        hoje = datetime.now().date()
        return sum(1 for v in visitas if datetime.fromisoformat(v['tempo']).date() == hoje)


def contar_total_visitas():
    """
    Conta o total de visitas registradas.
    """
    with bloqueio:
        visitas = carregar_visitas()
        return len(visitas)


def formatar_numero(n):
    """
    Formata um número inteiro para uma string compacta,
    usando sufixos K (mil), M (milhão) e G (bilhão).
    Exemplos:
    999 -> '999'
    1_234 -> '1.2K'
    17_486_444 -> '17.4M'
    """
    if n < 1000:
        return str(n)
    elif n < 1_000_000:
        return f"{n/1000:.1f}K"
    elif n < 1_000_000_000:
        return f"{n/1_000_000:.1f}M"
    else:
        return f"{n/1_000_000_000:.1f}G"


# Rotas da API


@app.route('/')
def info_api():
    """Informações da API"""
    return jsonify({
        'nome': 'API Contador de Visitas',
        'versao': '1.0.0',
        'descricao': 'API para contagem e registro de visitas',
        'endpoints': {
            'POST /api/visitas/registrar': 'Registra uma nova visita',
            'GET /api/visitas/total': 'Retorna total de visitas',
            'GET /api/visitas/hoje': 'Retorna visitas do dia atual',
            'GET /api/visitas/todas': 'Lista todas as visitas',
            'GET /api/status': 'Status da API'
        },
        'parametros': {
            'formato': {
                'descricao': 'Formato de exibição dos números',
                'valores': ['real', 'compacto'],
                'padrao': 'real',
                'exemplos': {
                    'real': '1234567',
                    'compacto': '1.2M'
                }
            }
        },
        'exemplos_uso': {
            'numero_real': '/api/visitas/total?formato=real',
            'numero_compacto': '/api/visitas/total?formato=compacto'
        },
        'status': 'online'
    })


@app.route('/api/visitas/registrar', methods=['POST'])
def registrar_visita():
    """Registra uma nova visita"""
    try:
        # Obtém o IP do cliente (considerando proxies)
        if request.headers.get('X-Forwarded-For'):
            ip = request.headers.get('X-Forwarded-For').split(',')[0].strip()
        else:
            ip = request.remote_addr

        # Obtém o User-Agent
        user_agent = request.headers.get('User-Agent', 'Desconhecido')

        # Registra a visita
        adicionar_visita(ip, user_agent)

        return jsonify({
            'sucesso': True,
            'mensagem': 'Visita registrada com sucesso',
            'ip': ip
        })
    except Exception as e:
        return jsonify({
            'sucesso': False,
            'erro': str(e)
        }), 500


@app.route('/api/visitas/total')
def obter_total_visitas():
    """Retorna o total de visitas"""
    try:
        total = contar_total_visitas()
        # Verifica se deve formatar ou não
        formato = request.args.get('formato', 'real')  # 'real' ou 'compacto'

        response = {
            'total': total,
            'formato': formato
        }

        if formato == 'compacto':
            response['visitas'] = formatar_numero(total)
        else:
            response['visitas'] = str(total)

        return jsonify(response)
    except Exception as e:
        return jsonify({
            'erro': str(e)
        }), 500


@app.route('/api/visitas/hoje')
def obter_visitas_hoje():
    """Retorna as visitas de hoje"""
    try:
        hoje = contar_visitas_hoje()
        # Verifica se deve formatar ou não
        formato = request.args.get('formato', 'real')  # 'real' ou 'compacto'

        response = {
            'hoje': hoje,
            'data': datetime.now().strftime('%Y-%m-%d'),
            'formato': formato
        }

        if formato == 'compacto':
            response['visitas'] = formatar_numero(hoje)
        else:
            response['visitas'] = str(hoje)

        return jsonify(response)
    except Exception as e:
        return jsonify({
            'erro': str(e)
        }), 500


@app.route('/api/visitas/todas')
def obter_todas_visitas():
    """Retorna todas as visitas (para debugging)"""
    try:
        visitas = carregar_visitas()
        return jsonify({
            'visitas': visitas,
            'total': len(visitas)
        })
    except Exception as e:
        return jsonify({
            'erro': str(e)
        }), 500


@app.route('/api/status')
def status_api():
    """Status da API"""
    try:
        total = contar_total_visitas()
        hoje = contar_visitas_hoje()
        formato = request.args.get('formato', 'real')  # 'real' ou 'compacto'

        response = {
            'status': 'online',
            'timestamp': datetime.now().isoformat(),
            'formato': formato,
            'estatisticas': {
                'total_visitas': total,
                'visitas_hoje': hoje
            }
        }

        # Adiciona formatação baseada no parâmetro
        if formato == 'compacto':
            response['estatisticas']['total_exibicao'] = formatar_numero(total)
            response['estatisticas']['hoje_exibicao'] = formatar_numero(hoje)
        else:
            response['estatisticas']['total_exibicao'] = str(total)
            response['estatisticas']['hoje_exibicao'] = str(hoje)

        return jsonify(response)
    except Exception as e:
        return jsonify({
            'status': 'erro',
            'erro': str(e)
        }), 500


# Executa o servidor Flask
if __name__ == '__main__':
    import os
    
    # Configurações para deploy
    port = int(os.environ.get('PORT', 5000))
    host = os.environ.get('HOST', '0.0.0.0')
    debug = os.environ.get('DEBUG', 'True').lower() == 'true'
    
    print(" Iniciando API do contador de visitas...")
    print(" Endpoints disponíveis:")
    print("   - GET  / (info da API)")
    print("   - POST /api/visitas/registrar")
    print("   - GET  /api/visitas/total")
    print("   - GET  /api/visitas/hoje")
    print("   - GET  /api/visitas/todas")
    print("   - GET  /api/status")
    print(f" API rodando em: http://{host}:{port}")
    
    app.run(debug=debug, host=host, port=port)
