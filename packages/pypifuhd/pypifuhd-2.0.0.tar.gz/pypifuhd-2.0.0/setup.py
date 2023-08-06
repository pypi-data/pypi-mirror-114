import pathlib
from setuptools import find_packages, setup

# The directory containing this file
base_dir = pathlib.Path(__file__).parent

# The text of the README file
README = (base_dir / "README.md").read_text()

with open('requirements.txt') as f:
    required = f.read().splitlines()

# This call to setup() does all the work
setup(
    name="pypifuhd",
    version="2.0.0",
    description="pypifuhd: Python tools for processing 3D face",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/lingtengqiu/Open-PIFuhd",
    author="lingtengqiu",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
    ],
    packages=find_packages(),
    include_package_data=True,
    install_requires=required,
    entry_points={
        "console_scripts": [
            "realpython=reader.__main__:main",
        ]
    },
)
