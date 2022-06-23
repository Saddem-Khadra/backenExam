import jwt
from rest_framework.exceptions import AuthenticationFailed
from .models import User
from .serializer import UserSerializer


def auth_token(request, *args, **kwargs):
    token = request.COOKIES.get('Token')
    if not token:
        raise AuthenticationFailed('Unauthenticated!')

    try:
        payload = jwt.decode(token, 'secret', algorithms=['HS256'])
    except jwt.ExpiredSignatureError:
        raise AuthenticationFailed('Unauthenticated!')

    user = User.objects.filter(id=payload['id']).first()
    user_serialize = UserSerializer(user)
    return user_serialize
