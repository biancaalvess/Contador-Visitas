# Contador de Visitas para Portfólio

Este projeto implementa um sistema completo de contador de visitas em tempo real para sites ou portfólios, utilizando Flask para o backend e uma interface web responsiva com atualizações automáticas.

Extensão do projeto : [Notifica-Site](https://github.com/biancaalvess/Notifica-Site)

---

##  Funcionalidades

-  **Atualização em tempo real** - Contadores atualizam automaticamente a cada 5 segundos
-  **Múltiplas estatísticas** - Total de visitas e visitas do dia atual
-  **Interface moderna** - Design responsivo com efeitos visuais
-  **Mobile-friendly** - Funciona perfeitamente em dispositivos móveis
-  **Performance** - Sistema otimizado com threads e locks para concorrência
-  **Persistência** - Dados salvos em arquivo JSON local

## Como funciona

**Backend Flask** - Servidor web completo que registra cada visita automaticamente, salvando IP, user-agent e timestamp em JSON. Possui endpoints RESTful para buscar estatísticas e registrar visitas.

**Frontend Responsivo** - Interface web moderna que se conecta automaticamente ao backend, exibe contadores formatados (1.2K, 17.4M) e atualiza em tempo real com indicadores visuais de status.

Exemplo:
            <div className="mt-12 text-center">
              <div className="inline-flex items-center gap-3 bg-background/80 backdrop-blur-sm border border-primary/30 rounded-full px-6 py-3 shadow-lg">
                <div className="w-3 h-3 rounded-full bg-blue-500 animate-pulse"></div>
                <span className="text-sm font-medium text-muted-foreground">
                  {visitorCount !== null ? `${formatarNumero(visitorCount)} visitas` : "Carregando visitas..."}
                </span>
              </div>
            </div>
          </div>



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

### Acesso
- **Interface Web**: http://localhost:5000
- **API Total**: http://localhost:5000/api/visitas/total
- **API Hoje**: http://localhost:5000/api/visitas/hoje

##  Arquitetura

### Backend Flask (`app.py`)

- **Servidor web completo** com endpoints RESTful
- **Armazenamento JSON** em `visitas.json`
- **Thread-safe** com locks para concorrência
- **Detecção de IP** considerando proxies
- **Formatação inteligente** de números (1.2K, 17.4M, etc.)

### Endpoints da API

- `GET /` - Interface web principal
- `POST /api/visitas/registrar` - Registra nova visita
- `GET /api/visitas/total` - Retorna total de visitas
- `GET /api/visitas/hoje` - Retorna visitas do dia atual
- `GET /api/visitas/todas` - Lista todas as visitas (debug)

### Funções principais

- `carregar_visitas()`: lê o arquivo JSON e retorna a lista de visitas
- `salvar_visitas(visitas)`: grava a lista de visitas no arquivo JSON
- `adicionar_visita(ip, user_agent)`: adiciona uma nova visita
- `contar_visitas_hoje()`: conta quantas visitas ocorreram hoje
- `contar_total_visitas()`: conta o total de visitas registradas
- `formatar_numero(n)`: formata números para formato compacto (K, M, G)

----------------------------------------------------------------------

# Portfolio Visitor Counter

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

