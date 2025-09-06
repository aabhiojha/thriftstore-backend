from rest_framework.permissions import BasePermission

class HasPermission(BasePermission):
    """
    Custom permission to check if user has specific permission.
    Usage: permission_classes = [HasPermission]
    permission_required = 'can_view_users'
    """
    permission_required = None
    
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
            
        if request.user.is_superuser:
            return True
            
        permission_code = getattr(view, 'permission_required', self.permission_required)
        if not permission_code:
            return False
            
        return request.user.has_permission(permission_code)

class CanManageUsers(HasPermission):
    permission_required = 'can_manage_users'

class CanViewUsers(HasPermission):
    permission_required = 'can_view_users'

class CanManageProducts(HasPermission):
    permission_required = 'can_manage_products'

class CanViewProducts(HasPermission):
    permission_required = 'can_view_products'

class CanManageOrders(HasPermission):
    permission_required = 'can_manage_orders'

class CanViewOrders(HasPermission):
    permission_required = 'can_view_orders'