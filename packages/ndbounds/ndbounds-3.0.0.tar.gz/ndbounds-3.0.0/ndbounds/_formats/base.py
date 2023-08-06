# Copyright (C) 2021 Matthias Nadig

import numpy as np


class BoundFormatHandler:
    """
    A class that serves as interface to the actual array containing the bounds
    """

    def __init__(self, n_dims, shape):
        self._n_dims = n_dims
        self._shape = shape

    def __getitem__(self, key):
        bounds_extracted = self._getitem(key)
        if bounds_extracted.get_n_dims() != self.get_n_dims() or \
            len(bounds_extracted.get_shape()) == 0:
            raise RuntimeError('Invalid access of items in {}-dimensional bounds of shape {} using key: {}'.format(
                self.get_n_dims(), self.get_shape(), key
            ))
        return bounds_extracted

    def require_se(self):
        return self._require_se()

    def require_cw(self):
        return self._require_cw()

    def require_sw(self):
        return self._require_sw()

    def require_secw(self):
        return self._require_secw()

    def require_start(self):
        return self._require_start()

    def require_end(self):
        return self._require_end()

    def require_center(self):
        return self._require_center()

    def require_width(self):
        return self._require_width()

    def get_n_dims(self):
        return self._n_dims

    def get_shape(self):
        return self._shape

    def convert_to_se(self, inplace=False):
        return self._convert_to_se(inplace=inplace)

    def convert_to_cw(self, inplace=False):
        return self._convert_to_cw(inplace=inplace)

    def convert_to_sw(self, inplace=False):
        return self._convert_to_cw(inplace=inplace)

    def get_bounds_se(self, copy=True):
        return self._get_bounds_se(copy=copy)

    def get_bounds_cw(self, copy=True):
        return self._get_bounds_cw(copy=copy)

    def get_bounds_sw(self, copy=True):
        _raise_not_overwritten(self)

    def get_center(self, copy=True):
        return self._get_center(copy=copy)

    def get_width(self, copy=True):
        return self._get_width(copy=copy)

    def get_start(self, copy=True):
        return self._get_start(copy=copy)

    def get_end(self, copy=True):
        return self._get_end(copy=copy)

    def scale_dimensions(self, factor_each_dim):
        factor_each_dim = self._reshape_input_for_application_to_each_bounds(factor_each_dim)
        return self._scale_dimensions(factor_each_dim)

    def scale_width(self, factor_each_dim):
        factor_each_dim = self._reshape_input_for_application_to_each_bounds(factor_each_dim)
        return self._scale_width(factor_each_dim)

    def add_offset(self, offset_each_dim):
        offset_each_dim = self._reshape_input_for_application_to_each_bounds(offset_each_dim)
        return self._add_offset(offset_each_dim)

    def apply_func_on_position(self, fn):
        return self._apply_func_on_position(fn)

    def apply_func_on_width(self, fn):
        return self._apply_func_on_width(fn)

    def copy(self):
        return self._copy()

    def delete(self, indices, axis=None):
        return self._delete(indices, axis=axis)

    def _require_se(self):
        _raise_not_overwritten(self)

    def _require_cw(self):
        _raise_not_overwritten(self)

    def _require_sw(self):
        _raise_not_overwritten(self)

    def _require_secw(self):
        _raise_not_overwritten(self)

    def _require_start(self):
        _raise_not_overwritten(self)

    def _require_end(self):
        _raise_not_overwritten(self)

    def _require_center(self):
        _raise_not_overwritten(self)

    def _require_width(self):
        _raise_not_overwritten(self)

    def _convert_to_se(self, inplace=False):
        _raise_not_overwritten(self)

    def _convert_to_cw(self, inplace=False):
        _raise_not_overwritten(self)

    def _convert_to_sw(self, inplace=False):
        _raise_not_overwritten(self)

    def _apply_func_on_position(self, fn):
        _raise_not_overwritten(self)

    def _apply_func_on_width(self, fn):
        _raise_not_overwritten(self)

    def _copy(self):
        _raise_not_overwritten(self)

    def _get_bounds_se(self, copy=True):
        _raise_not_overwritten(self)

    def _get_bounds_cw(self, copy=True):
        _raise_not_overwritten(self)

    def _get_bounds_sw(self, copy=True):
        _raise_not_overwritten(self)

    def _get_start(self, copy=True):
        _raise_not_overwritten(self)

    def _get_end(self, copy=True):
        _raise_not_overwritten(self)

    def _get_center(self, copy=True):
        _raise_not_overwritten(self)

    def _get_width(self, copy=True):
        _raise_not_overwritten(self)

    def _add_offset(self, offset_each_dim):
        _raise_not_overwritten(self)

    def _scale_dimensions(self, factor_each_dim):
        _raise_not_overwritten(self)

    def _scale_width(self, factor_each_dim):
        _raise_not_overwritten(self)

    def _delete(self, indices, axis=None):
        _raise_not_overwritten(self)

    def _getitem(self, key):
        _raise_not_overwritten(self)

    def _reshape_input_for_application_to_each_bounds(self, arr):
        arr = np.asarray(arr)
        if arr.shape == (self.get_n_dims(),):
            # Repeat the array for each bounds
            for n_elements in reversed(self.get_shape()):
                arr = np.repeat(arr[np.newaxis], n_elements, axis=0)
        elif arr.shape == self.get_shape()+(self.get_n_dims(),):
            # Shape already as required for calculations
            pass
        else:
            raise ValueError('Bad shape for input array. Expected {}, got {}.'.format(
                '{} or {}'.format((self.get_n_dims(),), self.get_shape()+(self.get_n_dims(),)),
                arr.shape
            ))

        return arr

    def _raise_not_possible_for_child(self):
        raise RuntimeError(
            'Method not possible for child (type = {}). '.format(type(self)) +
            'This error occurs usually, if the NdBounds class did not request the required attributes ' +
            'from the bound format handler.')

    def _pack_se(self, start, end):
        return NdBoundsSE(start=start, end=end)

    def _pack_cw(self, center, width):
        return NdBoundsCW(center=center, width=width)

    def _pack_sw(self, start, width):
        return NdBoundsSW(start=start, width=width)

    def _pack_sec(self, start, end, center):
        return NdBoundsSEC(start=start, end=end, center=center)

    def _pack_sew(self, start, end, width):
        return NdBoundsSEW(start=start, end=end, width=width)

    def _pack_scw(self, start, center, width):
        return NdBoundsSCW(start=start, center=center, width=width)

    def _pack_ecw(self, end, center, width):
        return NdBoundsECW(end=end, center=center, width=width)

    def _pack_secw(self, start, end, center, width):
        return NdBoundsSECW(start=start, end=end, center=center, width=width)


# Imports must be below the base class, since it will will be imported by subclasses
from .format_se import NdBoundsSE
from .format_cw import NdBoundsCW
from .format_sw import NdBoundsSW
from .format_sec import NdBoundsSEC
from .format_sew import NdBoundsSEW
from .format_scw import NdBoundsSCW
from .format_ecw import NdBoundsECW
from .format_secw import NdBoundsSECW


def _raise_not_overwritten(inst):
    raise RuntimeError('Method should be overwritten by child (type = {})'.format(type(inst)))
