#!/bin/bash

# Verifica se está rodando como root
if [ "$EUID" -ne 0 ]; then 
    echo "Por favor, execute como root (sudo ./install_linux.sh)"
    exit 1
fi

# Cria diretório de instalação
INSTALL_DIR="/opt/nerd_rats"
mkdir -p "$INSTALL_DIR"

# Copia arquivos
cp -r src/ requirements.txt "$INSTALL_DIR/"

# Cria ambiente virtual e instala dependências
python3 -m venv "$INSTALL_DIR/venv"
source "$INSTALL_DIR/venv/bin/activate"
pip install -r requirements.txt

# Cria arquivo .env
cat > "$INSTALL_DIR/.env" << EOL
TRACKING_POST_URL=https://nerds-rats-hackathon.onrender.com/metrics
TRACKING_INTERVAL=20
CONFIG_PATH=/etc/nerd_rats.conf
EOL

# Cria serviço systemd
cat > /etc/systemd/system/nerd_rats.service << EOL
[Unit]
Description=NerdRats Event Tracker
After=network.target

[Service]
Type=simple
ExecStart=$INSTALL_DIR/venv/bin/python $INSTALL_DIR/src/presentation/cli/main.py
Restart=always
User=$SUDO_USER
Environment=PYTHONPATH=$INSTALL_DIR
Environment=DISPLAY=:0

[Install]
WantedBy=multi-user.target
EOL

# Configura permissões
chown -R $SUDO_USER:$SUDO_USER "$INSTALL_DIR"
chmod +x "$INSTALL_DIR/src/presentation/cli/main.py"

# Inicia o serviço
systemctl daemon-reload
systemctl enable nerd_rats
systemctl start nerd_rats

echo "Instalação concluída! O serviço foi iniciado e será executado automaticamente na inicialização." 