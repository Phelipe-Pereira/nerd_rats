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

## Instalação

### Windows
1. Baixe o arquivo `NerdRats.exe` da última release
2. Execute o programa
3. Na primeira execução, configure seu email e usuário do GitHub
4. O programa iniciará automaticamente com o Windows

### Linux
1. Baixe o script `install_linux.sh`
2. Dê permissão de execução:
   ```bash
   chmod +x install_linux.sh
   ```
3. Execute como root:
   ```bash
   sudo ./install_linux.sh
   ```
4. Na primeira execução, configure seu email e usuário do GitHub
5. O programa será instalado como serviço e iniciará automaticamente

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

## Configurações

As configurações são armazenadas em:
- Windows: `%APPDATA%\nerd_rats\config.conf`
- Linux: `/etc/nerd_rats.conf`

## Para Desenvolvedores

### Requisitos
- Python 3.7 ou superior
- Bibliotecas Python:
  - pynput>=1.7.6
  - requests>=2.31.0
  - python-dotenv>=1.0.0

### Gerando Executável (Windows)
1. Clone o repositório
2. Execute:
   ```bash
   python build_exe.py
   ```
3. O executável será gerado na pasta `dist`

### Variáveis de Ambiente
- `TRACKING_POST_URL`: URL para envio dos dados (padrão: http://localhost:5000/track)
- `TRACKING_INTERVAL`: Intervalo de envio em segundos (padrão: 20)
- `CONFIG_PATH`: Caminho do arquivo de configuração
