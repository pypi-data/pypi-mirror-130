"""Contains class for execution of prediction model."""
import csv
import time

from pathlib import Path

from alive_progress import alive_it    # pylint: disable=E0401

from tily import tiff
from tily import models

PREDICTION_IN_TENSOR_INDEX = 1


class WsiTil:
    """Prediction model for Tumor Infiltrating Lymphocytes slides.

    Attributes:
        input_tiff: str, absolute location of the TIFF file.
        model_type: str, the name of the prediction model.
        model_path: str, absolute location of the models files.
        output_path: str, absoulte location for the output files.
        mpp: float, the pixel mapping of the scanned image.
        page_index: int, index of TIFF page to use as reference.
        patch_size: int, size of patch to crop from original slide.
        patch_magnification: int, magnifacation of the cropped area.
    """

    def __init__(self, startup_options: dict) -> None:
        """Initializes class with required parameters."""

        self.tiff_file = startup_options["input_tiff"]
        self.width, self.height, self.crop_size = tiff.get_tiff_parameters(
            self.tiff_file, startup_options["mpp"],
            startup_options["page_index"],
            startup_options["patch_magnification"],
            startup_options["patch_size"])
        self.prediction_csv = self.csv_file_name(startup_options["output_path"])
        self.run_predictor(startup_options["model_type"],
                           startup_options["model_path"],
                           startup_options["page_index"])

    def csv_file_name(self, output_path: str) -> str:
        """Generates CSV file name."""
        tiff_name = str(Path(Path(self.tiff_file).name).stem)
        prediction_csv = str(
            Path(output_path).joinpath(tiff_name)
        ) + '_w_' + str(self.width // self.crop_size) + '_h_' + str(
            self.height // self.crop_size) + '_csz_' + str(
                self.crop_size) + time.strftime("_%Y%m%d_%H%M%S") + '.csv'
        return prediction_csv

    def csv_writer(self, data_row: tuple) -> None:
        """Writes rows to csv file.

        Args:
            data_row: tuple, containing data to append to csv.
        """
        headers = ('x', 'y', 'prediction', 'whiteness', 'blackness', 'redness')
        with open(self.prediction_csv, 'a',
                  encoding="utf-8") as prediction_file:
            writer = csv.writer(prediction_file)
            if not Path(self.prediction_csv).exists():
                writer.writerow(headers)
            writer.writerow(data_row)

    def run_predictor(self, model_type: str, model_path: str,
                      page_index: int) -> None:
        """Runs model prediction inference over TIFF crops."""

        page = tiff.get_tiff_page(self.tiff_file, page_index)
        model = models.Models(model_type, model_path)
        model_input_image_size = model.get_size()

        for x_index_crop_on_slide in alive_it(
                range(self.height // self.crop_size),
                title=f"Running {model_type} based prediction",
                theme="scuba"):
            for y_index_crop_on_slide in range(self.width // self.crop_size):
                x_top_left = x_index_crop_on_slide * self.crop_size
                y_top_left = y_index_crop_on_slide * self.crop_size
                crop_array = tiff.get_crop_array(page, x_top_left, y_top_left,
                                                 self.crop_size)
                resized_array = tiff.resize_image_array(crop_array,
                                                        model_input_image_size)

                prediction = model.predict(
                    tiff.normalize_image_array(resized_array))
                prediction_sigmoid = tiff.get_sigmoid(
                    prediction[:, PREDICTION_IN_TENSOR_INDEX])
                self.csv_writer(
                    (x_index_crop_on_slide, y_index_crop_on_slide,
                     prediction_sigmoid, tiff.get_whiteness(resized_array),
                     tiff.get_blackness(resized_array),
                     tiff.get_redness(resized_array)))
