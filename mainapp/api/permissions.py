from rest_framework import permissions


class IsBotAuthor(permissions.BasePermission):
    message = "Only the authors can edit and delete bots"

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.add_by_user == request.user


class IsCommentLikeAuthor(permissions.BasePermission):
    message = "Only the authors can edit and delete comments"

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.author == request.user


class CollectionPermissions(permissions.BasePermission):
    message = "Only the authors can edit and delete collections"

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        elif request.method == "POST":
            return request.user.is_authenticated
        else:
            return obj.collection_author == request.user
