import os

from {{project_name}} import create_app

config = os.environ.get("APP_CONFIG")

app = create_app(config)

if __name__ == "__main__":
    app.run(host="0.0.0.0")
