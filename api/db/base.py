import os

import flask
import flask_sqlalchemy


db = flask_sqlalchemy.SQLAlchemy()


def setup_db(app: flask.Flask) -> None:
    app.config['SQLALCHEMY_DATABASE_URI'] = (
        'postgres+psycopg2://{username}:{password}@{host}:{port}/{db_name}'.format(
            username=os.environ.get('RDS_USERNAME', 'user'),
            password=os.environ.get('RDS_PASSWORD', 'password'),
            host=os.environ.get('RDS_HOSTNAME', 'db'),
            port=os.environ.get('RDS_PORT', 5432),
            db_name=os.environ.get('RDS_DB_NAME', 'user'),
        )
    )
    db.init_app(app)
    with app.app_context():
        db.create_all()
