"Handlers are some helper functions that are required for prediction module."
import shutil
import tempfile
import zipfile

from pathlib import Path
from typing import Optional

import requests

from absl import logging
from alive_progress import alive_it    # pylint: disable=E0401

CHUNK_SIZE = 1024
SUPPORTED_MODELS = ["vgg-mix", "incep-mix"]


def get_models(url: str, models_path: str) -> bool:
    """Prepares models files to be used for prediction.

    Args:
        url: str, remote location of models archive.
        models_path: str, path to directory with TF models.

    Returns:
        result: bool, True if sucessfull, False if not.
    """
    result = True
    temp_dir = tempfile.mkdtemp()
    logging.info("Temporary folder '%s' created", temp_dir)

    logging.info("Downloading archive from %s", url)
    model_zip_file = download_file(url, "models.zip", temp_dir)
    if model_zip_file is None:
        result = False

    zip_dir = _unpack_model(model_zip_file)
    if zip_dir is None:
        result = False
    logging.info("'%s' was extracted to '%s'", model_zip_file, zip_dir)

    model_path = _sort_model(zip_dir, models_path)
    logging.info("The model was sorted.")

    _add_checkpoints(model_path)
    logging.info("Checkpoints added.")

    logging.info("Removing temporary folder '%s'", temp_dir)
    shutil.rmtree(temp_dir)
    return result


def download_file(url: str, file_name: str, output_path: str) -> Optional[str]:
    """Downloads file from remote url.

    Args:
        url: str, link to remote location.
        file_name: str, expected file name with extension.
        output_path: str, location to save.

    Returns:
        file_path: Optional[str], local path to downloaded file.
    """
    file_path = Path(output_path).joinpath(file_name)
    if Path(absolute_file_path(file_path)).exists():
        return str(file_path)
    try:
        req = requests.get(url, allow_redirects=True, stream=True)
        file_type = f"application/{Path(file_name).suffix[1:]}"
        content_type = req.headers["Content-Type"]
        if content_type != file_type:
            logging.warning("Expecteda remote to be '%s' - got '%s'.",
                            file_type, content_type)
    except requests.exceptions.MissingSchema as err:
        logging.error("Please check the url - %s", err)
        return None

    if not Path(absolute_file_path(str(output_path))).is_dir():
        logging.info("Creating output folder '%s'.", output_path)
        Path(absolute_file_path(output_path)).mkdir(parents=True, exist_ok=True)
    with open(file_path, "wb") as file:
        for chunk in alive_it(req.iter_content(chunk_size=CHUNK_SIZE),
                              title=f"Downloading {file_name}",
                              theme="scuba"):
            file.write(chunk)
    return str(file_path)


def absolute_file_path(file_path: str) -> str:
    """Takes relative file path and returns absolute.

    Args:
        file_path: any form of path.

    Returns:
        str, resolved absolute file path.
    """
    return str(Path(file_path).resolve())


def _unpack_model(archive_path: str) -> Optional[str]:
    """Unpacks models archive.

    Args:
        archive_path: str, location of the zip archive.

    Returns:
        zip_dir: str, temporary local extraction path.
    """
    try:
        zip_dir = Path(archive_path).parent
        logging.info("Model archive will be extracted to '%s'", zip_dir)
        with zipfile.ZipFile(archive_path, "r") as zip_ref:
            zip_ref.extractall(zip_dir)
        return str(zip_dir)
    except zipfile.BadZipFile as err:
        logging.error("'%s' is not zip archive - %s", archive_path, err)
        return None
    except FileNotFoundError as err:
        logging.error("'%s' doesn't exists - %s", archive_path, err)
        return None


def _sort_model(input_model_path: str, output_path: str) -> str:
    """Sorts necessary files and saves them to final location.

    Args:
        input_model_path: str, unsorted model path location.
        output_path: str, destination location.

    Returns:
        output_model_path: str, absolute path to saved models.
    """
    source = Path(input_model_path).glob("*ckpt*")
    model_files = [f for f in source if f.is_file()]

    model_types = set()
    for file in model_files:
        model_types.add(Path(file.stem).stem)

    output_model_path = Path(output_path)
    for model in model_types:
        model_path = output_model_path.joinpath(model)
        logging.info("Creating folder for model '%s' as '%s'", model,
                     model_path)
        model_path.mkdir(parents=True, exist_ok=True)
        for file in model_files:
            if model in file.name:
                model_file = Path(model_path).joinpath(file.name)
                logging.info("Saving '%s' as '%s'", file.name, model_file)
                shutil.move(str(Path(file)), model_file)
    return str(output_model_path)


def _add_checkpoints(model_path: str) -> None:
    """Creates checkpoint files for each model.

    Args:
        model_path: str, location of sorted model files.
    """
    models = [d for d in Path(model_path).iterdir() if d.is_dir()]
    for model in models:
        if str(model.stem) in SUPPORTED_MODELS:
            checkpoint = model.joinpath('checkpoint')
            logging.info("Saving checkpoint for %s as %s", model, checkpoint)
            with open(checkpoint, "w", encoding="utf8") as file:
                file.write(f"model_checkpoint_path: \"{model.stem}.ckpt\"\n")
                file.write(
                    f"all_model_checkpoint_paths: \"{model.stem}.ckpt\"\n")
