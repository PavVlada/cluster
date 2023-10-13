if [ ! -f "$SSH_DIR/$SSH_KEY" ]; then
    ssh-keygen -t rsa -b 2048 -f "$SSH_DIR/$SSH_KEY"
    ssh-add "$SSH_DIR/$SSH_KEY"
    echo "Ключ $1 создан и добавлен в ssh-agent."
fi
echo "Используется ключ $SSH_KEY"
