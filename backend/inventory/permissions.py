from rest_framework.permissions import SAFE_METHODS, BasePermission


class StaffOrReadOnly(BasePermission):
    """
    Unauthenticated and authenticated users may GET (list/retrieve).
    POST, PUT, PATCH, DELETE require an authenticated Django staff user.
    """

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        user = request.user
        return bool(user and user.is_authenticated and user.is_staff)
