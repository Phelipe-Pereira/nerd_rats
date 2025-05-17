# NerdRats Event Tracker

Um programa multiplataforma que monitora eventos do computador (cliques do mouse, teclas pressionadas, distância percorrida pelo mouse e rolagens) e envia os dados periodicamente via POST.

## Estrutura do Projeto

```
nerd_rats/
├── src/
│   ├── domain/          # Entidades e regras de negócio
│   ├── infrastructure/  # Implementações de serviços
│   ├── application/     # Casos de uso
│   └── presentation/    # Interface com usuário
├── requirements.txt     # Dependências do projeto
├── install.bat         # Script de instalação para Windows
└── install.sh         # Script de instalação para Linux
```

## Requisitos

- Python 3.7 ou superior
- Bibliotecas Python (instaladas automaticamente):
  - pynput>=1.7.6
  - requests>=2.31.0
  - python-dotenv>=1.0.0

## Instalação

### Windows

1. Execute o script `install.bat` como administrador
2. O programa será instalado e configurado para iniciar com o Windows

### Linux

1. Execute o script de instalação como root:
   ```bash
   sudo ./install.sh
   ```
2. O programa será instalado como serviço systemd e iniciará automaticamente

## Configuração

- Na primeira execução, o programa solicitará:
  - Seu email
  - Seu usuário do GitHub
- As configurações são armazenadas em:
  - Windows: `%APPDATA%\nerd_rats\config.conf`
  - Linux: `/etc/nerd_rats.conf`

## Funcionalidades

### Coleta de Dados
- Monitoramento de eventos do mouse e teclado
- Coleta a cada 20 segundos
- Cache local para funcionamento offline
- Reenvio automático de dados quando online

### Formato dos Dados
O programa envia os seguintes dados para o backend:
```json
{
    "user_github": "string",    // Nome do usuário no GitHub
    "email": "string",          // Email do usuário
    "quant_clicks": number,     // Quantidade de clicks do mouse
    "quant_dist": number,       // Distância percorrida pelo mouse em cm
    "quant_scrow": number,      // Quantidade de scrolls
    "quant_keys": number        // Quantidade de teclas pressionadas
}
```

## Variáveis de Ambiente

- `TRACKING_POST_URL`: URL para envio dos dados (padrão: http://localhost:5000/track)
- `TRACKING_INTERVAL`: Intervalo de envio em segundos (padrão: 15)
- `CONFIG_PATH`: Caminho do arquivo de configuração
