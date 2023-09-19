from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, JsonResponse
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.viewsets import ModelViewSet, ViewSet

from application.models.user import User
from application.serializers.user import LoginSerializer, UserSerializer


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class LoginViewSet(ViewSet):
    serializer_class = LoginSerializer
    permission_classes = [AllowAny]

    @action(detail=False, methods=["POST"])
    def login(self, request):
        """ユーザのログイン"""
        serializer = LoginSerializer(data=request.data)
        if not serializer.is_valid():
            return JsonResponse(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST
            )

        employee_number = serializer.validated_data.get("employee_number")
        password = serializer.validated_data.get("password")
        user = authenticate(employee_number=employee_number, password=password)
        if not user:
            return JsonResponse(
                data={
                    "msg": "either employee number or password is incorrect"
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
        else:
            login(request, user)
            return JsonResponse(data={"role": user.Role(user.role).name})

    @action(methods=["POST"], detail=False)
    def logout(self, request):
        """ログアウト"""
        logout(request)
        return HttpResponse()
