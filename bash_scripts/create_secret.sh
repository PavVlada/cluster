if [ ! -f "$SECRET_DIR/$SECRET_FILE" ]; then
    args+="secret "
fi

if [ ! -f "$SECRET_DIR/$SECRET_ANSIBLE_VAULT" ]; then
    args+="vault"
fi

if [ -n "$args" ]; then
    python ../python_scripts/manage_secret.py $args
fi

echo "Используется секрет $SECRET_FILE и vault $SECRET_ANSIBLE_VAULT"
