Zeno
====

Zeno's Paradoxes Illustrated in Python

Resources
---------

https://packaging.python.org/tutorials/packaging-projects/  

https://packaging.python.org/guides/distributing-packages-using-setuptools/


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


See `Makefile`

Install package from `test.pypi.org`

    pip install --index-url https://test.pypi.org/simple/ --no-deps zeno

From PyPI

    pip install zeno

Test

    python
    import zeno
    zeno.hello()

