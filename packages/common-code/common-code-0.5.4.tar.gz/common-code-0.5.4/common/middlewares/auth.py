from common.rest_extend.response import RESTResponse, Results, FORBID_CODE
from django.utils.deprecation import MiddlewareMixin


class AuthMiddleware(MiddlewareMixin):
    def process_request(self, request):
        path = request.path
        if "login" not in path and path != "/":
            account = request.session.get("account", None)
            results = Results()
            if not account:
                results.describe = "no permission!!!"
                results.code = FORBID_CODE
                return RESTResponse(results)
            authorization = self.permissions(request, account)
            if not authorization:
                results.describe = "no permission!!!"
                results.code = FORBID_CODE
                return RESTResponse(results)

    def permissions(self, request, account):
        from tenant_auth.models import AuthTenant, AuthTenantRole, AuthPermission, AuthRolePermissions

        method = request.method
        path = request.path
        tenant = AuthTenant.objects.filter(account=account).first()
        if tenant:
            permission = AuthPermission.objects.filter(action=method, source_id=path).first()
            if permission:
                role_permissions = AuthRolePermissions.objects.filter(permission_id=permission.name).first()
                if role_permissions:
                    tenant_role = AuthTenantRole.objects.filter(
                        role_id=role_permissions.role_id, tenant_id=account
                    ).first()
                    if tenant_role:
                        return True

        return False
