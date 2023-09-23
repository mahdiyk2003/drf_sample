from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsTheAuthorOrIsAdminOrReadOnly(BasePermission):
    message = 'permission denied, you are not the owner'

    def has_permission(self, request, view):
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
        	return True
        return ((obj.author == request.user) or request.user.is_admin==True)
        
class IsAnAuthorOrIsAnAdminOrReadOnly(BasePermission):
    message = 'permission denied, you are not an author'
    def has_permission(self, request, view):
        return request.user.is_authenticated and (request.user.is_author or request.user.is_admin)