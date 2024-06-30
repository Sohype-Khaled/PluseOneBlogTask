from rest_framework_simplejwt.tokens import RefreshToken


def create_token(user):
    return RefreshToken.for_user(user)
