if [ ! -f "$ISO_DIR/$ISO_NAME" ]; then
    wget "$ISO_URL" -P "$ISO_DIR"
    echo "Скачивание $ISO_NAME успешно завершено"
fi
echo "Используется образ $ISO_NAME"