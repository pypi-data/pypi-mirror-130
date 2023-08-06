from __future__ import annotations

from abc import ABC
from math import ceil
from typing import TYPE_CHECKING

import numpy as np
from PIL import Image
from skimage.transform import resize
from tifffile import tifffile

from frmodel.base import CONSTS

if TYPE_CHECKING:
    from frmodel.base.D2.frame2D import Frame2D


class _Frame2DLoader(ABC):

    @classmethod
    def from_image(cls: 'Frame2D', file_path: str, scale:float = 1.0, scale_method=Image.NEAREST) -> 'Frame2D':
        """ Creates an instance using the file path.

        :param file_path: Path to image
        :param scale: The scaling to use
        :param scale_method: The method of scaling. See Image.resize

        :returns: Frame2D"""
        img = Image.open(file_path)
        img: Image.Image
        if scale != 1.0:
            img = img.resize([int(scale * s) for s in img.size], resample=scale_method)
        # noinspection PyTypeChecker
        ar = np.asarray(img)[..., :3]

        return cls.create(data=ar, labels=CONSTS.CHN.RGB)

    @classmethod
    def from_nxy_(cls: 'Frame2D', ar: np.ndarray, labels, xy_pos=(3, 4),  width=None, height=None) -> 'Frame2D':
        """ Rebuilds the frame with XY values. XY should be of integer values, otherwise, will be casted.

        Note that RGB channels SHOULD be on index 0, 1, 2 else some functions may break. However, can be ignored.

        The frame will be rebuild and all data will be retained, including XY.

        :param ar: The array to rebuild
        :param xy_pos: The positions of X and Y.
        :param labels: The labels of the new Frame2D, excluding XY
        :param height: Height of expected image, if None, Max will be used
        :param width: Width of expected image, if None, Max will be used

        :returns: Frame2D
        """
        max_y = height if height else np.max(ar[:,xy_pos[1]]) + 1
        max_x = width if width else np.max(ar[:,xy_pos[0]]) + 1

        fill = np.zeros(( ceil(max_y), ceil(max_x), ar.shape[-1]), dtype=ar.dtype)

        # Vectorized X, Y <- RGBXY... Assignment
        fill[ar[:, xy_pos[1]].astype(int),
             ar[:, xy_pos[0]].astype(int)] = ar[:]

        return cls.create(data=fill, labels=labels)

    @classmethod
    def from_image_spec(cls: 'Frame2D',
                        file_path_red: str,
                        file_path_green: str,
                        file_path_blue: str,
                        file_path_red_edge: str,
                        file_path_nir: str,
                        scale: float = 1.0) -> 'Frame2D':

        labels = [*cls.CHN.RGB, cls.CHN.RED_EDGE, cls.CHN.NIR]

        data = np.stack(
            [
                tifffile.imread(file_path_red),
                tifffile.imread(file_path_green),
                tifffile.imread(file_path_blue),
                tifffile.imread(file_path_red_edge),
                tifffile.imread(file_path_nir),
            ],
            axis=-1
        )

        if scale != 1.0:
            data = resize(data, output_shape=[int(scale * data.shape[0]),
                                              int(scale * data.shape[1])],
                          order=0)

        return cls.create(data=np.ma.masked_invalid(data, copy=False), labels=labels)

    def save(self: 'Frame2D', path: str):
        """ Saves the Frame2D underlying np.ndarray & dict as a .npz (.npy zip)

        The recommended extension is .npz
        """

        np.savez(path, data=self.data, labels=self.labels,
                 mask=self.data.mask if isinstance(self.data, np.ma.MaskedArray) else None)

    @classmethod
    def load(cls: 'Frame2D', path: str, mask=True):
        """ Loads the Frame2D from a .npz

        :param path: Path to the .npz
        :param mask: To mask the array. This should be disabled if MemoryError occurs.
        """
        files = np.load(path, allow_pickle=True)
        return cls.create(
            data=files['data'] if files['mask'] is None or not mask else np.ma.MaskedArray(data=files['data'], mask=files['mask']),
            labels=files['labels'].tolist())
