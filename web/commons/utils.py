def resolve_nested_attribute(obj, model_path=None):
    """
    Traverses the attribute's path of an object and returns the last property.

    Relations support:
        - Direct: `created_by` becomes obj.created_by
        - Nested: `activity.created_by` becomes obj.activity.created_by
        - Itself: if `model_path` is None, returns the object itself
    """
    if model_path is None:
        return obj

    for field in model_path.split("."):
        obj = getattr(obj, field)

    return obj
