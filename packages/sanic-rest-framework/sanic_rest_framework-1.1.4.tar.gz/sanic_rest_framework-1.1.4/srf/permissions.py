"""
@Author：WangYuXiang
@E-mile：Hill@3io.cc
@CreateTime：2021/4/25 16:51
@DependencyLibrary：无
@MainFunction：无
@FileDoc： 
    permissions.py
    文件说明
@ChangeHistory:
    datetime action why
    example:
    2021/4/25 16:51 change 'Fix bug'
        
"""
from srf.exceptions import PermissionDenied
from srf.constant import ALL_METHOD


class BasePermission:
    async def has_permission(self, request, view):
        pass

    async def has_obj_permission(self, request, view, obj):
        pass


class ViewMapPermission(BasePermission):
    """
    仅供GeneralView及其子类视图的权限套件

    :param BasePermission: BasePermission
    """
    async def has_permission(self, request, view):
        permission_map = self.get_permission_map(view)
        method = request.method.lower()
        permissions = permission_map.get(method)
        if not request.user.has_permissions(permissions):
            raise PermissionDenied()

    def get_permission_map(self, view):
        permission_map = self.permission_map
        if hasattr(view, 'permission_map'):
            permission_map.update(view.permission_map)
        return permission_map

    @property
    def permission_map(self):
        permission_map = {method.lower(): () for method in ALL_METHOD}
        permission_map['all'] = ()
        return permission_map
