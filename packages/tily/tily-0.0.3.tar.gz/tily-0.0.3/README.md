# wsi_til
[![pylint](https://github.com/kandabarau/wsi_til/actions/workflows/lint.yml/badge.svg)](https://github.com/kandabarau/wsi_til/actions/workflows/lint.yml)
[![release](https://github.com/kandabarau/wsi_til/actions/workflows/release.yml/badge.svg)](https://github.com/kandabarau/wsi_til/actions/workflows/release.yml)
[![build](https://github.com/kandabarau/wsi_til/actions/workflows/build.yml/badge.svg)](https://github.com/kandabarau/wsi_til/actions/workflows/build.yml)

Tumor-infiltrating lymphocytes prediction based on Whole Slide Imaging.

## Installation

The tools uses Tensorflow v.1 and thats why requires Python 3.7
to be installed. If you have Python below 3.7.12 already installed
please simply run:

```
pip install tily
```

If you also need to install Python 3.7 please run the following:

```
sudo make install
python3.7 -m pip install tily
```

## Usage

To start the validation run the following:

```bash
tily --input_tiff=<PATH TO TIF\SVS file>
```
