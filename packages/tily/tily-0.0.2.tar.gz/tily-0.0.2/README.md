# wsi_til
[![pylint](https://github.com/kandabarau/wsi_til/actions/workflows/lint.yml/badge.svg)](https://github.com/kandabarau/wsi_til/actions/workflows/lint.yml)
[![build](https://github.com/kandabarau/wsi_til/actions/workflows/build.yml/badge.svg)](https://github.com/kandabarau/wsi_til/actions/workflows/build.yml)
[![release](https://github.com/kandabarau/wsi_til/actions/workflows/release.yml/badge.svg)](https://github.com/kandabarau/wsi_til/actions/workflows/release.yml)

Tumor-infiltrating lymphocytes prediction based on Whole Slide Imaging.

## Installation

Below is instructions for Debian based systems.
The tools uses Tensorflow v.1 and thats why requires Python 3.7
to be installed. If you have Python below 3.7.12 already installed
please simply run:

```
sudo make install
```
If you also need to install Python 3.7 please run the following:

```
sudo make all
```

## Validation

1. TCGA tumor diagnostic slides (H&E stained) available at
[Genomic Data Commons Data Portal](https://portal.gdc.cancer.gov). 
Please download a [test slide](https://api.gdc.cancer.gov/data/82afde87-ee4c-41e1-88fc-b28b015fcc80)
and save as `validation.svs`.

2. To start the validation run the following:

```bash
python3 main.py
```
