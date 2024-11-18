#!/bin/bash

if ! dpkg -s pigpio > /dev/null 2>&1; then
    echo "Instalando o pigpio..."
    sudo apt update
    sudo apt install -y pigpio python3-pigpio
else
    echo "pigpio já está instalado."
fi

if ! pgrep -x "pigpiod" > /dev/null; then
    echo "Iniciando o daemon pigpiod..."
    sudo pigpiod
    echo "pigpiod iniciado."
else
    echo "pigpiod já está em execução."
fi
