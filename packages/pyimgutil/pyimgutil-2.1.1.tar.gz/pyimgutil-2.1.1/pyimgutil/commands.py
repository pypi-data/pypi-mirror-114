"""Perform the actual command specified by the user.

Copyright (C) 2021 emerac

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.

"""
import logging
from pathlib import Path
from typing import List, Union

from PIL import Image


logger = logging.getLogger(__name__)
SEARCH_EXTS = [".bmp", ".gif", ".ico", ".jpeg", ".jpg", ".png", ".ppm"]
SAVE_EXTS = ["bmp", "gif", "ico", "jpeg", "png", "ppm"]


def crop_image(
    image: Image,
    left: Union[int, None],
    right: Union[int, None],
    upper: Union[int, None],
    bottom: Union[int, None],
) -> Image:
    """Remove unwanted portions of an image.

    Parameters
    ----------
    image : :obj:`PIL.Image`
        The image to be cropped.
    left : int or None
        The left crop boundary, in pixels.
    right : int or None
        The right crop boundary, in pixels.
    upper : int or None
        The upper crop boundary, in pixels.
    bottom : int or None
        The bottom crop boundary, in pixels.

    Returns
    -------
    :obj:`PIL.Image`
        The cropped image.

    """
    if left is None:
        left = 0
    if right is None:
        right = image.width
    if upper is None:
        upper = 0
    if bottom is None:
        bottom = image.height
    if left >= right:
        raise ValueError(
            f"Error: the left ({left}) and right ({right}) boundaries are "
            "inverted. The left boundary must be less than the right "
            "boundary. Note that the image's dimensions are used in place of "
            "unspecified boundaries."
        )
    if upper >= bottom:
        raise ValueError(
            f"Error: the upper ({upper}) and bottom ({bottom}) boundaries "
            "are inverted. The upper boundary must be less than the bottom "
            "boundary. Note that the image's dimensions are used in place of "
            "unspecified boundaries."
        )
    return image.crop((left, upper, right, bottom))


def get_output_dir(output: Union[Path, None]) -> Path:
    """Set the path to the output and create the directory, if needed.

    Parameters
    ----------
    output : :obj:`pathlib.Path`
        The output argument specified by the user.

    Returns
    -------
    :obj:`pathlib.Path`
        The directory in which output should be placed.

    """
    if output is None:
        path = Path.cwd()
    else:
        path = output
        path.mkdir(exist_ok=True)
    return path


def get_valid_files(path: Path, recursive: bool) -> List[Path]:
    """Retrieve the paths to supported image files in the input path.

    Parameters
    ----------
    path : :obj:`pathlib.Path`
        The path being considered.
    recursive : bool
        Whether or not to search subdirectories.

    Returns
    -------
    list of :obj:`pathlib.Path`
        The paths of the supported image files that were found.

    """
    valid_files = []
    if not path.exists():
        raise ValueError(
            f"Error: An input path provided ({path}) does not exist. Please "
            "check the path and try again."
        )
    if path.is_file() and path.suffix.lower() in SEARCH_EXTS:
        valid_files.append(path)
    else:
        if recursive:
            contents = path.rglob("*")
        else:
            contents = path.glob("*")
        for subpath in contents:
            if subpath.is_file() and subpath.suffix.lower() in SEARCH_EXTS:
                valid_files.append(subpath)
    return valid_files


def mod_ext(path: Path, ext: str) -> Path:
    """Replace a filepath's extension.

    Parameters
    ----------
    path : :obj:`pathlib.Path`
        The filepath to modify.
    ext : str
        The desired extension.

    Returns
    -------
    path : :obj:`pathlib.Path`
        The modified filepath.

    """
    if ext.lower() == "jpeg":
        out_ext = ".jpg"
    else:
        out_ext = "." + ext.lower()
    out_path = path.parent / (path.stem + out_ext)
    return out_path


def mod_name(path: Path, text: str, prepend: bool) -> Path:
    """Add text to the beginning or end of the name part of a filepath.

    Parameters
    ----------
    path : :obj:`pathlib.Path`
        The filepath to modify.
    text : str
        The text to add.
    prepend : bool
        Whether to prepend or append the text.

    Returns
    -------
    path : :obj:`pathlib.Path`
        The modified filepath.

    """
    if prepend:
        return (path.parent / (text + path.name))
    else:
        return (path.parent / (path.stem + text + path.suffix))


