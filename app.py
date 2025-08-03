import json
from datetime import datetime
from threading import Lock
from flask import Flask, jsonify, request, render_template_string
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


# Template HTML para a página principal
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Contador de Visitas em Tempo Real</title>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            margin: 0;
            display: flex;
            justify-content: center;
            align-items: center;
            color: white;
        }
        
        .container {
            text-align: center;
            background: rgba(255, 255, 255, 0.1);
            backdrop-filter: blur(10px);
            border-radius: 20px;
            padding: 40px;
            box-shadow: 0 8px 32px rgba(31, 38, 135, 0.37);
            border: 1px solid rgba(255, 255, 255, 0.18);
            min-width: 300px;
        }
        
        .title {
            font-size: 2.5rem;
            margin-bottom: 20px;
            font-weight: 300;
        }
        
        .counter-box {
            background: rgba(255, 255, 255, 0.2);
            border-radius: 15px;
            padding: 30px;
            margin: 20px 0;
            backdrop-filter: blur(5px);
            border: 1px solid rgba(255, 255, 255, 0.2);
        }
        
        .counter-label {
            font-size: 1rem;
            opacity: 0.8;
            margin-bottom: 10px;
        }
        
        .counter-value {
            font-size: 3rem;
            font-weight: bold;
            margin: 10px 0;
            text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);
        }
        
        .status-indicator {
            display: inline-flex;
            align-items: center;
            gap: 8px;
            margin-top: 15px;
            font-size: 0.9rem;
            opacity: 0.8;
        }
        
        .pulse-dot {
            width: 8px;
            height: 8px;
            border-radius: 50%;
            background: #4ade80;
            animation: pulse 2s infinite;
        }
        
        @keyframes pulse {
            0%, 100% { opacity: 1; transform: scale(1); }
            50% { opacity: 0.7; transform: scale(1.1); }
        }
        
        .loading {
            color: #fbbf24;
        }
        
        .error {
            color: #ef4444;
        }
        
        .refresh-btn {
            background: rgba(255, 255, 255, 0.2);
            border: 1px solid rgba(255, 255, 255, 0.3);
            color: white;
            padding: 10px 20px;
            border-radius: 10px;
            cursor: pointer;
            font-size: 0.9rem;
            margin-top: 20px;
            transition: all 0.3s ease;
        }
        
        .refresh-btn:hover {
            background: rgba(255, 255, 255, 0.3);
            transform: translateY(-2px);
        }
        
        .stats-grid {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 15px;
            margin-top: 20px;
        }
        
        .stat-item {
            background: rgba(255, 255, 255, 0.1);
            padding: 15px;
            border-radius: 10px;
            border: 1px solid rgba(255, 255, 255, 0.2);
        }
        
        .stat-value {
            font-size: 1.5rem;
            font-weight: bold;
        }
        
        .stat-label {
            font-size: 0.8rem;
            opacity: 0.7;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1 class="title">Contador de Visitas</h1>
        
        <div class="counter-box">
            <div class="counter-label">Total de Visitas</div>
            <div class="counter-value" id="totalCounter">Carregando...</div>
            <div class="status-indicator">
                <div class="pulse-dot"></div>
                <span id="status">Atualizando em tempo real</span>
            </div>
        </div>
        
        <div class="stats-grid">
            <div class="stat-item">
                <div class="stat-value" id="todayCounter">-</div>
                <div class="stat-label">Hoje</div>
            </div>
            <div class="stat-item">
                <div class="stat-value" id="lastUpdate">-</div>
                <div class="stat-label">Última atualização</div>
            </div>
        </div>
        
        <button class="refresh-btn" onclick="atualizarContadores()">Atualizar Agora</button>
    </div>

    <script>
        let intervalId;
        
        async function atualizarContadores() {
            try {
                // Atualiza o status
                document.getElementById('status').textContent = 'Carregando...';
                document.getElementById('status').className = 'loading';
                
                // Busca o total de visitas
                const responseTotal = await fetch('/api/visitas/total');
                const dataTotal = await responseTotal.json();
                
                // Busca as visitas de hoje
                const responseHoje = await fetch('/api/visitas/hoje');
                const dataHoje = await responseHoje.json();
                
                // Atualiza os contadores
                document.getElementById('totalCounter').textContent = dataTotal.visitas_formatadas;
                document.getElementById('todayCounter').textContent = dataHoje.visitas_formatadas;
                document.getElementById('lastUpdate').textContent = new Date().toLocaleTimeString('pt-BR');
                
                // Atualiza o status
                document.getElementById('status').textContent = 'Conectado - Tempo real';
                document.getElementById('status').className = '';
                
            } catch (error) {
                console.error('Erro ao atualizar contadores:', error);
                document.getElementById('status').textContent = 'Erro de conexão';
                document.getElementById('status').className = 'error';
            }
        }
        
        async function registrarVisita() {
            try {
                await fetch('/api/visitas/registrar', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    }
                });
            } catch (error) {
                console.error('Erro ao registrar visita:', error);
            }
        }
        
        // Registra a visita quando a página carrega
        document.addEventListener('DOMContentLoaded', async () => {
            await registrarVisita();
            await atualizarContadores();
            
            // Atualiza a cada 5 segundos
            intervalId = setInterval(atualizarContadores, 5000);
        });
        
        // Limpa o intervalo quando a página é fechada
        window.addEventListener('beforeunload', () => {
            if (intervalId) {
                clearInterval(intervalId);
            }
        });
    </script>
</body>
</html>
"""

# Rotas da API


@app.route('/')
def home():
    """Página principal com contador em tempo real"""
    return render_template_string(HTML_TEMPLATE)


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
        return jsonify({
            'total': total,
            'visitas_formatadas': formatar_numero(total)
        })
    except Exception as e:
        return jsonify({
            'erro': str(e)
        }), 500


@app.route('/api/visitas/hoje')
def obter_visitas_hoje():
    """Retorna as visitas de hoje"""
    try:
        hoje = contar_visitas_hoje()
        return jsonify({
            'hoje': hoje,
            'visitas_formatadas': formatar_numero(hoje),
            'data': datetime.now().strftime('%Y-%m-%d')
        })
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


# Executa o servidor Flask
if __name__ == '__main__':
    print("🚀 Iniciando servidor do contador de visitas...")
    print("📊 Acesse: http://localhost:5000")
    print("🔄 Atualizações em tempo real ativadas!")
    app.run(debug=True, host='0.0.0.0', port=5000)
