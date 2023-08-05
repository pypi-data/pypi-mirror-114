from {{project_name}} import db


class {{ model_name|title }}(db.Model):

    __tablename__ = "{{model_name}}"

    id = db.Column(db.Integer, primary_key=True)
    # Add your table columns here