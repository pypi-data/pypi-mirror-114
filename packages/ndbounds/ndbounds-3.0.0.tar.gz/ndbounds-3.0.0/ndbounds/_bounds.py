# Copyright (C) 2021 Matthias Nadig


class NdBounds:
    """
    n-Dimensional Bounds
    """

    def __init__(self, bound_handler):
        self._bound_handler = bound_handler

    def __getitem__(self, key):
        return NdBounds(self._bound_handler[key])

    def __delitem__(self, key):
        # del self._bound_handler[key]
        raise NotImplementedError('To delete single bounds, use the delete(...)-method')

    def __setitem__(self, key, value):
        raise RuntimeError('Tried to modify bounds. Access by indexing is read-only.')

    def get_n_dims(self):
        """
        Returns the number of dimensions of the bounds
        (NOT OF THE NUMPY ARRAYS THEMSELVES)
        """
        return self._bound_handler.get_n_dims()

    def get_shape(self):
        """ Returns the shape of the Numpy array that contains the bounds """
        return self._bound_handler.get_shape()

    def get_bounds_se(self, copy=True):
        """ Returns the bounds in a Numpy array with format (start, end) """
        self._bound_handler = self._bound_handler.require_se()
        return self._bound_handler.get_bounds_se(copy=copy)

    def get_bounds_cw(self, copy=True):
        """ Returns the bounds in a Numpy array with format (center, width) """
        self._bound_handler = self._bound_handler.require_cw()
        return self._bound_handler.get_bounds_cw(copy=copy)

    def get_bounds_sw(self, copy=True):
        """ Returns the bounds in a Numpy array with format (start, width) """
        self._bound_handler = self._bound_handler.require_sw()
        return self._bound_handler.get_bounds_sw(copy=copy)

    def get_start(self, copy=True):
        """ Returns the start of the bounds """
        self._bound_handler = self._bound_handler.require_start()
        return self._bound_handler.get_start(copy=copy)

    def get_end(self, copy=True):
        """ Returns the end of the bounds """
        self._bound_handler = self._bound_handler.require_end()
        return self._bound_handler.get_end(copy=copy)

    def get_center(self, copy=True):
        """ Returns the center of the bounds """
        self._bound_handler = self._bound_handler.require_center()
        return self._bound_handler.get_center(copy=copy)

    def get_width(self, copy=True):
        """ Returns the width of the bounds """
        self._bound_handler = self._bound_handler.require_width()
        return self._bound_handler.get_width(copy=copy)

    def convert_to_se(self, inplace=False):
        """
        Makes sure, that the bounds are kept in format (start, end)
        Note 1: This method is meant for runtime improvements only. It might
        be useful, e.g., if the bounds are retrieved in SE format only and
        therefore an inplace conversion should be done, minimizing allocation
        of new arrays.
        Note 2: The inplace option refers to the underlying Numpy arrays,
        containing the bound information. Using the convert-method will
        always change the NdBounds instance inplace, by converting the
        bound handler.
        """
        self._bound_handler = self._bound_handler.convert_to_se(inplace=inplace)
        return self

    def convert_to_cw(self, inplace=False):
        """
        Makes sure, that the bounds are kept in format (center, width)
        Also see convert_to_se().
        """
        self._bound_handler = self._bound_handler.convert_to_cw(inplace=inplace)
        return self

    def require_cw(self):
        """ Makes sure that center and width are precomputed """
        self._bound_handler = self._bound_handler.require_cw()
        return self

    def require_se(self):
        """ Makes sure that start and end are precomputed """
        self._bound_handler = self._bound_handler.require_se()
        return self

    def require_sw(self):
        """ Makes sure that start and width are precomputed """
        self._bound_handler = self._bound_handler.require_sw()
        return self

    def require_secw(self):
        """ Makes sure that start, end, center and width are precomputed """
        self._bound_handler = self._bound_handler.require_secw()
        return self

    def require_start(self):
        """ Makes sure that start is precomputed """
        self._bound_handler = self._bound_handler.require_start()
        return self

    def require_end(self):
        """ Makes sure that end is precomputed """
        self._bound_handler = self._bound_handler.require_end()
        return self

    def require_center(self):
        """ Makes sure that center is precomputed """
        self._bound_handler = self._bound_handler.require_center()
        return self

    def require_width(self):
        """ Makes sure that width is precomputed """
        self._bound_handler = self._bound_handler.require_width()
        return self

    def scale_dimensions(self, factor_each_dim, inplace=False):
        """
        Scales the dimensions, the bounds refer to.
        Can be used e.g. when the signal the bounds - that are given in indices - refer to is downsampled.
        """
        if inplace:
            self._bound_handler = self._bound_handler.scale_dimensions(factor_each_dim)
            bounds_mod = self
        else:
            bounds_mod = NdBounds(self._bound_handler.copy())
            bounds_mod.scale_dimensions(factor_each_dim, inplace=True)
        return bounds_mod

    def scale_width(self, factor_each_dim, inplace=False):
        """
        Scales the width of the individual bounds.
        """
        self._bound_handler = self._bound_handler.require_width()
        if inplace:
            self._bound_handler = self._bound_handler.scale_width(factor_each_dim)
            bounds_mod = self
        else:
            bounds_mod = NdBounds(self._bound_handler.copy())
            bounds_mod.scale_width(factor_each_dim, inplace=True)
        return bounds_mod

    def add_offset(self, offset_each_dim, inplace=False):
        """
        Adds offset to the bounds.
        """
        if inplace:
            self._bound_handler = self._bound_handler.add_offset(offset_each_dim)
            bounds_mod = self
        else:
            bounds_mod = NdBounds(self._bound_handler.copy())
            bounds_mod.add_offset(offset_each_dim, inplace=True)
        return bounds_mod

    def apply_func_on_position(self, fn, inplace=False):
        """
        Applies a function to the position of the bounds, e.g. np.log(...).
        The function must have the following signature:
            fn(arr, out)
        The first argument "arr" is a Numpy array, on which the function will be applied,
        and the second one "out" must take an array of the same shape as "arr", into which
        the result will be written.
        """
        if inplace:
            self._bound_handler = self._bound_handler.apply_func_on_position(fn)
            bounds_mod = self
        else:
            bounds_mod = NdBounds(self._bound_handler.copy())
            bounds_mod.apply_func_on_position(fn, inplace=True)
        return bounds_mod

    def apply_func_on_width(self, fn, inplace=False):
        """
        Applies a function to the width of the bounds, also see apply_func_on_position().
        """
        self._bound_handler = self._bound_handler.require_width()
        if inplace:
            self._bound_handler = self._bound_handler.apply_func_on_width(fn)
            bounds_mod = self
        else:
            bounds_mod = NdBounds(self._bound_handler.copy())
            bounds_mod.apply_func_on_width(fn, inplace=True)
        return bounds_mod

    def copy(self):
        """ Returns a copy of itself """
        return NdBounds(self._bound_handler.copy())

    def delete(self, indices, axis=None):
        """ Deletes bounds at given indices """
        return NdBounds(self._bound_handler.delete(indices, axis=axis))
