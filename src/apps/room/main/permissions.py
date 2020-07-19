from rest_framework import permissions

class RoomMember(permissions.IsAuthenticated):
    def has_object_permission(self, request, view, obj):
        return request.user in obj.members.all()

class RoomAdmin(permissions.IsAuthenticated):
    def has_object_permission(self, request, view, obj):
        return request.user in obj.admins.all()

class RoomCreator(permissions.IsAuthenticated):
    def has_object_permission(self, request, view, obj):
        return request.user == obj.creator

class KickPermission(permissions.IsAuthenticated):
    def has_object_permission(self, request, view, obj):
        if request.user == obj.creator or request.user in obj.admins.all():
            return True
        return False