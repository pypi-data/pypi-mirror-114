Zeno
====

Zeno's Paradoxes Illustrated in Python


Resources
---------

https://en.wikipedia.org/wiki/Zeno%27s_paradoxes


Usage
-----

    pip install zeno

Executables are prefixed with `ze-`

    # The Dichotomy
    ze-dichotomy


Development
-----------

In addition to following the setup guide https://packaging.python.org/tutorials/packaging-projects/

I added a minimal `setup.py` so that `pip install -e .` would work

See `Makefile` for build and upload options

Install package from `test.pypi.org` (uploaded with `make test_upload`)

    pip install --index-url https://test.pypi.org/simple/ --no-deps zeno
