"""TIFF files processing functions."""
import xml.etree.ElementTree as ET

from typing import Any, Optional, Tuple

import tifffile
import numpy as np

from absl import logging
from PIL import Image

PAGE_DECODE_TILE_INDEX = 0
SAMPLE_DIMENSION_INDEX = 0
RED_CHANNEL_INDEX = 0
GREEN_CHANNEL_INDEX = 1
BLUE_CHANNEL_INDEX = 2


def get_tiff_properties(page: Any) -> dict:
    """Converts TIFF page properties to dictionary.

    Args:
        page: , single page of the input file.

    Returns:
        properties: dict, tag.name:tag.value parameters for the page.
    """
    properties = {tag.name: tag.value for tag in page.tags}
    return properties


def get_mpp_value(tiff_properties: dict, default_mpp: float) -> float:
    """Parses metadata properties for MPP value.

    Args:
        tiff_properties: dict, TIFF page parameters.
        default_mpp: float, default MPP value if not provided in metadata.

    Returns:
        float, TIFF page MPP value.
    """
    xml = tiff_properties.get('OlympusSIS')
    tiff_values = tiff_properties.get('ImageDescription')
    if tiff_values:
        if xml:
            tiff_values_xml = ET.fromstring(tiff_values)
            for pixels in tiff_values_xml.findall(
                    ".//{http://www.openmicroscopy.org/Schemas/OME/2015-01}Pixels"
            ):
                physical_size_x_value = pixels.attrib['PhysicalSizeX']
                return round(float(physical_size_x_value), 4)
        tiff_values_string = tiff_values.split('|')
        for value in tiff_values_string:
            if 'mpp' in value.lower():
                mpp_value = value.split("=")
                return round(float(mpp_value[-1].strip(" ")), 4)
    logging.warning(
        "No MPP value was found in metadata. "
        "Falling back to default: %s", default_mpp)
    return default_mpp


def get_width_value(tiff_properties: dict) -> int:
    """Extracts width(X) value from TIFF metadata.

    Args:
        tiff_properties: dict, TIFF page parameters.

    Returns:
        uint, TIFF page MPP value.
    """
    return int(tiff_properties.get('ImageWidth'))


def get_height_value(tiff_properties: dict) -> int:
    """Extracts height(Y) value from TIFF metadata.

    Args:
        tiff_properties: dict, TIFF page parameters.

    Returns:
        uint, TIFF page MPP value.
    """
    return int(tiff_properties.get('ImageLength'))


def get_crop_size(mpp_value: float, patch_magnification: int,
                  patch_size: int) -> int:
    """Calculates slide crop size based on MPP, patch size and magnification.

    Args:
        mpp_value: float, TIFF MPP value.
        patch_magnification: int, patch magnification value.
        patch_size: int, patch size value.

    Returns:
        uint, crop size value.
    """
    crop_size = (patch_size * (10.0 / mpp_value)) / patch_magnification
    return int(crop_size)


def get_tiff_parameters(file_path: str, default_mpp: float, page_index: int,
                        patch_magnification: int,
                        patch_size: int) -> Tuple[int, int, int]:
    """Calculates TIFF file parameters.

    Args:
        file_path: str, absolute path to TIFF file.
        default_mpp: float, fallback MPP value.
        page_index: int, index of TIFF page.
        patch_magnification: int, slide magnification.
        patch_size: int, slide patch size.

    Returns:
        width: int, image width.
        height: int, image height.
        crop: int, crop size.
    """
    with tifffile.TiffFile(file_path) as tif:
        properties = get_tiff_properties(tif.pages[page_index])
        mpp = get_mpp_value(properties, default_mpp)
        width = get_width_value(properties)
        height = get_height_value(properties)
        crop_size = get_crop_size(mpp, patch_magnification, patch_size)
        return int(width), int(height), int(crop_size)


