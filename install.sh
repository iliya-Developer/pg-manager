#!/bin/bash

REPO_URL="https://github.com/iliya-Developer/pg-manager.git"
APP_NAME="pg-manager"
APP_DIR="/opt/$APP_NAME"
SERVICE_NAME="$APP_NAME.service"
ENV_FILE="$APP_DIR/.env"

if [ "$EUID" -ne 0 ]; then
    echo "Please run as root"
    exit 1
fi

show_menu() {
    clear
    echo "======================================"
    echo "          $APP_NAME INSTALLER"
    echo "======================================"
    echo "1) Install"
    echo "2) Restart Service"
    echo "3) Uninstall"
    echo "4) Exit"
    echo "======================================"
    read -p "Select an option: " choice
}

install_app() {
    echo "[+] Installing $APP_NAME ..."

    read -p "Enter Telegram Bot Token: " BOT_TOKEN
    read -p "Enter Admin Telegram ID: " ADMIN_ID

    if [ -z "$BOT_TOKEN" ] || [ -z "$ADMIN_ID" ]; then
        echo "Error: BOT_TOKEN and ADMIN_ID are required"
        return 1
    fi

    echo "[+] Installing required packages..."
    apt update -y
    apt install -y python3 python3-venv python3-pip git rsync curl

    rm -rf "$APP_DIR"
    mkdir -p "$APP_DIR"

    echo "[+] Downloading project from GitHub..."
    if [ -d "/tmp/$APP_NAME" ]; then
        rm -rf "/tmp/$APP_NAME"
    fi
    git clone "$REPO_URL" "/tmp/$APP_NAME" || { echo "Git clone failed"; exit 1; }

    echo "[+] Copying project files..."
    rsync -av --exclude ".git" "/tmp/$APP_NAME/" "$APP_DIR/"
    rm -rf "/tmp/$APP_NAME"

    echo "[+] Creating virtual environment..."
    python3 -m venv "$APP_DIR/venv"

    echo "[+] Installing Python requirements..."
    "$APP_DIR/venv/bin/pip" install --upgrade pip
    "$APP_DIR/venv/bin/pip" install -r "$APP_DIR/requirements.txt" || true

    echo "[+] Installing required Python modules..."
    "$APP_DIR/venv/bin/pip" install fastapi uvicorn telebot python-dotenv requests

    echo "[+] Creating .env file..."
    cat <<EOF > "$ENV_FILE"
BOT_TOKEN=$BOT_TOKEN
ADMIN_ID=$ADMIN_ID
API_URL=http://127.0.0.1:9000/create-users
EOF

    echo "[+] Creating systemd service..."
    cat <<EOF > "/etc/systemd/system/$SERVICE_NAME"
[Unit]
Description=$APP_NAME Service
After=network.target

[Service]
User=root
WorkingDirectory=$APP_DIR
ExecStart=$APP_DIR/venv/bin/python $APP_DIR/main.py
Restart=always
EnvironmentFile=$ENV_FILE

[Install]
WantedBy=multi-user.target
EOF

    systemctl daemon-reload
    systemctl enable "$SERVICE_NAME"
    systemctl restart "$SERVICE_NAME"

    echo "======================================"
    echo "[✓] Installation Completed Successfully!"
    echo "Service: pg-manager.service"
    echo "======================================"
}

restart_service() {
    if ! systemctl is-active --quiet "$SERVICE_NAME"; then
        echo "Service is not running"
        return 1
    fi
    systemctl restart "$SERVICE_NAME"
    echo "[✓] Service restarted."
}

uninstall_app() {
    if systemctl is-active --quiet "$SERVICE_NAME"; then
        systemctl stop "$SERVICE_NAME"
    fi
    if systemctl is-enabled --quiet "$SERVICE_NAME"; then
        systemctl disable "$SERVICE_NAME"
    fi
    rm -f "/etc/systemd/system/$SERVICE_NAME"
    rm -rf "$APP_DIR"
    systemctl daemon-reload
    echo "[✓] Application removed."
}

while true; do
    show_menu
    case $choice in
        1) install_app ;;
        2) restart_service ;;
        3) uninstall_app ;;
        4) exit 0 ;;
        *) echo "Invalid option!" ;;
    esac
    read -p "Press Enter to continue..."
done