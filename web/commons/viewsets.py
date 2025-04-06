from rest_framework.decorators import action
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated

from .utils import resolve_nested_attribute


def get_user_or_401(self, request):
    permission = IsAuthenticated()
    if not permission.has_permission(request, self):
        self.permission_denied(
            request,
            message=getattr(permission, "message", None),
            code=getattr(permission, "code", None),
        )
    else:
        return request.user


def with_my_object_endpoint(
    pk_field_name=None,
    methods=["get", "put", "patch", "delete"],
):
    """
    Adds a custom 'my/' endpoint to a model's `ViewSet`, allowing interactions
    with an object related to the current user.
    """

    def decorator(base_cls):
        def partial_update_my(self, request, *args, **kwargs):
            kwargs["partial"] = True
            return self.update_my(request, *args, **kwargs)

        method_action_map = {
            "GET": "retrieve",
            "POST": "create",
            "PUT": "update",
            "PATCH": "partial_update",
            "DELETE": "destroy",
        }

        def my(self, request):
            current_user = get_user_or_401(self, request)
            self.kwargs["pk"] = resolve_nested_attribute(current_user, pk_field_name)

            method_name = method_action_map[request.method] + "_my"
            return getattr(self, method_name)(request, *self.args, **self.kwargs)

        my_action = action(detail=False, methods=methods)(my)

        setattr(base_cls, "my", my_action)
        setattr(base_cls, "retrieve_my", ModelViewSet.retrieve)

        setattr(base_cls, "create_my", ModelViewSet.create)
        if not hasattr(base_cls, "perform_create"):
            setattr(base_cls, "perform_create", ModelViewSet.perform_create)

        setattr(base_cls, "update_my", ModelViewSet.update)
        setattr(base_cls, "partial_update_my", partial_update_my)
        if not hasattr(base_cls, "perform_update"):
            setattr(base_cls, "perform_update", ModelViewSet.perform_update)

        setattr(base_cls, "destroy_my", ModelViewSet.destroy)
        if not hasattr(base_cls, "perform_destroy"):
            setattr(base_cls, "perform_destroy", ModelViewSet.perform_destroy)

        return base_cls

    return decorator
