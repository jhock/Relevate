from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from ....settings.access_keys import TOKEN_SECRET_KEY


def generate_confirmation_token(user_profile, expiration=3600):
    s = Serializer(TOKEN_SECRET_KEY, expiration)
    return s.dumps({'confirm': user_profile.id})


def confirm(user_profile, token):
    s = Serializer(TOKEN_SECRET_KEY)
    try:
        data = s.loads(token)
    except:
        return False
    if data.get('confirm') != user_profile.id:
        return False
    user_profile.confirmed = True
    user_profile.save()
    return True


def new_confirm(user_profile):
    if user_profile.confirmed:
        return True
    user_profile.confirmed = True
    user_profile.save()
    return True