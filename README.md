## GIBS ColorMaps

[GIBS](https://wiki.earthdata.nasa.gov/display/GIBS/) is a powerful imagery service maintained by NASA, often used in tiling applications. This package leverages the wide variety of color maps GIBS has to offer and presents a Python-based implementation via `matplotlib`. For more information regarding GIBS and their services, check out their GitHub [repo](https://github.com/nasa-gibs) and their [landing site](https://earthdata.nasa.gov/about/science-system-description/eosdis-components/global-imagery-browse-services-gibs).

---

## Installation
To install the latest version of `cmgibs` to your own environment:

```bash
$ cd <target_dir>
```
Make sure your environment is activated; on Linux,
```bash
$ source <env_name>/bin/activate
$ pip install -e git+https://github.com/asascience-open/cmgibs.git@v0.0.2-dev#egg=cmgibs
```

## Usage
To use the color maps available in `cmgibs`, just import the module:

```python
import cmgibs
import matplotlib.cm

for name, cmap in cmgibs.cmap_d.items():
    matplotlib.cm.register_cmap(name=name, cmap=cmap)
```

## Development
Pull requests are welcome! If you'd like to contribute, please fork.

A note on tests: unit tests are implemented to make sure we don't unintentionally break the code. To make sure you're testing *your* new code and not just the existing package:

First make sure you're in the correct directory with your environment activated and use the `pip install -e .` (`-e` for 'editable') to install your local project. This way, your unit tests will be referencing your code and not the stable package.

```bash
(env) $ cd ~/cmgibs
(env) $ pip install -e .
```

You can run the unit tests with any testing framework of your choice; I use `pytest`.
```bash
$ pytest [-v]
```