def mod_parent(path: Path, parent: Path) -> Path:
    """Replace a filepath's parent.

    Parameters
    ----------
    path : :obj:`pathlib.Path`
        The filepath to modify.
    parent : :obj:`pathlib.Path`
        The desired parent.

    Returns
    -------
    path : :obj:`pathlib.Path`
        The modified filepath.

    """
    return (parent / path.name)


def resize_image(
    image: Image,
    width: Union[int, None],
    height: Union[int, None],
    scale: Union[float, None],
    ratio: bool,
) -> Image:
    """Resize an image.

    Parameters
    ----------
    image : :obj:`PIL.Image`
        The image to be resized.
    width : int or None
        The width, in pixels, of the resulting image.
    height : int or None
        The height, in pixels, of the resulting image.
    scale : float or None
        The amount to scale the image (respects aspect ratio).
    ratio : bool
        Whether or not to retain the original image's aspect ratio.

    Returns
    -------
    :obj:`PIL.Image`
        The resized image.

    """
    re_width = width
    re_height = height
    if scale is not None:
        re_width = int(image.width * scale)
        re_height = int(image.height * scale)
    elif ratio:
        ratio = image.width / image.height
        if width is not None:
            re_height = int(width / ratio)
        if height is not None:
            re_width = int(ratio * height)
    else:
        if width is None:
            re_width = image.width
        if height is None:
            re_height = image.height
    resized_image = image.resize((re_width, re_height))
    return resized_image


def rotate_image(image: Image, angle: int, fill: bool) -> Image:
    """Rotate an image.

    Parameters
    ----------
    image : :obj:`PIL.Image`
        The image to be resized.
    angle : int
        The number of degrees to rotate the image counter clockwise
    fill : bool
        Whether or not to fill open areas with black pixels.

    Returns
    -------
    :obj:`PIL.Image`
        The rotated image.

    """
    if angle is not None and fill:
        mod_im = image.rotate(angle, expand=True, fillcolor="#000000")
    elif angle is not None:
        mod_im = image.rotate(angle, expand=True)
    else:
        mod_im = image
    return mod_im


def transpose_image(image: Image) -> Image:
    """Flip an image horizontally.

    Parameters
    ----------
    image : :obj:`PIL.Image`
        The image to be transposed.

    Returns
    -------
    :obj:`PIL.Image`
        The transposed image.

    """
    return image.transpose(0)


def save_image(
    im: Image,
    path: Path,
    quality: Union[int, None],
    force: bool,
) -> None:
    """Save the image to the specified path.

    Parameters
    ----------
    image : :obj:`PIL.Image`
        The image to be saved.
    path : :obj:`pathlib.Path`
        The path to which the image shall be saved.
    quality : int or None
        The quality of the saved image (only for compressed images).
    force : bool
        Whether to raise exceptions in the case of file conflicts.

    Raises
    ------
    FileExistsError
        If the save path already exists.

    """
    if path.exists() and not force:
        raise FileExistsError(
            f"Error: the processed image could not be saved to '{path}' "
            "because a file already exists in that location. If you would "
            "like to overwrite the conflicting file, use the 'force' argument."
        )
    if path.exists() and force:
        logger.warning(
            f"An existing file ({path}) will be overwritten because "
            "the 'force' argument has been used."
        )

    if im.mode in ["RGBA", "P"] and path.suffix[1:].lower() == "jpg":
        logger.debug("Converting image mode to RGB for JPEG save format.")
        im = im.convert("RGB")
    if im.mode == "P" and path.suffix[1:].lower() == "ppm":
        logger.debug("Converting image mode to RGB for PPM save format.")
        im = im.convert("RGB")

    try:
        if quality is None:
            im.save(path, quality="keep")
            logger.debug("File saved with 'keep' quality.")
        else:
            im.save(path, quality=quality)
            logger.debug(f"File saved with '{quality}' quality.")
    except ValueError:
        logger.warning(
            "The file could not be saved with 'keep' quality. Saving with "
            "recommended highest quality."
        )
        im.save(path, quality=95)
