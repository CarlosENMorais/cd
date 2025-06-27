#!/bin/bash

echo "Criando um ambiente virtual Python..."
python3 -m venv .venv

echo "Ativando ambiente virtual..."
source .venv/bin/activate

echo "Instalando pacotes necessários..."
python3 -m pip install -r requirements.txt

echo "Executando programa dash_app.app"
python3 -m dash_app.app

