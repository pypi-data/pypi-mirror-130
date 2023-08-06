# flconverters
A Python module containing multiple file converters.

## Authors
[CSynodinos](https://github.com/CSynodinos)

## Installation

Via pip:

```bash
  pip install flconverters
```

This is my first attempt at creating a library. This library allows for the conversion of files into other formats (both as a single file and as a batch).
It relies on pillow, opencv, XLSXWriter and docx for most conversions. The rest are done by default python libraries. Currently, installation is available through pip, but in the future conda installation will be possible.

## Example
```bash
    >>> from flconverters import txtconvert
    >>> convert = txtconvert(__file__ = path/to/file/or/directory, __d__ = path/to/output/directory)
    >>> convert.txt_docx()
```

## Features

- [x] Convert Text Documents to .docx
    - [ ] Convert to .ods

- [x] Convert Image files to other formats:
    - [x] images to pdf.
    - [x] image to base64 text file (UTF-8 encryption).
    - [x] images to binary.
    - [x] multiple compressed/raw image formats to .jpeg and .png.

- [x] Convert spreadsheet files (.xlsx, .csv, .tsv) into .xlsx, .csv or .tsv.
	- [ ] Convert to .ods
    - [ ] Convert to .html
