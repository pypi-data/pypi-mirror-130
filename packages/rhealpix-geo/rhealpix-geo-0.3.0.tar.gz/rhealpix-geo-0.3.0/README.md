# DGGS Classes for Cells and Cell Collections for parametrisations of rHEALPix grids

This library contains classes for representing DGGS Cells and collections of these ("CellCollection") according to parametrisations of the [rHEALPix Discrete Global Grid System](https://iopscience.iop.org/article/10.1088/1755-1315/34/1/012012/pdf).
This provides a convenient low level API to work with Cells and CellCollections. An example of a library that utilises these objects for higher level geospatial operations is the [rhealpix-sf library](https://github.com/surroundaustralia/rhealpix-sf) which provides a set of Simple Feature relation operations for DGGS Cells.  
  
Validation is provided for Cell and CellCollections.
CellCollections have the following operations performed on instantiation: 
- compression (where all children of a parent are present, replace with their parent)  
- deduplication (removal of repeated cells)  
- absorb (where a child and its parent are present, remove the child/children)  
- ordering (alphabetical and numerical based on suids)  

These operations provide a consistent representation of collections of Cells, allowing higher level operations to work with a simplified, valid, and consistent set of cells. 

Cells and CellCollections have the following attributes or methods:
- add: Add two sets of Cell or CellCollections, returning a CellCollection  
- subtract: Subtract a Cell or CellCollection from an other, returning a CellCollection  
- equal: Test two Cells or CellCollections for equivalence  
- len: the number of Cells in a Cell (1) or CellCollection (N)  
- area: to be implemented
- resolution / min and max resolution for CellCollections: the resolution or minimum / maximum resolution for Cells or CellCollections respectively.  
- neighbours: the Cells immediately neighbouring a Cell or CellCollection, optionally including diagonals. For CellCollections, excludes neighbouring cells interior to the CellCollection. Resolution specifiable.  
- border: the set of interior Cells along the edges of a Cell or CellCollection. Resolution specifiable.  
- children: the set of child Cells for a Cell or CellCollection. Resolution specifiable. 

## Installation 
Install from PyPi, for example using pip or poetry.  

https://pypi.org/project/rhealpix-geo/  

This package has no dependencies.

## Use
These functions are implemented in the file `rheal/dggs_classes.py`

This means they can be used like this (full working script):

```python
from rheal import Cell, CellCollection

a = Cell("R1")
b = Cell("R11")
c = CellCollection("R1 R2")
print(a + b)
# b is within a, so a CellCollection equivalent to a is returned
print(a - b)
# b is within a, so a subset of a is returned
print(a + c)
# c contains a, so a CellCollection equivalent to c is returned 
print(a == b)
# a's border at a resolution two levels higher than a's resolution
print(a.border(a.resolution+2))
# a's children at a resolution one level higher (default) than a's resolution
print(a.children())
# a's neighbours at a's resolution (default) including diagonals (default). Note only 7 neighbours due to the shape of the north hemisphere cell.
print(a.neighbours())
```

## Testing
All tests are in `tests/` and implemented using [pytest](https://docs.pytest.org/en/6.2.x/).

There are individual tests for each of the Cell and CellCollection operations. 

## Contributing
Via GitHub, Issues & Pull Requests: 

* <https://github.com/surroundaustralia/rhealpix-geo

## License
This code is licensed with the BSD 3-clause license as per [LICENSE](LICENSE).

## Citation
```bibtex
@software{https://github.com/surroundaustralia/rhealpix-geo,
  author = {{David Habgood}},
  title = {Objects for DGGS Cells and collections of Cells},
  version = {0.0.1},
  date = {2021},
  url = {https://github.com/surroundaustralia/rhealpix-geo}
}
```

## Contact
_Creator & maintainer:_  
**David Habgood**  
_Application Architect_  
[SURROUND Australia Pty Ltd](https://surroundaustralia.com)  
<david.habgood@surroundaustrlaia.com>  

https://orcid.org/0000-0002-3322-1868
