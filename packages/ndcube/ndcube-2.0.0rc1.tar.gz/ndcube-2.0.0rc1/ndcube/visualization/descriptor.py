class PlotterDescriptor:
    def __init__(self, default_type=None):
        self._default_type = default_type

    def __set_name__(self, owner, name):
        """
        This function is called when the class the descriptor is attached to is initialized.

        The *class* and not the instance.
        """
        # property name is the name of the attribute on the parent class
        # pointing at an instance of this descriptor.
        self._property_name = name
        # attribute name is the name of the attribute on the parent class where
        # the data is stored.
        self._attribute_name = f"_{name}"

    def __get__(self, obj, objtype=None):
        if obj is None:
            return

        if getattr(obj, self._attribute_name, None) is None:

            # We special case the default MatplotlibPlotter so that we can
            # delay the import of matplotlib until the plotter is first
            # accessed.
            if self._default_type == "mpl_plotter":
                try:
                    from ndcube.visualization.mpl_plotter import MatplotlibPlotter
                except ImportError as e:
                    raise ImportError(
                        "Matplotlib can not be imported, so the default plotting "
                        "functionality is disabled. Please install matplotlib.") from e

                self.__set__(obj, MatplotlibPlotter)

            elif self._default_type is not None:
                self.__set__(obj, self._default_type)
            else:
                # If we have no default type then just return None
                return

        return getattr(obj, self._attribute_name)

    def __set__(self, obj, value):
        if not isinstance(value, type):
            raise TypeError("NDCube.plotter can only be set with an uninitialised plotter object.")
        setattr(obj, self._attribute_name, value(obj))
