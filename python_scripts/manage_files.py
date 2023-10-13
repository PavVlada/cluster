import os
import yaml
from jinja2 import Template


def read_yaml(dir, name):
    full_path = os.path.join(dir, name)

    with open(full_path, "r") as file:
        return yaml.safe_load(file)


def read_config():
    config_dir = os.environ.get('CONFIG_DIR')
    config_file = os.environ.get('CONFIG_FILE')
    config = read_yaml(config_dir, config_file)
    return config


def read_secret():
    secret_dir = os.environ.get('SECRET_DIR')
    secret_file = os.environ.get('SECRET_FILE')
    return read_yaml(secret_dir, secret_file)


def read_file(dir, name):
    full_path = os.path.join(dir, name)

    with open(full_path, 'r') as file:
        return file.read()


def create_file(output_dir, output_name, content):
    full_path = os.path.join(output_dir, output_name)
    
    with open(full_path, 'w') as output_file:
        output_file.write(content)


def read_template(template_name):
    current_dir = os.path.dirname(os.path.abspath(__file__))
    template_dir = os.path.join(current_dir, 'templates')
    return read_file(template_dir, template_name + '.j2')
    

def render_template(template_content, context):
    template = Template(template_content)
    return template.render(context)


def create_template(output_dir, output_name, template_name, context):
    template_content = read_template(template_name)
    rendered_content = render_template(template_content, context)
    create_file(output_dir, output_name, rendered_content)