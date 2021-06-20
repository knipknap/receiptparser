import sys
import os
from setuptools import setup, find_packages
sys.path.insert(0, 'receiptparser')
from version import __version__

# Import the project description from the README.
with open("README.md") as fp:
    descr = fp.read()

# Run the setup.
setup(name             = 'receiptparser',
      version          = __version__,
      description      = 'Receipt and bill parser using OCR',
      long_description = descr,
      long_description_content_type='text/markdown',
      install_requires = ["wand>=0.6.2",
                          "pytesseract>=0.3.5",
                          "munch>=2.5.0",
                          "python-dateutil",
                          "pyaml"],
      author           = 'Samuel Abels',
      author_email     = 'knipknap@gmail.com',
      license          = 'MIT',
      package_dir      = {'receiptparser': 'receiptparser'},
      package_data     = {'receiptparser': ['data/configs/*.yml']},
      packages         = find_packages(),
      scripts          = ['scripts/receiptparser'],
      extras_require   = {},
      keywords         = ' '.join(['receipt',
                                   'bill',
                                   'parser',
                                   'ocr',
                                   'fuzzy',
                                   'scan',
                                   'library']),
      url              = 'https://github.com/knipknap/receiptparser/',
      classifiers      = [
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Intended Audience :: End Users/Desktop',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Environment :: Console',
        'Topic :: Scientific/Engineering :: Image Recognition',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Text Processing',
      ])
