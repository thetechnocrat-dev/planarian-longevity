from rest_framework.generics import CreateAPIView
from .models import CustomUser
from .serializers import UserSerializer

class SignUpView(CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
