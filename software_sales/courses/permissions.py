from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsOwnerOrStaff(BasePermission):
    """Allow staff or the user related to an object."""

    def has_object_permission(self, request, view, obj):
        if request.user.is_staff:
            return True
        owner = getattr(obj, "usuario", None) or getattr(obj, "criado_por", None)
        return owner == request.user


class IsCourseOwnerOrReadOnly(BasePermission):
    """Allow authenticated reads and restrict writes to the course owner or staff."""

    def has_object_permission(self, request, view, obj):
        return (
            request.method in SAFE_METHODS
            or request.user.is_staff
            or obj.criado_por == request.user
        )
