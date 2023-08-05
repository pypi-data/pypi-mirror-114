from flask import Blueprint, render_template


{{blueprint_name}} = Blueprint(
    "{{blueprint_name}}",
    __name__,
    template_folder="templates",
    static_folder="static",
    static_url_path="/{{blueprint_name}}/static/",
    url_prefix="/{{blueprint_name}}"
)


@{{blueprint_name}}.route("/")
def index():
    return render_template("{{blueprint_name}}/index.html", title="{{blueprint_name|title}}")


# add your routes here
