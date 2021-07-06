import requests

from domain.models import User


class GoogleAuthenticator:
    def authenticate(self, google_jwt_token):
        response = requests.get(
            f"https://oauth2.googleapis.com/tokeninfo?id_token={google_jwt_token}"
        )

        user = response.json()
        return User.from_dict(user)

    def get_user(self, jwt_token):
        pass


def get_google_authenticator():
    return GoogleAuthenticator()
