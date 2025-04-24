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


def set_model_viewset_actions(base_cls, action_prefix=""):
    def new_partial_update(self, request, *args, **kwargs):
        kwargs["partial"] = True
        update = getattr(self, "update" + action_prefix)
        return update(request, *args, **kwargs)

    name_action_map = {
        "list": ModelViewSet.list,
        "retrieve": ModelViewSet.retrieve,
        "create": ModelViewSet.create,
        "update": ModelViewSet.update,
        "partial_update": new_partial_update,
        "destroy": ModelViewSet.destroy,
    }
    for name, func in name_action_map.items():
        setattr(base_cls, name + action_prefix, func)

    if not hasattr(base_cls, "perform_update"):
        setattr(base_cls, "perform_update", ModelViewSet.perform_update)
    if not hasattr(base_cls, "perform_create"):
        setattr(base_cls, "perform_create", ModelViewSet.perform_create)
    if not hasattr(base_cls, "perform_destroy"):
        setattr(base_cls, "perform_destroy", ModelViewSet.perform_destroy)

    return base_cls


def with_my_object_endpoint(
    pk_field_name=None,
    methods=["get", "put", "patch", "delete"],
    endpoint_name="my",
):
    """
    Adds a `my/` endpoint to a model's `ViewSet`, allowing interaction
    with current user's object.

    The object is resolved with `pk_field_name` from current user's model.
    For example, `profile.pk` covers direct or reverse relation to `Profile` model's pk.

    Overwrite `.perform_update()`, `.perform_destroy()`
    for `request.action == endpoint_name` to tweak the functionality.
    """

    def decorator(base_cls):
        method_action_map = {
            "GET": "retrieve",
            "PUT": "update",
            "PATCH": "partial_update",
            "DELETE": "destroy",
        }
        prefix = "_my_object"

        def endpoint(self, request):
            current_user = get_user_or_401(self, request)
            self.kwargs["pk"] = resolve_nested_attribute(current_user, pk_field_name)

            method_name = method_action_map[request.method] + prefix
            return getattr(self, method_name)(request, *self.args, **self.kwargs)

        endpoint.__name__ = endpoint_name
        my_action = action(detail=False, methods=methods)(endpoint)

        setattr(base_cls, endpoint_name, my_action)
        set_model_viewset_actions(base_cls, action_prefix=prefix)

        return base_cls

    return decorator


def with_my_list_endpoint(
    field_name,
    methods=["get", "post"],
    endpoint_name="my",
):
    """
    Adds a `my/` endpoint to a model's `ViewSet`, allowing interaction
    with current user's list of objects.

    The object is resolved with `field_name` from current user's model.
    For example, `subscribers` covers direct or reverse relation to `Subscriber` model.

    Overwrite `.perform_create()` or any method that interacts with `queryset`
    (except `.get_queryset()`) for `request.action == endpoint_name` to tweak the functionality.
    """

    def decorator(base_cls):
        method_action_map = {
            "GET": "list",
            "PUT": "create",
        }
        prefix = "_my_list"

        original_get_queryset = base_cls.get_queryset

        def new_get_queryset(self):
            current_action = getattr(self, "action", None)
            if current_action == endpoint_name:
                return getattr(self, "queryset" + prefix)
            return original_get_queryset(self)

        def endpoint(self, request):
            current_user = get_user_or_401(self, request)
            queryset = resolve_nested_attribute(current_user, field_name).all()
            setattr(self, "queryset" + prefix, queryset)

            method_name = method_action_map[request.method] + prefix
            return getattr(self, method_name)(request, *self.args, **self.kwargs)

        new_get_queryset.__name__ = "get_queryset"
        setattr(base_cls, "get_queryset", new_get_queryset)

        endpoint.__name__ = endpoint_name
        my_action = action(detail=False, methods=methods)(endpoint)
        setattr(base_cls, endpoint_name, my_action)

        set_model_viewset_actions(base_cls, action_prefix=prefix)
        return base_cls

    return decorator
