# API Contador de Visitas

API RESTful para contagem e registro de visitas, ideal para integração em portfólios, websites e aplicações que necessitam de monitoramento de visitantes.

Extensão do projeto : [Notifica-Site](https://github.com/biancaalvess/Notifica-Site)

---

##  Funcionalidades

-  **API RESTful** - Endpoints organizados e documentados
-  **Múltiplas estatísticas** - Total de visitas e visitas do dia atual
-  **Thread-safe** - Sistema seguro para múltiplos acessos simultâneos
-  **Performance** - Otimizado com locks para concorrência
-  **Persistência JSON** - Dados salvos localmente em formato JSON
-  **CORS habilitado** - Permite integração com qualquer frontend
-  **Formatação inteligente** - Números compactos (1.2K, 17.4M, etc.)

## Como funciona

**API Flask** - Servidor web que fornece endpoints para registrar visitas e obter estatísticas. Salva automaticamente IP, user-agent e timestamp de cada visita em arquivo JSON.

**Integração flexível** - Pode ser consumida por qualquer frontend (React, Vue, Angular, vanilla JS) ou aplicação que precise de contagem de visitas.

##  Exemplos de uso

### JavaScript Frontend
```javascript
// Registrar uma visita
await fetch('http://localhost:5000/api/visitas/registrar', {
    method: 'POST'
});

// Obter total de visitas (número real)
const response = await fetch('http://localhost:5000/api/visitas/total');
const data = await response.json();
console.log(`Total: ${data.visitas}`); // Ex: "1234567"

// Obter total de visitas (formato compacto)
const responseCompacto = await fetch('http://localhost:5000/api/visitas/total?formato=compacto');
const dataCompacto = await responseCompacto.json();
console.log(`Total: ${dataCompacto.visitas}`); // Ex: "1.2M"
```

### React Hook
```jsx
const [visitas, setVisitas] = useState(null);
const [formato, setFormato] = useState('real'); // 'real' ou 'compacto'

useEffect(() => {
    fetch(`/api/visitas/total?formato=${formato}`)
        .then(res => res.json())
        .then(data => setVisitas(data.visitas));
}, [formato]);
```



##  Instalação e Uso

### Pré-requisitos
- Python 3.7+
- pip (gerenciador de pacotes Python)

### Instalação
```bash
# Clone o repositório
git clone <url-do-repositorio>
cd Contador-Visitas

# Instale as dependências
pip install -r requirements.txt

# Execute o servidor
python app.py
```

### Endpoints da API
- **Info da API**: `GET /` - Informações gerais da API
- **Registrar visita**: `POST /api/visitas/registrar` - Registra nova visita
- **Total de visitas**: `GET /api/visitas/total` - Retorna total (real ou formatado)
- **Visitas hoje**: `GET /api/visitas/hoje` - Retorna visitas do dia (real ou formatado)
- **Todas as visitas**: `GET /api/visitas/todas` - Lista completa (debug)
- **Status da API**: `GET /api/status` - Status e estatísticas gerais

### Parâmetro de Formato
Todos os endpoints que retornam números suportam o parâmetro `formato`:

| Parâmetro | Descrição | Exemplo |
|-----------|-----------|---------|
| `?formato=real` | Número real completo | `1234567` |
| `?formato=compacto` | Número formatado | `1.2M` |

**Padrão**: `real` (sempre retorna número completo se não especificado)

##  Arquitetura

### Backend Flask (`app.py`)

- **Servidor web completo** com endpoints RESTful
- **Armazenamento JSON** em `visitas.json`
- **Thread-safe** com locks para concorrência
- **Detecção de IP** considerando proxies
- **Formatação inteligente** de números (1.2K, 17.4M, etc.)

### Endpoints disponíveis

- `GET /` - Informações da API
- `POST /api/visitas/registrar` - Registra nova visita
- `GET /api/visitas/total` - Retorna total de visitas
- `GET /api/visitas/hoje` - Retorna visitas do dia atual
- `GET /api/visitas/todas` - Lista todas as visitas (debug)
- `GET /api/status` - Status e estatísticas da API

### Funções principais

- `carregar_visitas()`: lê o arquivo JSON e retorna a lista de visitas
- `salvar_visitas(visitas)`: grava a lista de visitas no arquivo JSON
- `adicionar_visita(ip, user_agent)`: adiciona uma nova visita
- `contar_visitas_hoje()`: conta quantas visitas ocorreram hoje
- `contar_total_visitas()`: conta o total de visitas registradas
- `formatar_numero(n)`: formata números para formato compacto (K, M, G)

----------------------------------------------------------------------

# Visitor Counter

This project implements a simple visitor counter system for a website or portfolio, using Python for the backend (storing visits in a JSON file) and React for the frontend, displaying the formatted and stylized number of visits.

Project extension: [Notifica-Site](https://github.com/biancaalvess/Notifica-Site)



## How it works

Backend - A Python script records each visit, saving information such as the IP, user-agent and time in a JSON file. It also has functions to count how many visits happened on the current day and to format this number in a compact way (like 1.2K to 1,200).

Frontend - In React, the number of visits is fetched via a call to the backend (an endpoint that returns the total number of visits for the day). While loading, the component displays a message, and then displays the formatted number inside a stylized box, with an animated dot to give it a touch of life.

Example:
            <div className="mt-12 text-center">
              <div className="inline-flex items-center gap-3 bg-background/80 backdrop-blur-sm border border-primary/30 rounded-full px-6 py-3 shadow-lg">
                <div className="w-3 h-3 rounded-full bg-blue-500 animate-pulse"></div>
                <span className="text-sm font-medium text-muted-foreground">
                  {visitorCount !== null ? `${formatarNumero(visitorCount)} visitas` : "Carregando visitas..."}
                </span>
              </div>
            </div>
          </div>



## Backend (Python)

### Main file: `contador_visitas.py`

- Stores visits in a JSON file called `visitas.json`.
- Uses locks (`Lock`) to avoid concurrency issues when accessing the file.
- Records IP, User-Agent and time of visit.
- Allows you to count visits made on the current day.
- Has a function to format the number of visits in a compact format (e.g.: 1.2K, 17.4M).

### Main functions

- `carrar_visitas()`: reads the JSON file and returns the list of visits.
- `salvar_visitas(visitas)`: saves the list of visits in the JSON file.
- `add_visit(ip, user_agent)`: adds a new visit.
- `count_visits_today()`: counts how many visits occurred today.
- `format_number(n)`: formats an integer to a compact format with suffixes (K, M, G).

