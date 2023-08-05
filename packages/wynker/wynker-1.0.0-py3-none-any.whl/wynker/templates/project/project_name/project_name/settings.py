import importlib


# Register your blueprints here

REGISTER_BLUEPRINTS = [
    "{{project_name}}.blueprints.error_pages",
    "{{project_name}}.blueprints.main",
    # Add your blueprint name to register
]


def register_blueprints(app):
    for blueprint_name in REGISTER_BLUEPRINTS:
        blueprint_module = f"{blueprint_name}.views"
        module_handle = importlib.import_module(blueprint_module, ".")
        app.register_blueprint(getattr(module_handle, blueprint_name.split(".")[-1]))
