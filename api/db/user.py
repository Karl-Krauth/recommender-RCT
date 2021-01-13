from __future__ import annotations
import secrets
import time
import typing

import jwt
import werkzeug.security

from . import base


SECRET_KEY = secrets.token_hex(128)


class User(base.db.Model):
    __tablename__ = 'users'
    id = base.db.Column(base.db.Integer, primary_key=True)
    username = base.db.Column(base.db.String(32), index=True, unique=True)
    password_hash = base.db.Column(base.db.String(128))

    def verify_password(self, password: str) -> bool:
        return werkzeug.security.check_password_hash(self.password_hash, password)

    def generate_auth_token(self, expires_in: int=600) -> str:
        return jwt.encode(payload={'id': self.id, 'exp': time.time() + expires_in},
                          key=SECRET_KEY,
                          algorithm='HS256')

    @staticmethod
    def verify_auth_token(token: str) -> typing.Optional[User]:
        try:
            data = jwt.decode(token,
                              key=SECRET_KEY,
                              algorithms=['HS256'])
        except:
            return None

        return User.query.get(data['id'])

    @staticmethod
    def get_user(username: str) -> typing.Optional[User]:
        return User.query.filter_by(username=username).one_or_none()

    @staticmethod
    def add_user(username: str, password: str) -> typing.Optional[User]:
        if User.get_user(username=username) is not None:
            return None

        password_hash = werkzeug.security.generate_password_hash(password)
        user = User(username=username, password_hash=password_hash)
        base.db.session.add(user)
        base.db.session.commit()
        return user
