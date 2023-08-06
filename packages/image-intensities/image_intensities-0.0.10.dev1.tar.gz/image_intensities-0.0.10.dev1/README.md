# image_intensities
Python implementation of the great [derpibooru/image_intensities](https://github.com/derpibooru/image_intensities/tree/8aa43674f61f77cfc756c23556b6ae45e1b210b1).

# dependencies

### libpng (for pure python)
- MacOS: `brew install libpng` (tested to work with 1.6.37)
- Ubuntu: `sudo apt-get update && sudo apt-get install libpng-dev`
- Dockerfile, Ubuntu based: `apt-get update -y && apt-get install -y libpng-dev && apt-get clean && rm -rfv /var/lib/apt/lists/*`

```python
from image_intensities import rgb_luma_from_filename, Luma

luma = rgb_luma_from_filename('/path/to/image.png')

# returns something like
luma == Luma(nw=0.42, ne=0.44, sw=0.58, se=0.69)
```


### Minimal installation example

Using docker to get a barebones system with as much missing dependencies as possible:

```sh
# docker run -it --rm python:3.9 bash
pip install image_intensities 
```
