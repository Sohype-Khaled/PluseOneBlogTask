from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from authn.serializers import RegisterUserSerializer


class RegisterAPIView(APIView):
    permission_classes = [AllowAny]
    parser_classes = (MultiPartParser,)

    @swagger_auto_schema(
        request_body=RegisterUserSerializer,
        responses={
            201: "Created",
            422: "Unprocessable Entity",
        },
        operation_summary="User Registration",
        operation_description="Register a new user with the provided username, email, and password."
    )
    def post(self, request):
        """
        Register a new user with the provided data.
        """
        serializer = RegisterUserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()

            refresh = RefreshToken.for_user(user)
            return Response({"access": str(refresh.access_token), "refresh": str(refresh)
                             }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
