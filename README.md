# Contador de Visitas para Portfólio

Este projeto implementa um sistema simples de contador de visitas para um site ou portfólio, utilizando Python para backend (armazenando visitas em arquivo JSON) e React para frontend, exibindo o número formatado e estilizado de visitas.

Extensão do projeto : [Notifica-Site](https://github.com/biancaalvess/Notifica-Site)

---

## Como funciona

Backend - Um script Python registra cada visita, salvando informações como o IP, user-agent e horário em um arquivo JSON. Ele também tem funções para contar quantas visitas aconteceram no dia atual e para formatar esse número de forma compacta (tipo 1.2K para 1.200).

Frontend - No React, o número de visitas é buscado via uma chamada para o backend (um endpoint que retorna o total de visitas do dia). Enquanto carrega, o componente mostra uma mensagem, e depois exibe o número formatado dentro de uma caixa estilizada, com uma bolinha animada para dar aquele toque de vida.

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



## Backend (Python)

### Arquivo principal: `contador_visitas.py`

- Armazena as visitas em um arquivo JSON chamado `visitas.json`.
- Utiliza travas (`Lock`) para evitar problemas de concorrência ao acessar o arquivo.
- Registra IP, User-Agent e horário da visita.
- Permite contar as visitas feitas no dia atual.
- Possui função para formatar o número de visitas em formato compacto (ex: 1.2K, 17.4M).

### Funções principais

- `carregar_visitas()`: lê o arquivo JSON e retorna a lista de visitas.
- `salvar_visitas(visitas)`: grava a lista de visitas no arquivo JSON.
- `adicionar_visita(ip, user_agent)`: adiciona uma nova visita.
- `contar_visitas_hoje()`: conta quantas visitas ocorreram hoje.
- `formatar_numero(n)`: formata um número inteiro para formato compacto com sufixos (K, M, G).

### Exemplo de uso:

```python
visitas_hoje = contar_visitas_hoje()
print(formatar_numero(visitas_hoje))  # Exemplo: "1.2K"

-

# Portfolio Visitor Counter

This project implements a simple visitor counter system for a website or portfolio, using Python for the backend (storing visits in a JSON file) and React for the frontend, displaying the formatted and stylized number of visits.

Project extension: [Notifica-Site](https://github.com/biancaalvess/Notifica-Site)

---

## How it works

Backend - A Python script records each visit, saving information such as the IP, user-agent and time in a JSON file. It also has functions to count how many visits happened on the current day and to format this number in a compact way (like 1.2K to 1,200).

Frontend - In React, the number of visits is fetched via a call to the backend (an endpoint that returns the total number of visits for the day). While loading, the component displays a message, and then displays the formatted number inside a stylized box, with an animated dot to give it a touch of life.

Example:
<div className="mt-12 text-center">
<div className="inline-flex items-center gap-3 bg-background/80 backdrop-blur-sm border border-primary/30 rounded-full px-6 py-3 shadow-lg">
<div className="w-3 h-3 rounded-full bg-blue-500 animate-pulse"></div>
<span className="text-sm font-medium text-muted-foreground">
{visitorCount !== null ? `${formatarNumero(visitorCount)} visita` : "Loading visits..."}
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

### Usage example:

```python
visits_today = count_visits_today()
print(format_number(visits_today)) # Example: "1.2K"