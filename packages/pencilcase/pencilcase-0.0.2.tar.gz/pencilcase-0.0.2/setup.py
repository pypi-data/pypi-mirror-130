from setuptools import setup
import pathlib

import pkg_resources

with pathlib.Path('requirements.txt').open() as requirements_txt:
    install_requires = [
        str(requirement)
        for requirement
        in pkg_resources.parse_requirements(requirements_txt)
    ]


setup(
    name="pencilcase",
    author="Chelsea Voss",
    author_email="csvoss@csvoss.com",
    description=("A little box of Python tools."),
    version="0.0.2",
    scripts=["pencilcase.py"],
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/csvoss/pencil",
    install_requires=install_requires,
)
