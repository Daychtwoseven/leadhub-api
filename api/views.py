from django.db.models import Q
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework import status, authentication
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from . models import *
from . serializers import *


@api_view(['GET', 'POST'])
@authentication_classes([authentication.TokenAuthentication])
@permission_classes([IsAuthenticated])
def index_page(request):
    try:
        if request.method == 'POST':
            print('here')
        
        elif request.method == 'GET':
            print('here')
    except Exception as e:
        return Response({'statusMsg': str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'POST'])
def create_user_page(request):
    try:
        if request.method == 'POST':
            print(request.data)
            email = request.data['email']
            username = request.data['username']
            password = request.data['password']
            password2 = request.data['password2']

            if password == password2:
                account = Account.objects.filter(Q(email=email) | Q(username=username)).first()
                if not account:
                    account = Account.objects.create(email=email, username=username)
                    account.set_password(password)
                    account.save()
                    token = Token.objects.filter(user=account).first()

                    data = {
                        'email': account.email,
                        'username': account.username,
                        'token': token.key
                    }

                    return Response(data, status=status.HTTP_200_OK)

                return Response({'statusMsg': 'Account already exist.'}, status=status.HTTP_400_BAD_REQUEST)

            return Response({'statusMsg': 'Password did not match.'}, status=status.HTTP_400_BAD_REQUEST)

        elif request.method == 'GET':
            return Response({'email': "", 'username': "", 'password': "", 'password2': ""}, status=status.HTTP_200_OK)

    except Exception as e:
        return Response({'statusMsg': str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def get_user_page(request):
    try:
        print(request.data['email'])
        if request.data['email']:
            account = Account.objects.filter(email=request.data['email']).first()
            if account:
                token = Token.objects.filter(user=account).first()

                data = {
                    'email': account.email,
                    'username': account.username,
                    'token': token.key
                }

                return Response({'account': data}, status=status.HTTP_201_CREATED)
            return Response({'statusMsg': 'Email does not exist.'}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'statusMsg': 'Email Required.'}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({'statusMsg': str(e)}, status=status.HTTP_400_BAD_REQUEST)