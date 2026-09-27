from rest_framework.permissions import BasePermission


class IsOwnerOrAdmin(BasePermission):
    """
    Object-level permission: allow access only to the owner of the object
    or a staff/admin user.
    """

    def has_object_permission(self, request, view, obj):
        if request.user.is_staff:
            return True
        # Works for models with .farmer field (Crop, SoilData)
        owner = getattr(obj, 'farmer', None)
        if owner is None:
            owner = getattr(obj, 'user', None)
        return owner == request.user
