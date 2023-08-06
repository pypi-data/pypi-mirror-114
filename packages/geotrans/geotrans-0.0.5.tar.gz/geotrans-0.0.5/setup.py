# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['geotrans']

package_data = \
{'': ['*']}

install_requires = \
['click', 'geopandas']

extras_require = \
{'coverage': ['coverage', 'coverage-badge'],
 'docs': ['sphinx',
          'sphinx-rtd-theme',
          'nbsphinx',
          'sphinx-gallery',
          'sphinx-autodoc-typehints'],
 'format-lint': ['sphinx',
                 'pylint',
                 'rstcheck',
                 'black',
                 'black-nb',
                 'blacken-docs',
                 'blackdoc',
                 'isort'],
 'typecheck': ['mypy']}

entry_points = \
{'console_scripts': ['geotrans = geotrans.cli:main']}

setup_kwargs = {
    'name': 'geotrans',
    'version': '0.0.5',
    'description': 'Switch between spatial fileformats.',
    'long_description': 'Geotransformations Python Command Line Utility\n==============================================\n\n|Documentation Status| |PyPI Status| |CI Test| |Coverage|\n\nDocumentation\n-------------\n\n-  Published on ReadTheDocs:\n   `Documentation <https://geotransform.readthedocs.io/en/latest/index.html>`__\n\nFeatures\n--------\n\n-  Command line utility for easy transformations between geodata/spatial\n   filetypes.\n-  Python functions with documentation for direct usage.\n\n   -  This is my own main use case: A package with all basic geopandas\n      file loads and saves bundled.\n\n-  Uses Python pathlib for cross-platform path handling.\n\nSupport\n-------\n\nCurrently supports:\n\n-  `GeoPackages <https://www.geopackage.org/>`__\n-  `Esri\n   Shapefiles <https://www.esri.com/library/whitepapers/pdfs/shapefile.pdf>`__\n-  `File\n   Geodatabases <https://desktop.arcgis.com/en/arcmap/10.3/manage-data/administer-file-gdbs/file-geodatabases.htm>`__\n   *Read only*\n-  `GeoJSON <https://geojson.org/>`__\n\nAll file formats supported by geopandas can be implemented.\n\nDependencies\n------------\n\n-  `geopandas <https://github.com/geopandas/geopandas>`__ for\n   transforming between geodata filetypes which in turn uses ``fiona`` (that\n   uses ``GDAL``).\n-  `click <https://github.com/pallets/click/>`__ for command line\n   integration.\n\nAlternatives\n------------\n\nThe ``GDAL`` tool `ogr2ogr <https://gdal.org/programs/ogr2ogr.html>`__ is a\nmuch more sophisticated command-line tool for converting between spatial\nfile formats.\n\nGeopandas by itself supports many more spatial file formats. For more\nadvanced use cases when interacting with Python I recommend just using\ngeopandas.\n\nFiona provides a command-line interface ``fio``.\n`fio <https://fiona.readthedocs.io/en/latest/manual.html>`__.\n\nInstallation\n------------\n\n-  PyPi\n\n.. code:: bash\n\n   pip install geotrans\n\n-  poetry for development\n\n.. code:: bash\n\n   git clone https://github.com/nialov/geotransform.git\n   cd geotransform\n   poetry install\n\nUsing geotransform\n------------------\n\nCommand line\n~~~~~~~~~~~~\n\nRun\n\n.. code:: bash\n\n   geotrans --help\n\nto print the command line help for the utility.\n\nTo transform from a geopackage file with a single layer to an ESRI\nshapefile:\n\n.. code:: bash\n\n   geotrans input_file.gpkg --to_type shp --output output_file.shp\n\nTo transform from a geopackage file with multiple layers to multiple\nESRI shapefiles into a given directory:\n\n.. code:: bash\n\n   geotrans input_file.gpkg --to_type shp --output output_dir\n\nPython\n~~~~~~\n\nAll main functions in charge of loading and saving geodata files are\nexposed in the transform.py file in the geotrans package.\n\n.. code:: python\n\n   from geotrans.transform import load_file, save_files, SHAPEFILE_DRIVER\n   from pathlib import Path\n\n   # Your geodata file\n   filepath = Path("input_file.gpkg")\n\n   # load_file returns a single or multiple geodataframes depending\n   # on how many layers are in the file.\n   geodataframes, layer_names = load_file(filepath)\n\n   # Assuming geopackage contained only one layer ->\n   # Save acquired geodataframe and layer\n   save_files(geodataframes, layer_names, [Path("output_file.shp")], SHAPEFILE_DRIVER)\n\nLicense\n-------\n\n-  This project is licensed under the terms of the `MIT\n   license. <LICENSE.md>`__\n\nCopyright © 2020, Nikolas Ovaskainen.\n\n.. |Documentation Status| image:: https://readthedocs.org/projects/geotransform/badge/?version=latest\n   :target: https://geotransform.readthedocs.io/en/latest/?badge=latest\n.. |PyPI Status| image:: https://img.shields.io/pypi/v/geotrans.svg\n   :target: https://pypi.python.org/pypi/geotrans\n.. |CI Test| image:: https://github.com/nialov/geotransform/workflows/test-and-publish/badge.svg\n   :target: https://github.com/nialov/geotransform/actions/workflows/test-and-publish.yaml?query=branch%3Amaster\n.. |Coverage| image:: https://raw.githubusercontent.com/nialov/geotransform/master/docs_src/imgs/coverage.svg\n   :target: https://github.com/nialov/geotransform/blob/master/docs_src/imgs/coverage.svg\n',
    'author': 'nialov',
    'author_email': 'nikolasovaskainen@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/nialov/geotrans',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.7.1,<4.0.0',
}


setup(**setup_kwargs)
