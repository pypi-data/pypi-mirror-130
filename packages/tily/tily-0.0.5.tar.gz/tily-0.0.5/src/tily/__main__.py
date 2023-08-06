"""Command line interface for wsi-til library."""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os
import sys
import signal
from pathlib import Path

from absl import app
from absl import flags
from absl import logging

from tily import handlers
from tily import prediction

FLAGS = flags.FLAGS
MODEL_URL = "https://bit.ly/wsi-til-zip"
WORKDIR = Path.cwd()

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
logging.set_verbosity(logging.ERROR)

flags.DEFINE_string("input_tiff", None, "Path to TIFF or SVS file.")
flags.DEFINE_string("model_type", "vgg-mix", "Prediction model to use.")
flags.DEFINE_string("model_path", "/tmp/wsi_til/models",
                    "Location of pre-trained models files.")
flags.DEFINE_string("model_url", MODEL_URL,
                    "Remote location of models archive.")
flags.DEFINE_string("output_path", str(WORKDIR),
                    "Location where to store csv with results.")
flags.DEFINE_float("mpp", 0.3444,
                   "Default MPP value to use if none found in TIFF metadata.")
flags.DEFINE_integer("page_index", 0, "Index of TIFF page to use as reference.")
flags.DEFINE_integer("patch_size", 100, "Size of slide patch to use as input.")
flags.DEFINE_integer("patch_magnification", 20,
                     "Magnification of patch to match with slide.")


def _handle_term(*args) -> None:
    """Termination handler."""
    raise KeyboardInterrupt()


def _must_get_input_tiffs() -> list:
    """Validates input TIFF files.

    Return:
        list, input tiffs files.
        exit(1), if file doesn't exists.
    """
    input_tiffs = []

    if FLAGS.input_tiff:
        absoulte_tiff_path = handlers.absolute_file_path(FLAGS.input_tiff)
        if not Path(absoulte_tiff_path).exists():
            print("Provided TIFF '%s' wasn't found.", FLAGS.input_tiff)
            sys.exit(1)
        input_tiffs.append(absoulte_tiff_path)

    if FLAGS.input_tiff is None:
        logging.warning("'input_tiff' flag wasn't set - "
                        "will look for TIFF and SVS files in current workdir.")
        logging.warning("Current workdir is '%s'", WORKDIR)

        def _folder_parser(extension: str) -> list:
            """Looks for files with extension in WORKDIR.

            Args:
                extension: str, name of the files extension.

            Returns:
                list, files with matching extension.
            """
            return list(WORKDIR.glob(f"*.{extension}"))

        local_tiffs = _folder_parser("tif") + _folder_parser("svs")
        for found_file in local_tiffs:
            input_tiffs.append(str(found_file))
    return input_tiffs


def _must_get_models():
    """Validates that models graph exists."""
    model_path = Path(handlers.absolute_file_path(FLAGS.model_path))
    model_type_path = model_path.joinpath(FLAGS.model_type)
    model_graph = model_type_path.joinpath(FLAGS.model_type + ".ckpt.meta")
    if not model_graph.exists():
        output_path = handlers.absolute_file_path(FLAGS.model_path)
        if not Path(output_path).exists():
            Path(output_path).mkdir(parents=True)
        logging.warning("Saving models graphs to '%s'", output_path)
        if not handlers.get_models(FLAGS.model_url, output_path):
            logging.error("Failed to download model files.")
            sys.exit(1)


def _render_startup_options(tiff_file: str) -> dict:
    """Renders startup flags into attributes.

    Args:
        tiff_file: str, absoulte file path to TIFF file.

    Returns:
        startup_options: dict, rendered startup attributes.
    """
    startup_options = {
        "input_tiff": tiff_file,
        "model_type": FLAGS.model_type,
        "model_path": handlers.absolute_file_path(FLAGS.model_path),
        "output_path": handlers.absolute_file_path(FLAGS.output_path),
        "mpp": FLAGS.mpp,
        "page_index": FLAGS.page_index,
        "patch_size": FLAGS.patch_size,
        "patch_magnification": FLAGS.patch_magnification,
    }
    return startup_options


def init(argv):
    """Initializes CLI interface."""
    del argv

    signal.signal(signal.SIGTERM, _handle_term)
    logging.info("Retrieving TIFF files.")
    input_tiffs = _must_get_input_tiffs()
    if len(input_tiffs) == 0:
        print("No TIFF files found - nothing to do.")
        sys.exit(1)

    logging.info("Validating model files.")
    _must_get_models()

    logging.info("Rendering startup options.")
    startup_options = [_render_startup_options(tiff) for tiff in input_tiffs]

    logging.info("Starting prediction runner.")
    for task in startup_options:
        try:
            prediction.WsiTil(task)
        except AttributeError as err:
            logging.error("Failed to process '%s' - '%s'", task["input_tiff"],
                          err)
        except KeyboardInterrupt:
            print("\nProcess terminated. Bye!\n")

def main():
    """PIP package entrypoint."""
    app.run(init)


if __name__ == "__main__":
    app.run(init)
