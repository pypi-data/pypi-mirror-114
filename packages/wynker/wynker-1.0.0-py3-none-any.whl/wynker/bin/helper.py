import re
import os
import importlib

def validate_name(name: str):
    pattern = r"^[\w]*$"
    if re.search(pattern, name):
        return True
    else:
        return False


def get_template_path(template):
    """Return WYNKER template path"""

    import wynker

    wynker_path = os.path.dirname(wynker.__file__)

    template_path = os.path.join(wynker_path, f'templates/{template}/')

    return template_path


def is_main_dir():
    current_dir = os.getcwd()

    wsgi_path = os.path.join(current_dir, 'wsgi.py')

    if not os.path.isfile(wsgi_path):
        return False
    else:
        return True


def get_project_name():
    """Return project name"""
    current_path = os.getcwd()
    for root_main, dirs_main, files_main in os.walk(current_path):
        for dir in dirs_main:
            if os.path.isfile(os.path.join(dir, 'settings.py')):
                return dir
    
    return False


def get_models_directory():
    """Returns model directory path"""

    current_app_path = os.path.join(os.getcwd(), get_project_name())

    model_dir = os.path.join(current_app_path, "models/")

    return model_dir


def get_blueprints_directory():
    """Return blueprint directory path"""

    current_app_path = os.path.join(os.getcwd(), get_project_name())

    blueprint_dir = os.path.join(current_app_path, "blueprints/")

    return blueprint_dir