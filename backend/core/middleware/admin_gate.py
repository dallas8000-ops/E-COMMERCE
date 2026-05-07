"""Restrict ``/admin/`` to superusers only (shop staff keep storefront + staff dashboard)."""

from django.core.exceptions import PermissionDenied


class AdminSuperuserOnlyMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        path = request.path
        if path.startswith('/admin/'):
            user = request.user
            if user.is_authenticated and not user.is_superuser:
                raise PermissionDenied('Django admin is limited to superusers.')

        return self.get_response(request)
