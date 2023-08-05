from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name ='geometryobject',
    version = '1.0',
    py_modules = ['geometryobject'],
    author = 'samuelliem',
    author_email = 'samuelliem99@gmail.com',
    url = "https://github.com/samuelliem",
    description = 'Aplication program to print some 2d geometry object',
    long_description=long_description,
    long_description_content_type="text/markdown",
)