from rest_framework.permissions import BasePermission


class PublicActionsOrAuthenticated(BasePermission):
    """
    Allows unauthenticated access only to the actions named in the view's
    ``public_actions`` attribute (e.g. a customer placing an order or a
    reservation). Every other action requires an authenticated user.
    """

    def has_permission(self, request, view):
        public_actions = set(getattr(view, 'public_actions', []))
        if getattr(view, 'action', None) in public_actions:
            return True
        return bool(request.user and request.user.is_authenticated)


class IsStaffUser(BasePermission):
    """Authenticated staff/admin users only (used for management endpoints)."""

    def has_permission(self, request, view):
        user = request.user
        return bool(
            user
            and user.is_authenticated
            and (user.is_staff or getattr(user, 'role', '') in ('admin', 'manager', 'waiter', 'kitchen'))
        )
