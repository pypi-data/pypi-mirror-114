"""Perform the main functionality of the application.

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
from typing import List, Optional
import sys

from PIL import Image

import pyimgutil
from pyimgutil import arguments, commands


logger = logging.getLogger(__name__)


def check_args(args: argparse.Namespace) -> None:
    """Check all check-able arguments.

    Parameters
    ----------
    args : :obj:`argparse.Namespace`
        The namedtuple-like object containing parsed arguments.

    Returns
    -------
    None

    Notes
    -----
    This is a wrap-up of the checking functions in the arguments module.

    This function does not raise any errors itself, but the functions
    it calls may raise ValueError.

    """
    arguments.check_conflicts(args)
    if args.format is not None:
        arguments.check_format(args.format)
    if args.output is not None:
        arguments.check_output(args.output)
    if args.quality is not None:
        arguments.check_quality(args.quality)
    if args.command == "crop":
        arguments.check_crop(args.left, args.right, args.upper, args.bottom)
    if args.command == "resize":
        arguments.check_resize(args.width, args.height, args.scale)


def mod_path(path: Path, out_path: Path, args: argparse.Namespace) -> Path:
    """Modify parts of a filepath.

    Parameters
    ----------
    path : :obj:`pathlib.Path`
        The filepath to modify.
    output : :obj:`pathlib.Path`
        The desired parent.
    args : :obj:`argparse.Namespace`
        The namedtuple-like object containing parsed arguments.

    Returns
    -------
    :obj:`pathlib.Path`
        The modified filepath.

    Notes
    -----
    This is a wrap-up of the filepath modifying functions in the
    commands module.

    """
    new_path = commands.mod_parent(path, out_path)
    if args.prepend is not None:
        new_path = commands.mod_name(new_path, args.prepend, True)
    if args.append is not None:
        new_path = commands.mod_name(new_path, args.append, False)
    if args.format is not None:
        new_path = commands.mod_ext(new_path, args.format)
    return new_path


def perform_command(im: Image, args: argparse.Namespace) -> Image:
    """Perform a command on an image.

    Parameters
    ----------
    im : :obj:`PIL.Image`
        The image to modify.
    args : :obj:`argparse.Namespace`
        The namedtuple-like object containing parsed arguments.

    Returns
    -------
    :obj:`PIL.Image`
        The modified image.

    Notes
    -----
    This is a wrap-up of the image modifying functions in the commands
    module.

    """
    if args.command == "convert":
        mod_im = im
        logger.info("File converted.")
    if args.command == "crop":
        mod_im = commands.crop_image(
            im,
            args.left,
            args.right,
            args.upper,
            args.bottom,
        )
        logger.info("File cropped.")
    if args.command == "resize":
        mod_im = commands.resize_image(
            im,
            args.width,
            args.height,
            args.scale,
            args.ratio,
        )
        logger.info("File resized.")
    if args.command == "rotate":
        mod_im = commands.rotate_image(im, args.angle, args.fill)
        logger.info("File rotated.")
    if args.command == "transpose":
        mod_im = commands.transpose_image(im)
        logger.info("File transposed.")
    return mod_im


def main(argv: Optional[List[str]] = None) -> None:
    """Perform the main functionality of the application.

    Parameters
    ----------
    argv : list of str or None
        Arguments manually provided to the parser (only for testing).

    Returns
    -------
    None

    """
    pre_args = arguments.parse_pre_args(argv)
    arguments.configure_logging(pre_args.verbose)
    logger.debug(f"Log level: {pyimgutil.logger.level}")

    logger.info("Starting pyimgutil.")
    args = arguments.parse_args(argv)
    logger.debug(f"Arguments: {args}")
    logger.info("Checking the provided arguments.")
    try:
        check_args(args)
    except ValueError as e:
        logger.error(e)
        print(e)
        if args.command is None:
            print("For help, try `pyimgutil -h`.")
        else:
            print(f"For help, try `pyimgutil {args.command} -h`.")
        sys.exit()
    logger.info("Proceeding with the provided arguments.")

    logger.info("Retrieving input files.")
    input_files = []
    for path in args.input:
        logger.debug(f"Retrieving input: {path}")
        try:
            files_found = commands.get_valid_files(path, args.recursive)
        except ValueError as e:
            logger.error(e)
            print(e)
        else:
            logger.debug(f"Found files: {files_found}")
            input_files.append(files_found)
    files = set([file for sublist in input_files for file in sublist])
    logger.debug(f"Retrieved files: {files}")
    logger.info(f"Retrieved {len(files)} input files.")

    logger.info("Preparing the output location.")
    out_path = commands.get_output_dir(args.output)
    logger.info(f"Files will be saved to: {out_path}")

    logger.info("Processing files.")
    for file in files:
        with Image.open(file) as im:
            logger.info(f"Processing: {file}")
            try:
                mod_im = perform_command(im, args)
            except ValueError as e:
                logger.error(e)
                print(e)
                print(f"For help, try `pyimgutil {args.command} -h`.")
                sys.exit()

            logger.info("Preparing filename.")
            new_path = mod_path(file, out_path, args)
            logger.info(f"File will be saved to: {new_path}")

            logger.info("Saving file.")
            try:
                commands.save_image(mod_im, new_path, args.quality, args.force)
            except FileExistsError as e:
                logger.error(e)
                print(e)
            else:
                logger.info("File was saved.")
    logger.info("Finished processing files. Exiting pyimgutil.")


if __name__ == "__main__":
    main()
