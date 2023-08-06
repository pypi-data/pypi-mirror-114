# -*- coding: utf-8 -*-

from starlette.authentication import BaseUser


# As of 2021/07/20, `user` is something like this:
# {
#     "iss": "https://accounts.google.com",
#     "azp": "1084386621732-qjmkaojnut33ml81ht4h7q22me2p6qb1.apps.googleusercontent.com",
#     "aud": "1084386621732-qjmkaojnut33ml81ht4h7q22me2p6qb1.apps.googleusercontent.com",
#     "sub": "106637688186237713656",
#     "hd": "iut-rodez.fr",
#     "email": "johnny.accot@iut-rodez.fr",
#     "email_verified": True,
#     "at_hash": "ndyKkyw5_LQTsA9JKLim4A",
#     "nonce": "uYnEP5r9BQK9ilJ4ruC7",
#     "name": "Johnny Accot",
#     "picture": "https://lh3.googleusercontent.com/a/AATXAJymU07Yz4XziVRLP3RQK3RzbdHM0B-DC4VZ0N5d=s96-c",
#     "given_name": "Johnny",
#     "family_name": "Accot",
#     "locale": "fr",
#     "iat": 1625999571,
#     "exp": 1626003171,
# }


class GoogleUser(BaseUser):
    def __init__(self, profile: dict) -> None:
        self.id = profile["id"]
        self.email = profile["email"]
        self.name = profile["name"]
        self.given_name = profile["given_name"]
        self.family_name = profile["family_name"]
        self.locale = profile["locale"]
        self.groups = profile["groups"]

    @property
    def is_authenticated(self) -> bool:
        return True

    @property
    def display_name(self) -> str:
        return self.name
