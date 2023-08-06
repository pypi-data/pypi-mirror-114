"""Parse and error-check command-line arguments.

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
import argparse
import logging
from pathlib import Path
from typing import List, Optional, Union

import pyimgutil
from pyimgutil import commands


logger = logging.getLogger(__name__)


def check_conflicts(args: argparse.Namespace) -> None:
    """Check for invalid argument combinations.

    Parameters
    ----------
    args : :obj:`argparse.Namespace`
        The namedtuple-like object containing parsed arguments.

    Returns
    -------
    None

    Raises
    ------
    ValueError
        If an invalid combination of arguments is found.

    """
    if args.command is None:
        raise ValueError("Error: no command specified.")
    if args.command == "resize":
        w, h = (args.width, args.height)
        if args.ratio and w is None and h is None:
            raise ValueError(
                "Error: when using the ratio argument, either the width "
                "argument or the height argument must also be used."
            )
        if args.ratio and w is not None and h is not None:
            raise ValueError(
                "Error: the width, height, and ratio arguments cannot all "
                "three be used together. Try ratio with just width or just "
                "height.",
            )
        if args.scale is not None and (w is not None or h is not None):
            raise ValueError(
                "Error: the scale argument cannot be used with either the "
                "width argument or the height argument."
            )


def check_crop(
    left: Union[int, None],
    right: Union[int, None],
    upper: Union[int, None],
    bottom: Union[int, None],
) -> None:
    """Check for crop arguments that would cause errors.

    Parameters
    ----------
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
    None

    Raises
    ------
    ValueError
        If the arguments would result in a crop error.

    """
    if left is not None and right is not None and left >= right:
        raise ValueError(
            f"Error: the left argument ({left}) cannot be greater than "
            f"or equal to the right argument ({right})."
        )
    if upper is not None and bottom is not None and upper >= bottom:
        raise ValueError(
            f"Error: the upper argument ({upper}) cannot be greater than "
            f"or equal to the bottom argument ({bottom})."
        )


def check_format(ext: str) -> None:
    """Check the format argument for a supported format.

    Parameters
    ----------
    ext : str
        The image format that has been requested.

    Returns
    -------
    None

    Raises
    ------
    ValueError
        If the given format does not match a supported format.

    """
    if ext.lower() not in commands.SAVE_EXTS:
        raise ValueError(
            f"Error: the format argument ({ext}) does not match a supported "
            f"format ({', '.join(commands.SAVE_EXTS)})."
        )


def check_output(path: Path) -> None:
    """Check the output argument for a valid path.

    Parameters
    ----------
    path : :obj:`pathlib.Path`
        The directory in which to place output.

    Returns
    -------
    None

    Raises
    ------
    ValueError
        If the path is a file or its parent directory does not exist.

    """
    if path.is_file():
        raise ValueError(
            f"Error: the output argument ({path}) is an existing file. "
            "The output location must be an existing directory or a directory "
            "that can be created."
        )
    if not path.parent.is_dir():
        raise ValueError(
            f"Error: the output argument ({path}) does not exist and cannot "
            "be created because its parent directory also does not exist. Try "
            "creating the parent directory or choosing a new directory."
        )


def check_quality(quality: int) -> None:
    """Check the quality argument for a valid value.

    Parameters
    ----------
    quality : int
        The image quality used when saving JPEGs.

    Returns
    -------
    None

    Raises
    ------
    ValueError
        If the quality argument is outside of the acceptable range.

    """
    if quality < 0 or quality > 100:
        raise ValueError(
            f"Error: the quality argument ({quality}) must be between 0 and "
            "100."
        )


def check_resize(
    width: Union[int, None],
    height: Union[int, None],
    scale: Union[float, None],
) -> None:
    """Check for resize arguments that would cause errors.

    Parameters
    ----------
    width : int or None
        The width to which the image should be resized.
    height : int or None
        The height to which the image should be resized.
    scale : float or None
        The factor by which to scale the image.

    Returns
    -------
    None

    Raises
    ------
    ValueError
        If the arguments would result in a resize error.

    """
    if height is not None and height <= 0:
        raise ValueError(
            f"Error: the height argument ({height}) cannot be less than or "
            "equal to zero."
        )
    if width is not None and width <= 0:
        raise ValueError(
            f"Error: the width argument ({width}) cannot be less than or "
            "equal to zero."
        )
    if scale is not None and scale <= 0:
        raise ValueError(
            f"Error: the scale argument ({scale}) cannot be less than or "
            "equal to zero."
        )


def configure_logging(verbose: int) -> None:
    """Set the log handler and level based on user preferences.

    Parameters
    ----------
    verbose : int
        Represents the log level to output.

    Returns
    -------
    None

    """
    if verbose == 0:
        pyimgutil.logger.addHandler(pyimgutil.null_handler)
    else:
        pyimgutil.logger.addHandler(pyimgutil.stream_handler)
        if verbose == 1:
            pyimgutil.logger.setLevel(logging.INFO)
        elif verbose >= 2:
            pyimgutil.logger.setLevel(logging.DEBUG)


def parse_args(argv: Optional[List[str]] = None) -> argparse.Namespace:
    """Parse function or sys.argv arguments.

    Parameters
    ----------
    argv : list of str or None
        Arguments manually provided to the parser (only for testing).

    Returns
    -------
    :obj:`argparse.Namespace`
        The arguments parsed into a namedtuple-like object.

    """
    # Set up the parser that actually does the parsing.
    primary_parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description=(
            "Simple individual or batch image processing."
            "\n\n"
            "Supported image formats: BMP, GIF, ICO, JPEG, PNG, PPM"
        ),
        epilog=(
            "pyimgutil Copyright (C) 2021 emerac"
            "\n\n"
            "This program comes with ABSOLUTELY NO WARRANTY. This is free\n"
            "software, and you are welcome to redistribute it under certain\n"
            "conditions. You should have received a copy of the GNU General\n"
            "Public License along with this program. If not, see:\n"
            "<https://www.gnu.org/licenses/gpl-3.0.txt>."
        ),
    )

    # Set up a parser that holds arguments common to all commands.
    global_parser = argparse.ArgumentParser(
        add_help=False,
    )
    global_parser.add_argument(
        "input",
        help="The path to the file(s) and/or directories to process.",
        type=Path,
        nargs="+",
    )
    global_parser.add_argument(
        "-o",
        "--output",
        help=(
            "Choose the directory in which to place processed image files. If "
            "the last directory in the path does not exist, it will be "
            "created."
        ),
        type=Path,
        metavar="PATH",
    )
    global_parser.add_argument(
        "-p",
        "--prepend",
        help="Add text to the beginning of each output filename.",
        metavar="TEXT",
    )
    global_parser.add_argument(
        "-a",
        "--append",
        help="Add text to the end of each output filename.",
        metavar="TEXT",
    )
    global_parser.add_argument(
        "--quality",
        help="Set the image quality (0-100) to use when saving JPEGs.",
        type=int,
        metavar="NUMBER",
    )
    global_parser.add_argument(
        "--format",
        help="Choose the image format to output.",
        metavar="EXTENSION",
    )
    global_parser.add_argument(
        "--recursive",
        help="Search input directories recursively for supported image files.",
        action="store_true",
    )
    global_parser.add_argument(
        "--force",
        help=(
            "Allow processed image files to overwrite conflicting files in "
            "the output directory."
        ),
        action="store_true",
    )
    global_parser.add_argument(
        "-v",
        "--verbose",
        help="Provide log output. This argument can be repeated.",
        action="count",
        default=0,
    )

    # Each command's arguments will be handled by its own subparser.
    subparsers = primary_parser.add_subparsers(
        dest="command",
        help="Run `%(prog)s {argument} -h` to view argument help.",
    )

    # Convert.
    subparsers.add_parser(
        "convert",
        parents=[global_parser],
        formatter_class=argparse.RawDescriptionHelpFormatter,
        help="Change the format of an image.",
        description=(
            "To convert an image to a different format, use the format\n"
            "argument listed below followed by the desired format (BMP, GIF,\n"
            "ICO, JPEG, PNG, PPM)."
            "\n\n"
            "The format argument is available for other commands as well,\n"
            "but this command is suitable for when changing the format is\n"
            "the only desired process."
            "\n\n"
            "   ---"
            "\n\n"
            "By default, this program does the following:\n"
            "    - places output in the current working directory\n"
            "    - does not modify filenames\n"
            "    - skips file conflicts"
            "\n\n"
            "The above defaults can be changed, however, by using optional\n"
            "arguments listed below."
        ),
    )

    # Crop.
    crop_subparser = subparsers.add_parser(
        "crop",
        parents=[global_parser],
        formatter_class=argparse.RawDescriptionHelpFormatter,
        help="Remove unwanted outer areas from an image.",
        description=(
            "To crop an image, use the left, right, upper, and bottom\n"
            "arguments listed below. The area bounded by these arguments\n"
            "will remain after the crop. All boundaries are taken with\n"
            "respect to the top-left corner of the image. Lastly, if a\n"
            "boundary is not specified, no crop will be performed on that\n"
            "side of the image."
            "\n\n"
            "   ---"
            "\n\n"
            "By default, this program does the following:\n"
            "    - places output in the current working directory\n"
            "    - does not modify filenames\n"
            "    - skips file conflicts"
            "\n\n"
            "The above defaults can be changed, however, by using optional\n"
            "arguments listed below."
        ),
    )
    crop_group = crop_subparser.add_argument_group(
        "optional crop arguments",
    )
    crop_group.add_argument(
        "-l",
        "--left",
        help="Specify the left crop boundary, in pixels.",
        type=int,
        metavar="NUMBER",
    )
    crop_group.add_argument(
        "-r",
        "--right",
        help="Specify the right crop boundary, in pixels.",
        type=int,
        metavar="NUMBER",
    )
    crop_group.add_argument(
        "-u",
        "--upper",
        help="Specify the upper crop boundary, in pixels.",
        type=int,
        metavar="NUMBER",
    )
    crop_group.add_argument(
        "-b",
        "--bottom",
        help="Specify the bottom crop boundary, in pixels.",
        type=int,
        metavar="NUMBER",
    )

    # Resize.
    resize_subparser = subparsers.add_parser(
        "resize",
        parents=[global_parser],
        formatter_class=argparse.RawDescriptionHelpFormatter,
        help="Change the dimensions of an image.",
        description=(
            "To resize an image, use the height, width, scale, and ratio\n"
            "arguments listed below."
            "\n\n"
            "   ---"
            "\n\n"
            "By default, this program does the following:\n"
            "    - places output in the current working directory\n"
            "    - does not modify filenames\n"
            "    - skips file conflicts"
            "\n\n"
            "The above defaults can be changed, however, by using optional\n"
            "arguments listed below."
        ),
    )
    resize_group = resize_subparser.add_argument_group(
        "optional resize arguments",
    )
    resize_group.add_argument(
        "-H",
        "--height",
        help="Choose the pixel height to which the image shall be resized.",
        type=int,
        metavar="NUMBER",
    )
    resize_group.add_argument(
        "-W",
        "--width",
        help="Choose the pixel width to which the image shall be resized.",
        type=int,
        metavar="NUMBER",
    )
    resize_group.add_argument(
        "-s",
        "--scale",
        help=(
            "Proportionally scale the image's dimensions by a factor "
            "(ex. 0.74, 2.1, etc.)."
        ),
        type=float,
        metavar="NUMBER",
    )
    resize_group.add_argument(
        "-r",
        "--ratio",
        help="Maintain the image's original aspect ratio.",
        action="store_true",
    )

    # Rotate.
    rotate_subparser = subparsers.add_parser(
        "rotate",
        parents=[global_parser],
        formatter_class=argparse.RawDescriptionHelpFormatter,
        help="Reorient an image.",
        description=(
            "To rotate an image, use the angle and fill arguments listed\n"
            "below."
            "\n\n"
            "   ---"
            "\n\n"
            "By default, this program does the following:\n"
            "    - places output in the current working directory\n"
            "    - does not modify filenames\n"
            "    - skips file conflicts"
            "\n\n"
            "The above defaults can be changed, however, by using optional\n"
            "arguments listed below."
        ),
    )
    rotate_group = rotate_subparser.add_argument_group(
        "optional rotate arguments",
    )
    rotate_group.add_argument(
        "-A",
        "--angle",
        help="The number of degrees counter clockwise by which to rotate.",
        type=int,
        metavar="NUMBER",
    )
    rotate_group.add_argument(
        "--fill",
        help="Fill open areas with black pixels.",
        action="store_true",
    )

    # Transpose.
    subparsers.add_parser(
        "transpose",
        parents=[global_parser],
        formatter_class=argparse.RawDescriptionHelpFormatter,
        help="Flip an image horizontally.",
        description=(
            "Any images included as input will be transposed. No additional\n"
            "arguments are required."
            "\n\n"
            "   ---"
            "\n\n"
            "By default, this program does the following:\n"
            "    - places output in the current working directory\n"
            "    - does not modify filenames\n"
            "    - skips file conflicts"
            "\n\n"
            "The above defaults can be changed, however, by using optional\n"
            "arguments listed below."
        ),
    )
    return primary_parser.parse_args(argv)


def parse_pre_args(argv: Optional[List[str]] = None) -> argparse.Namespace:
    """Parse preliminary arguments to determine log output preferences.

    Some arguments need to be known quickly so that logging can be
    configured straight away. A full parsing of the arguments can be
    done later.

    Parameters
    ----------
    argv : list of str or None
        Arguments manually provided to the parser (only for testing).

    Returns
    -------
    :obj:`argparse.Namespace`
        The known arguments parsed into a namedtuple-like object.

    """
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument(
        "-v",
        "--verbose",
        action="count",
        default=0,
    )
    return parser.parse_known_args(argv)[0]
