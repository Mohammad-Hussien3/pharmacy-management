from rest_framework_simplejwt.tokens import RefreshToken

class CustomToken(RefreshToken):
    @classmethod
    def for_user(cls, user):
        token = super().for_user(user)
        token['username'] = user.username
        token['email'] = user.email
        token['password'] = user.password

        return token
