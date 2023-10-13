if [ ! -d "./../venv" ]; then
    echo "Создание виртуального окружения..."
    python3 -m venv ./../venv
fi
source ./../venv/bin/activate

pip install -r ./../requirements.txt 1> /dev/null
deactivate

echo "Виртуальное окружение готово к работе"