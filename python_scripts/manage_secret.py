import crypt
import getpass
import os
import sys
from python_scripts.manage_files import create_template, create_file, read_file


def create_password():
    pw = getpass.getpass()
    if pw == getpass.getpass("Confirm: "):
        secured_pswd = crypt.crypt(pw)
        return  secured_pswd
    else:
        exit()


def read_pub_ssh_key():
    ssh_dir = os.environ.get('SSH_DIR')
    ssh_key = str(os.environ.get('SSH_KEY')) + ".pub"
    pub_ssh_key = read_file(ssh_dir, ssh_key).rstrip('\n')
    return pub_ssh_key


def create_secret_dict():
    print('Введите пароль для root:')
    rootpw = create_password()
    print('Введите пароль для создаваемого пользователя:')
    adminpw = create_password()
    ssh_key = read_pub_ssh_key()

    return {
        'rootpw': rootpw,
        'adminpw': adminpw,
        'ssh_key': ssh_key
    }


def save_secret(secret_dict):
    secret_dir = os.environ.get('SECRET_DIR')
    secret_file = os.environ.get('SECRET_FILE')
    create_template(secret_dir, secret_file, 'secret_template.yml', secret_dict)


def create_secret():
    secret_dict = create_secret_dict()
    save_secret(secret_dict)


def create_ansible_vault():
    secret_dir = os.environ.get('SECRET_DIR')
    secret_file = os.environ.get('SECRET_ANSIBLE_VAULT')

    print("Введите пароль для ansible vault")
    value = getpass.getpass()
    create_file(secret_dir, secret_file, value)


functions = {
    'secret': create_secret,
    'vault': create_ansible_vault
}


if __name__=='__main__':
    for arg in sys.argv[1:]:
        if arg in functions:
            functions[arg]()