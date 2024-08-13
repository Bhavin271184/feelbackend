from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import BasePermission

class IsAuthenticatedForPostPatchDelete(BasePermission):
    def has_permission(self, request, view):
        if request.method in ['POST', 'PATCH', 'DELETE']:
            jwt_auth = JWTAuthentication()
            user_and_auth = jwt_auth.authenticate(request)
            if user_and_auth is not None:
                user, _ = user_and_auth
                return user is not None
            return False
        return True