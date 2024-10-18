#!/bin/bash

# Переменные
VENV_DIR=".venv"
DOMAIN_APP1="home.com"  # Локальный домен для первого приложения
DOMAIN_APP2="hacker.com"  # Локальный домен для второго приложения
APP1_MODULE="home-stand.home:app"    # Укажите модуль первого приложения Flask
APP2_MODULE="hacker-stand.hacker:app" # Укажите модуль второго приложения Flask
PORT_APP1=8080            # Порт для первого приложения
PORT_APP2=8081            # Порт для второго приложения

# Проверка на наличие виртуального окружения
if [ ! -d "$VENV_DIR" ]; then
    echo ">>> Создание виртуального окружения"
    python3 -m venv $VENV_DIR
else
    echo ">>> Виртуальное окружение уже существует"
fi

echo ">>> Активация виртуального окружения"
source $VENV_DIR/bin/activate

echo ">>> Установка зависимостей"
pip install -r requirements.txt

echo ">>> Добавление записей в /etc/hosts"
# Проверка, есть ли уже запись для первого приложения
if ! grep -q "$DOMAIN_APP1" /etc/hosts; then
    sudo sh -c "echo '127.0.0.1 $DOMAIN_APP1' >> /etc/hosts"
    echo ">>> Запись добавлена: 127.0.0.1 $DOMAIN_APP1"
else
    echo ">>> Запись для $DOMAIN_APP1 уже существует"
fi

# Проверка, есть ли уже запись для второго приложения
if ! grep -q "$DOMAIN_APP2" /etc/hosts; then
    sudo sh -c "echo '127.0.0.1 $DOMAIN_APP2' >> /etc/hosts"
    echo ">>> Запись добавлена: 127.0.0.1 $DOMAIN_APP2"
else
    echo ">>> Запись для $DOMAIN_APP2 уже существует"
fi

echo ">>> Запуск первого приложения через Gunicorn"
gunicorn  --bind $DOMAIN_APP1:$PORT_APP1 $APP1_MODULE &

echo ">>> Запуск второго приложения через Gunicorn"
gunicorn  --bind $DOMAIN_APP2:$PORT_APP2 $APP2_MODULE &

echo ">>> Оба приложения запущены"
