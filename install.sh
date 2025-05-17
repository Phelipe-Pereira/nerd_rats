#!/bin/bash

# Verifica se está rodando como root
if [ "$EUID" -ne 0 ]; then 
    echo "Por favor, execute como root (sudo ./install.sh)"
    exit 1
fi

# Verifica se Python está instalado
if ! command -v python3 &> /dev/null; then
    echo "Python3 não encontrado. Por favor, instale o Python 3.7 ou superior."
    exit 1
fi

# Cria ambiente virtual
python3 -m venv .venv
source .venv/bin/activate

# Instala dependências
pip install -r requirements.txt

# Cria diretório de instalação
INSTALL_DIR="/opt/nerd_rats"
mkdir -p "$INSTALL_DIR"
cp -r src/ requirements.txt "$INSTALL_DIR/"

# Cria arquivo .env com configurações
cat > "$INSTALL_DIR/.env" << EOL
TRACKING_POST_URL=https://nerds-rats-hackathon.onrender.com/metrics
TRACKING_INTERVAL=15
CONFIG_PATH=/etc/nerd_rats.conf
EOL

# Cria serviço systemd
cat > /etc/systemd/system/nerd_rats.service << EOL
[Unit]
Description=NerdRats Event Tracker
After=network.target

[Service]
Type=simple
ExecStart=/opt/nerd_rats/.venv/bin/python /opt/nerd_rats/src/presentation/cli/main.py
Restart=always
User=$SUDO_USER
Environment=PYTHONPATH=/opt/nerd_rats
Environment=DISPLAY=:0

[Install]
WantedBy=multi-user.target
EOL

# Recarrega serviços systemd e habilita o serviço
systemctl daemon-reload
systemctl enable nerd_rats
systemctl start nerd_rats

echo "Instalação concluída! O serviço foi iniciado e será executado automaticamente na inicialização."
