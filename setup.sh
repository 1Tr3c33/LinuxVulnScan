#!/bin/bash

echo "=== Configuración de la Herramienta de Ciberseguridad ==="

# Actualizar el sistema
echo "Actualizando el sistema..."
sudo apt update && sudo apt upgrade -y

# Instalar herramientas necesarias
echo "Instalando herramientas necesarias..."
sudo apt install -y nmap gobuster nikto

# Confirmar instalación de Python y pip
echo "Verificando Python y pip..."
if ! command -v python3 &>/dev/null; then
    echo "Python3 no está instalado. Instalándolo ahora..."
    sudo apt install -y python3
fi

if ! command -v pip3 &>/dev/null; then
    echo "pip no está instalado. Instalándolo ahora..."
    sudo apt install -y python3-pip
fi

# Instalar dependencias de Python
echo "Instalando dependencias de Python..."
pip3 install -r requirements.txt

echo "=== Configuración Completa ==="