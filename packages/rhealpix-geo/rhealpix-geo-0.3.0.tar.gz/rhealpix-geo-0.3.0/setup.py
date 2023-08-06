# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['rheal']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'rhealpix-geo',
    'version': '0.3.0',
    'description': 'Objects for DGGS Cells and collections of Cells.',
    'long_description': '# DGGS Classes for Cells and Cell Collections for parametrisations of rHEALPix grids\n\nThis library contains classes for representing DGGS Cells and collections of these ("CellCollection") according to parametrisations of the [rHEALPix Discrete Global Grid System](https://iopscience.iop.org/article/10.1088/1755-1315/34/1/012012/pdf).\nThis provides a convenient low level API to work with Cells and CellCollections. An example of a library that utilises these objects for higher level geospatial operations is the [rhealpix-sf library](https://github.com/surroundaustralia/rhealpix-sf) which provides a set of Simple Feature relation operations for DGGS Cells.  \n  \nValidation is provided for Cell and CellCollections.\nCellCollections have the following operations performed on instantiation: \n- compression (where all children of a parent are present, replace with their parent)  \n- deduplication (removal of repeated cells)  \n- absorb (where a child and its parent are present, remove the child/children)  \n- ordering (alphabetical and numerical based on suids)  \n\nThese operations provide a consistent representation of collections of Cells, allowing higher level operations to work with a simplified, valid, and consistent set of cells. \n\nCells and CellCollections have the following attributes or methods:\n- add: Add two sets of Cell or CellCollections, returning a CellCollection  \n- subtract: Subtract a Cell or CellCollection from an other, returning a CellCollection  \n- equal: Test two Cells or CellCollections for equivalence  \n- len: the number of Cells in a Cell (1) or CellCollection (N)  \n- area: to be implemented\n- resolution / min and max resolution for CellCollections: the resolution or minimum / maximum resolution for Cells or CellCollections respectively.  \n- neighbours: the Cells immediately neighbouring a Cell or CellCollection, optionally including diagonals. For CellCollections, excludes neighbouring cells interior to the CellCollection. Resolution specifiable.  \n- border: the set of interior Cells along the edges of a Cell or CellCollection. Resolution specifiable.  \n- children: the set of child Cells for a Cell or CellCollection. Resolution specifiable. \n\n## Installation \nInstall from PyPi, for example using pip or poetry.  \n\nhttps://pypi.org/project/rhealpix-geo/  \n\nThis package has no dependencies.\n\n## Use\nThese functions are implemented in the file `rheal/dggs_classes.py`\n\nThis means they can be used like this (full working script):\n\n```python\nfrom rheal import Cell, CellCollection\n\na = Cell("R1")\nb = Cell("R11")\nc = CellCollection("R1 R2")\nprint(a + b)\n# b is within a, so a CellCollection equivalent to a is returned\nprint(a - b)\n# b is within a, so a subset of a is returned\nprint(a + c)\n# c contains a, so a CellCollection equivalent to c is returned \nprint(a == b)\n# a\'s border at a resolution two levels higher than a\'s resolution\nprint(a.border(a.resolution+2))\n# a\'s children at a resolution one level higher (default) than a\'s resolution\nprint(a.children())\n# a\'s neighbours at a\'s resolution (default) including diagonals (default). Note only 7 neighbours due to the shape of the north hemisphere cell.\nprint(a.neighbours())\n```\n\n## Testing\nAll tests are in `tests/` and implemented using [pytest](https://docs.pytest.org/en/6.2.x/).\n\nThere are individual tests for each of the Cell and CellCollection operations. \n\n## Contributing\nVia GitHub, Issues & Pull Requests: \n\n* <https://github.com/surroundaustralia/rhealpix-geo\n\n## License\nThis code is licensed with the BSD 3-clause license as per [LICENSE](LICENSE).\n\n## Citation\n```bibtex\n@software{https://github.com/surroundaustralia/rhealpix-geo,\n  author = {{David Habgood}},\n  title = {Objects for DGGS Cells and collections of Cells},\n  version = {0.0.1},\n  date = {2021},\n  url = {https://github.com/surroundaustralia/rhealpix-geo}\n}\n```\n\n## Contact\n_Creator & maintainer:_  \n**David Habgood**  \n_Application Architect_  \n[SURROUND Australia Pty Ltd](https://surroundaustralia.com)  \n<david.habgood@surroundaustrlaia.com>  \n\nhttps://orcid.org/0000-0002-3322-1868\n',
    'author': 'david-habgood',
    'author_email': 'david.habgood@surroundaustralia.com',
    'maintainer': 'david-habgood',
    'maintainer_email': 'david.habgood@surroundaustralia.com',
    'url': 'https://github.com/surroundaustralia/rhealpix-geo',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
