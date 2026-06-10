from rest_framework.permissions import BasePermission
from .models import Company


class IsAdminUser(BasePermission):
    """
    Allows access only to users whose Company role is ADMIN.
    Returns 403 for authenticated CLIENT users.
    """

    def has_permission(self, request, view):
        return (
            request.user
            and request.user.is_authenticated
            and hasattr(request.user, 'company')
            and request.user.company.role == Company.Role.ADMIN
        )