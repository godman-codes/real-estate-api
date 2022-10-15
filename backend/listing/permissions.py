from rest_framework import permissions

class IsRealtorPermission(permissions.DjangoModelPermissions):
    def has_permission(self, request, view):
        print(request.user.is_realtor)
        if not request.user.is_realtor:
            return False
        return super().has_permission(request, view)