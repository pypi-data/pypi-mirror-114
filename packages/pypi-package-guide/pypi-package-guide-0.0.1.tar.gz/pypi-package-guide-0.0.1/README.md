
# PyPI Package Template

[![Supported Versions](https://img.shields.io/pypi/pyversions/kibana-api.svg)](https://pypi.org/project/kibana-api/)
[![Downloads](https://pepy.tech/badge/kibana-api/month)](https://pepy.tech/project/kibana-api/)

## Requirements
 * Python >= 3.6

    . . .
    
 * Linux Only


## Installation

You can find this package at https://pypi.org/project/pypi-package-template

```bash
pip install pypi-package-template
```

## Features
* Feature 0, short description
* Feature 1, short description
* Feature 2, short description

    . . .

* Feature N, short description



## Usage and Examples

#### Feature 1 

Description 
```python
from pypi-package-template import Phraser
phraser = Phraser()
phrase = phraser.get_random_phrase()
# ¿Quieres ser rico? Pues no te afanes es aumentar tus bienes, sino en disminuir tu codicia (Epicuro )
```

 . . .

## Testing

```bash
python -m unittest tests.tests 
```

## Contributing

You rules

## License
All other code in this repository is licensed under a MIT license.

## Contact Me

My blog: [cr0wg4n](https://cr0wg4n.medium.com/) 
Twitter: [cr0wg4n](https://twitter.com/cr0wg4n) 
Linkedin: [cr0wg4n](https://www.linkedin.com/in/cr0wg4n/) 


## Upload Package to PYPI (only-for-demo)

Install some dependencies to build your package:
```bash
pip install sdist setuptools twine
```


Create your build:
```bash
python setup.py sdist
```

then two directories appear:
- <your_package_name>.egg-info
- dist/<your_package_name>-<your_version>.tar.gz

You can prove your package build before upload:
```bash
pip install -e ./dist/<your_package_name>-<your_version>.tar.gz
```

Upload your package, you must be logged at https://pypi.org/ before, after that:
```bash
## Introduce your credentials, remmember it!
twine upload dist/*
```

And finally, you package is up!

