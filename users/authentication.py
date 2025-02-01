from datetime import datetime, timedelta

from rest_framework import permissions
from rest_framework.permissions import BasePermission
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken

from users.serializers import UserUsernameAndIdSerializer


class JwtExtractor(JWTAuthentication):
    def get_jwt_values(self, request):
        pass


def generate_tokens(user):
    """
    Generates access and refresh tokens for a given user.
    """
    refresh = RefreshToken.for_user(user)
    return {
        "access": str(refresh.access_token),
        "refresh": str(refresh),
    }


def jwt_response(user, request=None):
    """
    Generates JWT response including access & refresh tokens and user data.
    """
    roles = ["ROLE_ADMIN"] if user.is_staff else ["ROLE_USER"]
    user_data = UserUsernameAndIdSerializer(user, context={"request": request}).data
    user_data.update({"roles": roles})

    tokens = generate_tokens(user)
    return {
        "success": True,
        "user": user_data,
        "access": tokens["access"],
        "refresh": tokens["refresh"],
    }


class IsAdminOrReadOnly(BasePermission):
    """
    Allows read-only access for all users, but restricts modification to admins.
    """
    def has_permission(self, request, view):
        return request.method in permissions.SAFE_METHODS or (request.user and request.user.is_staff)


class IsAdminOrOwnerOrReadOnly(BasePermission):
    """
    Allows read-only access for all users, but write access only for admins or the resource owner.
    """
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user and (request.user.is_staff or obj.user == request.user)
