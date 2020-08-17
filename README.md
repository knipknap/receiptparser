# receiptparser

[![Build Status](https://travis-ci.org/knipknap/receiptparser.svg?branch=master)](https://travis-ci.org/knipknap/receiptparser)
[![Coverage Status](https://coveralls.io/repos/github/knipknap/receiptparser/badge.svg?branch=master)](https://coveralls.io/github/knipknap/receiptparser?branch=master)
[![Code Climate](https://lima.codeclimate.com/github/knipknap/receiptparser/badges/gpa.svg)](https://lima.codeclimate.com/github/knipknap/receiptparser)
[![Documentation Status](https://readthedocs.org/projects/receiptparser/badge/?version=latest)](http://receiptparser.readthedocs.io/en/latest/?badge=latest)

## Summary

A receipt and bill parser written in Python.
Can be used as a Python module or CLI tool.

It was originally based on [receipt-parser](https://github.com/mre/receipt-parser),
but has effectively been completely rewritten/replaced.

So far, only German receipts are supported, but other countries can
be added using a simple [YAML configuration file](data/configs/germany.yml).

## Installation

```bash
pip3 install receiptparser
```

## CLI Usage

A simple example to read all images (.jpg) from a directory and print the recognized data
to stdout:

```bash
receiptparser tests/data/germany/img/
```

You can customize the output as follows:

```bash
receiptparser -v0 --format "{date:%Y-%m-%d} - {market} - {postal} - {sum}.jpg" tests/data/germany/img/
```

In this case, `-v0` suppresses any output, except for what you specify in the `--format FORMAT`
parameter. FORMAT is a Python format string as specified [here](https://docs.python.org/3.4/library/string.html#format-string-syntax).
The following values can be used in the format string:

- market: The recognized name of the business
- postal: The recognized postal code of the business
- date: The recognized date of the bill or receipt
- sum: The dollar (or Euro, or other currency) amount of the bill or receipt

### Syntax

```bash
usage: receiptparser [-h] [-c CONFIG] [--config-file CONFIG_FILE] [-s] [-t TESSERACT] [-f FORMAT] [-v {0,1,2}] input

positional arguments:
  input                 file or directory from which images will be read

optional arguments:
  -h, --help            show this help message and exit
  -c CONFIG, --config CONFIG
                        built-in config to use
  --config-file CONFIG_FILE
                        like -c, but point to a file instead
  -s, --sharpen         whether to sharpen the image before OCR
  -t TESSERACT, --tesseract TESSERACT
                        output directory for OCR recognized text (default is to discard)
  -f FORMAT, --format FORMAT
                        format of the recognized output. default is pretty-printing
  -v {0,1,2}, --verbosity {0,1,2}
                        increase output verbosity
```

## Python usage

```python
from receiptparser.config import read_config
from receiptparser.parser import process_receipt

config = read_config('my_config.yml')
receipt = process_receipt(config, "my_receipt.jpg", sharpen=False, out_dir=None, verbosity=0)

print("Filename:   ", receipt.filename)
print("Market:     ", receipt.market)
print("Postal code:", receipt.postal)
print("Date:       ", receipt.date)
print("Amount:     ", receipt.sum)
```
