import sys
import os
from setuptools import setup, find_packages
sys.path.insert(0, 'receiptparser')
from version import __version__

# Import the project description from the README.
descr = '''
Use OCR to parse an image of a receipt or bill, and use fuzzy matching to
extract information like the dollar (or Euro) amount, the company name,
the date and the postal code.
'''.strip()

# Run the setup.
setup(name             = 'receiptparser',
      version          = __version__,
      description      = 'Receipt and bill parser using OCR',
      long_description = descr,
      author           = 'Samuel Abels',
      author_email     = 'knipknap@gmail.com',
      license          = 'MIT',
      package_dir      = {'receiptparser': 'receiptparser'},
      package_data     = {},
      packages         = find_packages(),
      scripts          = ['scripts/rp'],
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