def get_tiff_page(file_path: str, page_index: int):
    """Returns specified page

    Args:
        file_path: str, absolute path to TIFF file.
        page_index: int, index of TIFF page.

    Returns:
        page: Any, the TIFF page.
    """
    # with tifffile.TiffFile(file_path) as tif:
    #     page = tif.pages[page_index]
    #     return page
    return tifffile.TiffFile(file_path).pages[page_index]


def validate_crop_area(page: Any, x_top_left: int, y_top_left: int,
                       crop_size: int) -> Optional[list]:
    """Validates a crop area upon the TIFF page.

    Args:
        page: TiffPage, TIFF page from which the crop must be extracted.
        x_top_left: int, x coordinate of the top left corner of the desired crop.
        y_top_left: int, y coordinate of the top left corner of the desired crop.
        crop_size: int, desired crop size.

    Returns:
        err: str, error message if any.
    """
    errors = []
    if not page.is_tiled:
        err = "Input page must be tiled."
        logging.error(err)
        errors.append(err)

    if crop_size < 1:
        err = "Crop size is %s - must be strictly positive."
        logging.error(err, crop_size)
        errors.append(err)

    if x_top_left < 0:
        err = "Coordinates %s of X top left is out of image bounds."
        logging.error(err, x_top_left)
        errors.append(err)

    if y_top_left < 0:
        err = "Coordinates %s of Y top left is out of image bounds."
        logging.error(err, y_top_left)
        errors.append(err)

    if x_top_left + crop_size >= page.imagelength:
        err = "Coordinates %s of X bottom right is bigger than image X limit %s."
        logging.error(err, x_top_left + crop_size, page.imagelength)
        errors.append(err)

    if y_top_left + crop_size >= page.imagewidth:
        err = "Coordinates %s of Y bottom right is bigger than image Y limit %s."
        logging.error(err, y_top_left + crop_size, page.imagewidth)
        errors.append(err)

    if len(errors) > 0:
        return errors
    return None


def get_crop_array(    # pylint: disable=too-many-locals
        page: Any, x_top_left: int, y_top_left: int, crop_size: int) -> Any:
    """Extracts a crop from the TIFF page.

    Args:
        page: TiffPage, TIFF page from which the crop must be extracted.
        x_top_left: int, x coordinate of the top left corner of the desired crop.
        y_top_left: int, y coordinate of the top left corner of the desired crop.
        crop_size: int, desired crop size.

    Returns:
        np.ndarray, cropped slide area.
    """

    if validate_crop_area(page, x_top_left, y_top_left, crop_size):
        logging.error("Crop area is not valid.")
        return None

    # Calculate 2d limits (top left, bottom right) of tiles containing crop.
    tile_x_top_left = x_top_left // page.tilewidth
    tile_y_top_left = y_top_left // page.tilewidth
    tile_x_bottom_right, tile_y_bottom_right = np.ceil([
        (x_top_left + crop_size) / page.tilewidth,
        (y_top_left + crop_size) / page.tilewidth
    ]).astype(int)

    # Calculate the key for 1d/2d tile index conversion.
    tile_per_width = int(np.ceil(page.imagewidth / page.tilewidth))

    # Create an empty array to hold tiles containing crop.
    tiles_with_crop_arr = np.empty(
        ((tile_x_bottom_right - tile_x_top_left) * page.tilewidth,
         (tile_y_bottom_right - tile_y_top_left) * page.tilewidth,
         page.samplesperpixel),
        dtype=page.dtype)

    jpeg_tables = page.tags.get('JPEGTables', None)
    if jpeg_tables is not None:
        jpeg_tables = jpeg_tables.value

    for tile_x_2d in range(tile_x_top_left, tile_x_bottom_right):
        for tile_y_2d in range(tile_y_top_left, tile_y_bottom_right):
            # Convert tile 2d index back to 1d.
            tile_index_1d = int(tile_x_2d * tile_per_width + tile_y_2d)
            # Get tile array.
            page.parent.filehandle.seek(page.dataoffsets[tile_index_1d])
            data = page.parent.filehandle.read(
                page.databytecounts[tile_index_1d])
            # Get top left corner of tile array on tiles_with_crop_arr.
            im_x = (tile_x_2d - tile_x_top_left) * page.tilewidth
            im_y = (tile_y_2d - tile_y_top_left) * page.tilewidth
            # write tile array without sample dimension into tiles_with_crop_arr.
            tiles_with_crop_arr[
                im_x:im_x + page.tilewidth,
                im_y:im_y + page.tilewidth, :] = page.decode(
                    data, tile_index_1d,
                    jpeg_tables)[PAGE_DECODE_TILE_INDEX].squeeze(
                        axis=SAMPLE_DIMENSION_INDEX)
    # Get top left corner of crop on tiles_with_crop_arr.
    im_x_top_left = x_top_left - tile_x_top_left * page.tilewidth
    im_y_top_left = y_top_left - tile_y_top_left * page.tilewidth

    return tiles_with_crop_arr[im_x_top_left:im_x_top_left + crop_size,
                               im_y_top_left:im_y_top_left + crop_size, :]


