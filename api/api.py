import os
import re
import typing

import flask
import flask_api
import flask_httpauth
import sqlalchemy

import db


app = flask_api.FlaskAPI(__name__)
auth = flask_httpauth.HTTPBasicAuth()


def main(debug: bool) -> None:
    db.setup_db(app)
    app.run(host='0.0.0.0', debug=debug)


@auth.verify_password
def verify_password(username_or_token: str, password: str) -> bool:
    # Attempt to authenticate with a token.
    user = db.User.verify_auth_token(username_or_token)
    if user is None:
        # Try to authenticate with a username and password.
        user = db.User.get_user(username_or_token)
        if user is None or not user.verify_password(password):
            return False

    flask.g.user = user
    return True


@app.route('/recommendations', methods=['GET'])
def get_recommendations() -> typing.List[typing.Dict[str, str]]:
    if 'video_id' in flask.request.args:
        video_id = flask.request.args['video_id']
        if not re.compile('[a-zA-Z0-9_-]{11}').match(video_id):
            raise flask_api.exceptions.ParseError('Invalid video id provided.')
    else:
        raise flask_api.exceptions.ParseError('No video id provided.')

    return [
        {
            'title': 'TEST VIDEO',
            'id': 'C0DPdy98e4c',
            'views': 1000,
        },
    ]


@app.route('/token')
@auth.login_required
def get_auth_token() -> typing.Dict[str, str]:
    token = flask.g.user.generate_auth_token()
    return {'token': token.decode('ascii')}


@app.route('/username')
@auth.login_required
def get_username() -> typing.Dict[str, str]:
    return {'hello': flask.g.user.username}


@app.route('/users', methods=['POST'])
def new_user() -> typing.Dict[str, str]:
    username = flask.request.json.get('username')
    password = flask.request.json.get('password')
    if username is None or password is None:
        raise flask_api.exceptions.ParseError()
    user = db.User.add_user(username=username, password=password)
    if user is None:
        raise flask_api.exceptions.ParseError()

    return {'username': user.username}


if __name__ == '__main__':
    main(os.environ.get('DEBUG') == '1')
