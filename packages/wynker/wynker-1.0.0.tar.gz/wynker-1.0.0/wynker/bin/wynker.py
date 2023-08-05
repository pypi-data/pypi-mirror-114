import os

import click
import shutil
from jinja2 import Template
from wynker import __version__
from .helper import (
    validate_name,
    get_template_path,
    is_main_dir,
    get_project_name,
    get_models_directory,
    get_blueprints_directory
)


@click.group()
@click.version_option(__version__)
def main():
    pass


@main.command()
@click.argument("project_name")
def start(project_name):
    """Creates new Flask Project"""

    # normalize
    project_name = project_name.lower().replace("-", "_")

    if not validate_name(project_name):
        click.secho(
            f"\n Error! Invalid project name, please provide a valid project name \n",
            fg="red",
        )
        exit()

    # check directory with project_name exists or not
    if os.path.exists(project_name):
        click.secho(
            f"\n Error! Directory with {project_name} already exists! \n", fg="red"
        )
        exit()

    click.secho(f"\nCreating a new Flask app in {os.getcwd()}/\n")

    template_path = get_template_path("project")

    prefix_length = len(template_path)

    not_render_ext = [".html", ".js", ".css"]

    for root, dirs, files in os.walk(template_path):
        path_rest = root[prefix_length:]

        parent_dir = path_rest.replace("project_name", project_name)

        if parent_dir:
            target_dir = os.path.join(os.getcwd(), parent_dir)
            os.makedirs(target_dir, exist_ok=True)

        for dirname in dirs[:]:
            if dirname.startswith(".") or dirname == "__pycache__":
                dirs.remove(dirname)

        for filename in files:
            name, extension = os.path.splitext(filename)
            old_path = os.path.join(root, filename)
            new_path = os.path.join(
                os.getcwd(), parent_dir, filename.replace("project_name", project_name)
            )
            
            if not extension in not_render_ext:
                with open(old_path, encoding="utf-8") as template_file:
                    content = template_file.read()
                template = Template(content).render(project_name=project_name)
                with open(new_path, "w", encoding="utf-8") as new_file:
                    new_file.write(template)
            else:
                shutil.copyfile(old_path, new_path)

    click.secho(
        f"\nSuccess! Created {project_name} at {os.getcwd()}/{project_name}.\n",
        fg="green",
    )

    next_steps = f"""
We suggest that you begin by typing:
    
    cd {project_name}
    flask run
    """

    click.secho(next_steps)


@main.group()
def add():
    """Adds Blueprint, Model to your app"""
    pass


@add.command()
@click.argument("model_name")
def model(model_name):
    """Adds model in your app"""

    # normalize
    model_name = model_name.lower().replace("-", "_")

    if not validate_name(model_name):
        click.secho(
            f"\n Error! Invalid model name, please provide a valid model name \n",
            fg="red",
        )
        exit()

    template_model_dir = get_template_path("model")

    prefix_length = len(template_model_dir)

    # check command is ran from main directory
    main_dir = is_main_dir()

    if not main_dir:
        click.secho(
            f"\n Error! Please run this command in main project directory where wsgi.py file exists. \n",
            fg="red",
        )
        exit()

    project_name = get_project_name()

    if not project_name:
        click.secho(
            f"\n Error! Please make sure you are in main project directory where wsgi.py file exists \n",
            fg="red",
        )
        exit()

    model_directory = get_models_directory()
    model_path = os.path.join(model_directory, f"{model_name}.py")

    if os.path.isfile(model_path):
        click.secho(
            f"\n Error! Looks like {model_name} model already exists! \n",
            fg="red",
        )
        exit()

    for root, dirs, files in os.walk(template_model_dir):
        
        for file in files:
            with open(os.path.join(root, file), encoding="utf-8") as f:
                content = f.read()
            model_temp = Template(content).render(
                model_name=model_name, project_name=project_name
            )
            with open(model_path, "w", encoding="utf-8") as tf:
                tf.write(model_temp)
    
    # append to __init__ file
    if os.path.isfile(os.path.join(model_directory, '__init__.py')):
        with open(os.path.join(model_directory, "__init__.py"), "a", encoding="utf-8") as file:
            file.write(f"\nfrom .{model_name} import {model_name.title()}  # Added by WYNKER")

    click.secho(
        f"\nSuccess! Added model {model_name}.\n",
        fg="green",
    )

    next_steps = f"""
To make migration of model, type:
    
    flask db -m "your-migration-message"
    flask db upgrade
    """

    click.secho(next_steps)


@add.command()
@click.argument("blueprint_name")
def blueprint(blueprint_name):
    """Adds blueprint in your app"""

    # normalize
    blueprint_name = blueprint_name.lower().replace("-", "_")

    if not validate_name(blueprint_name):
        click.secho(
            f"\n Error! Invalid blueprint name, please provide a valid blueprint name \n",
            fg="red",
        )
        exit()

    template_blueprint_dir = get_template_path("blueprint")

    prefix_length = len(template_blueprint_dir)

    not_render_ext = [".html", ".js", ".css"]

    # check command is ran from main directory
    main_dir = is_main_dir()

    if not main_dir:
        click.secho(
            f"\n Error! Please run this command in main project directory where wsgi.py file exists. \n",
            fg="red",
        )
        exit()

    project_name = get_project_name()

    if not project_name:
        click.secho(
            f"\n Error! Please make sure you are in main project directory where wsgi.py file exists \n",
            fg="red",
        )
        exit()
    
    blueprint_directory = get_blueprints_directory()
    blueprint_path = os.path.join(blueprint_directory, blueprint_name)

    if os.path.isdir(blueprint_path):
        click.secho(
            f"\n Error! Looks like {blueprint_name} blueprint already exists! \n",
            fg="red",
        )
        exit()
    
    for root, dirs, files in os.walk(template_blueprint_dir):
        path_rest = root[prefix_length:]

        parent_dir = path_rest.replace("blueprint_name", blueprint_name)

        if parent_dir:
            target_dir = os.path.join(blueprint_directory, parent_dir)
            os.makedirs(target_dir, exist_ok=True)

        for dirname in dirs[:]:
            if dirname.startswith(".") or dirname == "__pycache__":
                dirs.remove(dirname)

        for filename in files:
            name, extension = os.path.splitext(filename)
            old_path = os.path.join(root, filename)
            new_path = os.path.join(
                blueprint_directory, parent_dir, filename.replace("blueprint_name", blueprint_name)
            )
            if not extension in not_render_ext:
                with open(old_path, encoding="utf-8") as template_file:
                    content = template_file.read()
                template = Template(content).render(blueprint_name=blueprint_name)
                with open(new_path, "w", encoding="utf-8") as new_file:
                    new_file.write(template)
            else:
                shutil.copyfile(old_path, new_path)


    click.secho(
        f"\nSuccess! Added blueprint {blueprint_name}.\n",
        fg="green",
    )

    next_steps = f"""
To register blueprint, follow:
    
    1. Open settings.py file

    2. Add following module path in REGISTER_BLUEPRINTS list

       {project_name}.blueprints.{blueprint_name}
    """

    click.secho(next_steps)


if __name__ == "__main__":
    main()
