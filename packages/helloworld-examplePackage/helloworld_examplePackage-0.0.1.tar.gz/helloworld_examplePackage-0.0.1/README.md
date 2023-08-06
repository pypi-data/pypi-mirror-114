# Hello World
This is an example/format project demonstrating how to publish a python module to PyPI.

```python
pip install helloworld
```

# Developing Hello World
To install helloworld, along with the tools you need to develop and run tests, run the following in you virtualenv:

```bash
$ pip install -e .[dev]
```

## Usage
```python
from helloworld import say_hello

# Generate "Hello, World!"
say_hello()

# Generate "Hello, Everybody!"
say_hello("Everybody")
```
