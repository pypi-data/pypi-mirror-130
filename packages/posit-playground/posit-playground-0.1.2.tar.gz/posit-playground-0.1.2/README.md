<a href="https://github.com/urbanij/posit-playground/actions"><img src="https://github.com/urbanij/posit-playground/actions/workflows/main.yml/badge.svg"></a>
[![codecov](https://codecov.io/gh/urbanij/posit-playground/branch/main/graph/badge.svg?token=U37RUDDRN1)](https://codecov.io/gh/urbanij/posit-playground)

# posit-playground

Posit library with no frills

## Install

- stable

```sh
pip install posit-playground
```

<!-- - main

```sh
pip install git+https://github.com/urbanij/posit-playground.git
``` -->

## Usage

```python
from posit_playground import posit

p1 = posit.from_bits(
    bits = 0b000110111011101, 
    size = 16, 
    es = 3,
)

p1 * p1 # implements posit multiplication
```

or better yet, launch a notebook on binder 

[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/urbanij/posit-playground/HEAD?labpath=notebooks%2F1_posit_decode.ipynb)

or visit [notebooks/1_posit_decode.ipynb](https://github.com/urbanij/posit-playground/blob/main/notebooks/1_posit_decode.ipynb)


## Demo

[![asciicast](https://asciinema.org/a/455652.svg)](https://asciinema.org/a/455652)


Screenshot of posit-playground in action, with a corner case example in which the exponent is chopped off the bit fields

![Imgur](https://imgur.com/0M8USPC.jpg)
