# Exemplos de Respostas da API

## GET / (Informações da API)
```json
{
  "nome": "API Contador de Visitas",
  "versao": "1.0.0",
  "descricao": "API para contagem e registro de visitas",
  "endpoints": {
    "POST /api/visitas/registrar": "Registra uma nova visita",
    "GET /api/visitas/total": "Retorna total de visitas",
    "GET /api/visitas/hoje": "Retorna visitas do dia atual",
    "GET /api/visitas/todas": "Lista todas as visitas",
    "GET /api/status": "Status da API"
  },
  "parametros": {
    "formato": {
      "descricao": "Formato de exibição dos números",
      "valores": ["real", "compacto"],
      "padrao": "real",
      "exemplos": {
        "real": "1234567",
        "compacto": "1.2M"
      }
    }
  },
  "exemplos_uso": {
    "numero_real": "/api/visitas/total?formato=real",
    "numero_compacto": "/api/visitas/total?formato=compacto"
  },
  "status": "online"
}
```

## POST /api/visitas/registrar
```json
{
  "sucesso": true,
  "mensagem": "Visita registrada com sucesso",
  "ip": "192.168.1.100"
}
```

## GET /api/visitas/total (formato=real)
```json
{
  "total": 1234567,
  "formato": "real",
  "visitas": "1234567"
}
```

## GET /api/visitas/total?formato=compacto
```json
{
  "total": 1234567,
  "formato": "compacto",
  "visitas": "1.2M"
}
```

## GET /api/visitas/hoje
```json
{
  "hoje": 42,
  "data": "2025-08-03",
  "formato": "real",
  "visitas": "42"
}
```

## GET /api/status
```json
{
  "status": "online",
  "timestamp": "2025-08-03T10:30:45.123456",
  "formato": "real",
  "estatisticas": {
    "total_visitas": 1234567,
    "visitas_hoje": 42,
    "total_exibicao": "1234567",
    "hoje_exibicao": "42"
  }
}
```

## GET /api/visitas/todas
```json
{
  "visitas": [
    {
      "tempo": "2025-08-03T01:14:05.272508",
      "ip": "127.0.0.1",
      "user_agent": "Mozilla/5.0..."
    },
    {
      "tempo": "2025-08-03T02:30:12.456789",
      "ip": "192.168.1.100",
      "user_agent": "Mozilla/5.0..."
    }
  ],
  "total": 2
}
```