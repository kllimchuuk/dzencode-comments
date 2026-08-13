from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import RefreshToken

from .exceptions import InvalidTokenException


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        refresh = request.data.get("refresh")
        if not refresh:
            raise InvalidTokenException("Refresh token is required.")
        try:
            RefreshToken(refresh).blacklist()
        except TokenError:
            raise InvalidTokenException()
        return Response(
            {"detail": "Successfully logged out."}, status=status.HTTP_200_OK
        )
