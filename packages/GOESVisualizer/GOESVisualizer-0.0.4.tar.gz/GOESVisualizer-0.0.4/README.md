# GOESVisualizer

A simple toolbox to retrieve/visualize/save GOES16(east) and GOES17(west) RGB image over a region of interest

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install GOESVisualizer.

```bash
pip install GOESVisualizer
```

## Usage

see example.py

or

```bash
from GOESVisualizer import GSVis

GSobj = GSVis('west',2021,7,21,20,-125,-117,35,45)
# only plot
GSobj.plotGS()
# or only save
GSobj.plotGS(True,'goessample.png')

```

## License
[MIT](https://choosealicense.com/licenses/mit/)
