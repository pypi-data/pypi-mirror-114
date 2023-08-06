from pydoc import locate


def str_to_class(path: str):
    """Generate class object from path.

    Example:
        if your class name is MyClass and located in my_app.models.MyClass then:

        path = "my_app.models.MyClass"
        my_class = to_class(path)

    :param path: String path of the module's class
    :return my_class: Object or None
    """
    try:
        my_class = locate(path)
    except ImportError:
        raise ValueError(f'Module `{path}` does not exist.')
    return my_class or None
