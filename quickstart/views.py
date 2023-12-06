from django.contrib.auth import login
from knox.views import LoginView as KnoxLoginView
from quickstart.serializers import AuthSerializer, UserSerializer
from rest_framework import authentication, generics, permissions
from rest_framework.authtoken.serializers import AuthTokenSerializer


class CreateUserView(generics.CreateAPIView):
    # Create user API view
    serializer_class = UserSerializer



class LoginView(KnoxLoginView):
    # login view extending KnoxLoginView
    serializer_class = AuthSerializer
    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        serializer = AuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        return super(LoginView, self).post(request, format=None) 


class ManageUserView(generics.RetrieveUpdateAPIView):
    """Manage the authenticated user"""
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self):
        """Retrieve and return authenticated user"""
        return self.request.user