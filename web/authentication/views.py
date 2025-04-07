from rest_framework.generics import CreateAPIView, GenericAPIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.token_blacklist.models import (
    OutstandingToken,
    BlacklistedToken,
)
from drf_spectacular.utils import extend_schema

from .serializers import SignUpSerializer, User


class SignUpView(CreateAPIView):
    serializer_class = SignUpSerializer
    queryset = User.objects.all()
    permission_classes = (AllowAny,)


class LogoutAllView(GenericAPIView):
    @extend_schema(request=None, responses={200: None})
    def post(self, request):
        current_user = request.user

        tokens = OutstandingToken.objects.filter(user=current_user).all()
        blacklisted_tokens = [BlacklistedToken(token=obj) for obj in tokens]

        BlacklistedToken.objects.bulk_create(
            blacklisted_tokens,
            ignore_conflicts=True,
        )

        return Response(status=status.HTTP_200_OK)
