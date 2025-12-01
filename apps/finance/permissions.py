from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsOwnerOrReadOnlyGlobal(BasePermission):
    def has_object_permission(self, request, view, obj):
        # Read is allowed for everything
        if request.method in SAFE_METHODS:
            return True

        # Write is allowed only for user's own categories
        return obj.user == request.user