def resize_image_array(crop_array: np.ndarray,
                       target_size: tuple) -> np.ndarray:
    """Resizes the crop array.

    Args:
        crop_array: np.ndarray, crop 3d RGB array to resize.
        target_size: tuple, width and height of desired image array.

    Returns:
        np.ndarray, 3d RGB array of model-requ
        ired width and height.
    """
    image_resized = Image.fromarray(
        crop_array.astype('uint8')).resize(target_size)
    return np.asarray(image_resized)


def get_whiteness(crop_array: np.ndarray) -> float:
    """Measures the whiteness of the input image array.

    Args:
        crop_array: np.ndarray, crop 3d RGB array of uint8 of range 0..255.

    Returns:
        whiteness: float, mean standard deviation across 3 color channels.
    """
    whiteness = (np.std(crop_array[:, :, RED_CHANNEL_INDEX]) +
                 np.std(crop_array[:, :, GREEN_CHANNEL_INDEX]) +
                 np.std(crop_array[:, :, BLUE_CHANNEL_INDEX])) / 3.0
    return float(whiteness)


def get_blackness(crop_array: np.ndarray) -> float:
    """Measures the blackness of the input image array.

    Args:
        crop_array: np.ndarray, crop 3d RGB array of uint8 of range 0..255.

    Returns:
        blackness: float, mean intensity across 3 color channels.
    """
    blackness = np.mean(crop_array)
    return float(blackness)


def get_redness(crop_array: np.ndarray) -> float:
    """Measures the redness of the input image array.

    Args:
        crop_array: np.ndarray, crop 3d RGB array of uint8 of range 0..255.

    Returns:
        redness: float, mean of red-weighted intensity across 3 color channels.
    """
    redness = np.mean((crop_array[:, :, RED_CHANNEL_INDEX] >= 190) *
                      (crop_array[:, :, GREEN_CHANNEL_INDEX] < 100) *
                      (crop_array[:, :, BLUE_CHANNEL_INDEX] <= 100))
    return float(redness)


def normalize_image_array(crop_array: np.ndarray) -> np.ndarray:
    """Normalizes the array for model input.

    Args:
        crop_array: np.ndarray, image array of uint8 of range 0..255.

    Returns:
        normalized_array: np.ndarray, normalized 4d float array of range -1..1.
    """
    normalized_array = np.empty(crop_array.shape)
    np.clip(crop_array, 0, 255, normalized_array)
    normalized_array /= 255
    normalized_array -= 0.5
    normalized_array *= 2
    return np.expand_dims(normalized_array, axis=SAMPLE_DIMENSION_INDEX)


def get_sigmoid(prediction: float) -> float:
    """Computes sigmoid value of prediction.

    Args:
        prediction: float, model inference output.

    Returns:
        sig: float, sigmoid - original distributed values pushed to 0..1.
    """
    sigmoid = 1 / (1 + np.exp(-prediction))
    return float(sigmoid)
