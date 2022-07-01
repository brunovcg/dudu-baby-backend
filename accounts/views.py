from rest_framework.views import APIView
from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from accounts.permissions import IsSuperuser
from rest_framework.authtoken.models import Token
from accounts.models import User
from .serializers import UserSerializer
from django.db import IntegrityError

class LoginView(APIView):

    def post(self, request):

        username= request.data['username']
        password = request.data['password']
        user = authenticate(username=username, password=password)
        user_type = ""

        if user:
            token = Token.objects.get_or_create(user=user)[0]

            user_logged = User.objects.get(username=username)

            if user_logged.is_superuser:
                user_type = 'superuser'
            else:
                user_type="user"

            return Response({'token': token.key, "user_id" : user_logged.id, "user_type" : user_type, "username" : user_logged.username })

        return Response({"message": "Wrong username or password"}, status=status.HTTP_401_UNAUTHORIZED)


class SignupView(APIView):


    def post(self, request):

        try:
            new_user =  User.objects.get_or_create(
                username = request.data["username"],
                email = request.data["email"],
                password = request.data["password"],
                is_superuser = request.data["is_superuser"],
                document = request.data["document"],
              
            )
            if not new_user[1]:
              return Response({"message: User Already exists"},status=status.HTTP_409_CONFLICT)
        except IntegrityError:
            return Response({"message: Payload error"},status=status.HTTP_400_BAD_REQUEST)

        serialized = UserSerializer(new_user[0])
        return Response(serialized.data, status=status.HTTP_201_CREATED)

class UserView(APIView):
    # authentication_classes = [TokenAuthentication]
    # permission_classes = [IsSuperuser]


    def get(self,request):

        users = User.objects.all()
        serialized = UserSerializer(users, many=True)

        return Response(serialized.data,status=status.HTTP_200_OK)

