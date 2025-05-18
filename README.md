# NerdRats Event Tracker 🐀

[![Windows](https://img.shields.io/badge/Windows-0078D6?style=for-the-badge&logo=windows&logoColor=white)](https://github.com/seu-usuario/nerd_rats/releases)
[![Linux](https://img.shields.io/badge/Linux-FCC624?style=for-the-badge&logo=linux&logoColor=black)](https://github.com/seu-usuario/nerd_rats/releases)
[![Python](https://img.shields.io/badge/Python-3.7+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)

Um programa multiplataforma que monitora eventos do computador (cliques do mouse, teclas pressionadas, distância percorrida pelo mouse e rolagens) e envia os dados periodicamente via POST para análise de produtividade.

## ✨ Funcionalidades

- 🖱️ **Monitoramento de Mouse**
  - Contagem de cliques
  - Distância percorrida (em cm)
  - Número de rolagens (scroll)
- ⌨️ **Monitoramento de Teclado**
  - Contagem de teclas pressionadas
- 🔄 **Sincronização**
  - Envio automático a cada 20 segundos
  - Cache local para funcionamento offline
  - Reenvio automático quando online
- 📊 **Logs e Métricas**
  - Logs detalhados das atividades
  - Métricas em tempo real
  - Histórico de envios

## 🚀 Instalação

### Windows

1. Baixe o arquivo `NerdRats.exe` da [última release](https://github.com/seu-usuario/nerd_rats/releases)
2. Execute o programa como administrador
3. Na primeira execução:
   - Configure seu email
   - Configure seu usuário do GitHub
4. O programa iniciará automaticamente com o Windows

### Linux

1. Baixe o script `install_linux.sh`
2. Abra o terminal e navegue até a pasta do download
3. Dê permissão de execução:
   ```bash
   chmod +x install_linux.sh
   ```
4. Execute como root:
   ```bash
   sudo ./install_linux.sh
   ```
5. Configure seu email e usuário do GitHub quando solicitado

## 📁 Estrutura do Projeto

```
nerd_rats/
├── src/
│   ├── domain/          # Entidades e regras de negócio
│   ├── infrastructure/  # Implementações de serviços
│   │   ├── config/     # Configurações do sistema
│   │   ├── services/   # Serviços de monitoramento
│   │   └── logs/       # Sistema de logs
│   ├── application/     # Casos de uso
│   └── presentation/    # Interface com usuário
├── requirements.txt     # Dependências do projeto
├── install.bat         # Script de instalação para Windows
└── install.sh         # Script de instalação para Linux
```

## 📊 Formato dos Dados

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

## ⚙️ Configurações

### Localização dos Arquivos

- **Windows**:
  - Configurações: `%APPDATA%\nerd_rats\config.ini`
  - Logs: `%APPDATA%\nerd_rats\logs\`
  - Cache: `%APPDATA%\nerd_rats\cache\`

- **Linux**:
  - Configurações: `/etc/nerd_rats.conf`
  - Logs: `/var/log/nerd_rats/`
  - Cache: `/var/cache/nerd_rats/`

### Variáveis de Ambiente

| Variável | Descrição | Padrão |
|----------|-----------|---------|
| `TRACKING_POST_URL` | URL para envio dos dados | https://nerds-rats-hackathon.onrender.com/metrics |
| `TRACKING_INTERVAL` | Intervalo de envio (segundos) | 20 |
| `LOG_LEVEL` | Nível de log (DEBUG, INFO, WARNING, ERROR) | INFO |
| `LOG_RETENTION_DAYS` | Dias para manter logs | 30 |

## 🛠️ Para Desenvolvedores

### Requisitos

- Python 3.7 ou superior
- pip (gerenciador de pacotes Python)

### Dependências Principais

```txt
pynput>=1.7.6      # Monitoramento de mouse e teclado
requests>=2.31.0   # Requisições HTTP
python-dotenv>=1.0.0   # Gerenciamento de variáveis de ambiente
```

### Instalação para Desenvolvimento

1. Clone o repositório:
   ```bash
   git clone https://github.com/seu-usuario/nerd_rats.git
   cd nerd_rats
   ```

2. Crie um ambiente virtual:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux
   .\venv\Scripts\activate   # Windows
   ```

3. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```

### Gerando Executável

#### Windows
```bash
python build_exe.py
```
O executável será gerado na pasta `dist`

#### Linux
```bash
python build_linux.py
```

## 🚫 Solução de Problemas

### Windows

1. **Programa não inicia**:
   - Execute como administrador
   - Verifique se o Visual C++ Redistributable está instalado
   - Verifique os logs em `%APPDATA%\nerd_rats\logs`

2. **Logs não aparecem**:
   - Crie manualmente a pasta `%APPDATA%\nerd_rats\logs`
   - Execute como administrador
   - Configure `LOG_LEVEL=DEBUG` para mais detalhes

### Linux

1. **Permissões negadas**:
   ```bash
   sudo chmod -R 755 /opt/nerd_rats
   sudo chown -R $USER:$USER /var/log/nerd_rats
   ```

2. **Serviço não inicia**:
   ```bash
   sudo systemctl status nerd_rats
   sudo journalctl -u nerd_rats
   ```

## 📝 Comandos Úteis

### Windows PowerShell

```powershell
# Iniciar o programa
.\dist\NerdRats.exe

# Parar o programa
Stop-Process -Name NerdRats -Force

# Ver logs em tempo real
Get-Content -Path "$env:APPDATA\nerd_rats\logs\$(Get-Date -Format 'yyyy-MM-dd').log" -Wait
```

### Linux

```bash
# Status do serviço
sudo systemctl status nerd_rats

# Reiniciar serviço
sudo systemctl restart nerd_rats

# Ver logs em tempo real
tail -f /var/log/nerd_rats/$(date +%Y-%m-%d).log
```

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.

## 🤝 Contribuindo

Contribuições são bem-vindas! Por favor, leia o [CONTRIBUTING.md](CONTRIBUTING.md) para detalhes sobre nosso código de conduta e o processo para enviar pull requests.
