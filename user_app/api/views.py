from rest_framework.decorators import api_view
from user_app.api.serializers import RegistrationSerializer
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from user_app import models
from rest_framework import status
# from rest_framework_simplejwt.tokens import RefreshToken

@api_view(['POST',])
def logout_view(request):

    if request.method == 'POST':
        request.user.auth_token.delete()
        return Response(status=status.HTTP_200_OK)
        
@api_view(['POST',])
def registration_view(request):
    
    if request.method == 'POST':
        serializer = RegistrationSerializer(data=request.data)

        #Create a new dictionary
        data = {}

        #checking whether the serializer condition is valid
        if serializer.is_valid():
            account = serializer.save()

            #Data inside the account from the serializer
            data['response'] = 'Registration Successful!'
            data['username']  = account.username
            data['email'] = account.email

            #To access the token
            #The .key extension prevents the error Object of type Token is not JSON serializable
            # token = Token.objects.get(user=account).key
            #Storing the token and returning it
            # data['token'] = token
            # refresh = RefreshToken.for_user(account)
            # data['token'] = {
            #                     'refresh': str(refresh),
            #                     'access': str(refresh.access_token),
            #                 }

        else:
            data = serializer.errors
        return Response(data, status=status.HTTP_201_CREATED)

