import json
from datetime import datetime
from threading import Lock

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

# Exemplo de uso:
visitas_hoje = contar_visitas_hoje()
print(formatar_numero(visitas_hoje))


