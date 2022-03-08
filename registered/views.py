from django.shortcuts import render

# Create your views here.
from .serializers import UserCreateSerializer
from rest_framework import response, decorators, permissions, status


# from rest_framework_simplejwt.tokens import RefreshToken


@decorators.api_view(['POST'])
@decorators.permission_classes([permissions.AllowAny])
def registered(request):
    serializer = UserCreateSerializer(data=request.data)
    if not serializer.is_valid():
        return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    user = serializer.save()
    # refresh = RefreshToken.for_user(user)
    # res = {
    #     'refresh': str(refresh),
    #     'access':  str(refresh.access_token)
    # }
    return response.Response('注册成功' + user.username, status=status.HTTP_201_CREATED)
