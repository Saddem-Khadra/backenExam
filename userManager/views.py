import datetime
import jwt
from rest_framework.exceptions import AuthenticationFailed, NotFound, PermissionDenied
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import User
from userManager.utils import auth_token
from .serializer import UserSerializer


class LoginView(APIView):
    def post(self, request):
        email = request.data['email']
        password = request.data['password']
        user = User.objects.filter(email=email).first()
        if user is None:
            raise AuthenticationFailed('User not Found!')
        if not user.check_password(password):
            raise AuthenticationFailed('Incorrect Password!')

        payload = {
            'id': user.id,
            'iat': datetime.datetime.utcnow(),
            'exp': datetime.datetime.utcnow() + datetime.timedelta(days=60),
        }
        token = jwt.encode(payload, 'secret', algorithm='HS256')
        response = Response()
        response.set_cookie(key='Token', value=token, httponly=True)

        user_serialize = UserSerializer(user)
        response.data = user_serialize.data
        print(response.cookies.values())
        return response


class UserView(APIView):

    def get(self, request):
        response = Response()
        response.data = auth_token(request).data
        return response


class NotFriendsView(APIView):
    def get(self, request):
        users = User.objects.all().exclude(friends__email__exact=auth_token(request).data.get('email', None)).exclude(
            id=auth_token(request).data.get('id', None))
        serializer = UserSerializer(users, many=True)

        response = Response()
        response.data = serializer.data
        return response


class LogoutView(APIView):
    def post(self, request):
        if auth_token(request):
            response = Response()
            response.delete_cookie('Token')
            response.data = {'message': 'token deleted'}
            return response


class RegisterView(APIView):
    def get(self, request):
        if request.data.get('user_id', None):
            if User.objects.filter(id=request.data.get('user_id', None)).exists():
                user = User.objects.get(id=request.data.get('user_id', None))
                response = Response()
                response.data = UserSerializer(user).data
            else:
                raise NotFound
        else:
            users = User.objects.all().order_by('id')
            response = Response()
            response.data = UserSerializer(users, many=True).data
        return response

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
        response = Response()
        response.data = {'user': serializer.data}
        return response

    def put(self, request):
        if auth_token(request):
            if request.data.get('friend_id', None):
                if User.objects.filter(id=request.data.get('friend_id', None)).exists():
                    user = User.objects.get(id=auth_token(request).data.get('id', None))
                    serializer = UserSerializer(instance=user, data=request.data,
                                                context={
                                                    "method": request.method,
                                                    "friend_id": request.data.get('friend_id', None),
                                                    "add": request.data.get('add', None)
                                                })
                    if serializer.is_valid(raise_exception=True):
                        serializer.save()
                    response = Response()
                    response.data = UserSerializer(user).data
                else:
                    raise NotFound
            else:
                raise NotFound
            return response
        else:
            raise PermissionDenied
