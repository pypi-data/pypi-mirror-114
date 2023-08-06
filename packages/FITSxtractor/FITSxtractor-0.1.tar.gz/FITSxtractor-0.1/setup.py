from distutils.core import setup

with open("README.md", "r", encoding="utf-8") as fh:
  long_description = fh.read()
setup(
  name = 'FITSxtractor',
  packages = ['FITSxtractor'],
  version = '0.1',
  license='MIT',
  description = 'This package extracts xml metadata from FITS output to a csv or xlsx file',
  long_description=long_description,
  long_description_content_type="text/markdown",
  author = 'ovanov',
  author_email = 'ovanov@protonmail.com',
  url = 'https://github.com/ovanov/FITSxtractor',
  keywords = ['FITS', 'xml', 'csv', 'CLI programm'],
  install_requires=[
          'pandas>=1.3.1',
          'openpyxl>=3.0.7',
          'tqdm==4.61.2'
      ],
  classifiers=[
    'Development Status :: 3 - Alpha',
    'Intended Audience :: Developers',
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
    'Programming Language :: Python :: 3.9',
  ],
)