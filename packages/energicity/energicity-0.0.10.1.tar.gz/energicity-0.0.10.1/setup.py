from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='energicity',
    version='0.0.10.1',
    description="EnergiCity main python package, it's a toolkit",
    py_modules=["hello", "powerleone"],
    package_dir={"":"src"},
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://gitlab.com/EnergiCity/energicity-py-package',
    author="Ahmed Ali",
    author_email='ahmed.elsir.khalfalla@gmail.com',
    install_requires = [
        "requests",
    ],
    extras_requires = {
        "dev": [
            "twine",
        ],
    }
)
