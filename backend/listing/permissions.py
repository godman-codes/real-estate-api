from rest_framework import permissions

class IsRealtorPermission(permissions.DjangoModelPermissions):
    def has_permission(self, request, view):
        if not request.user.is_realtor:
            return False
        elif request.user.is_realtor:
            return True
        return super().has_permission(request, view)