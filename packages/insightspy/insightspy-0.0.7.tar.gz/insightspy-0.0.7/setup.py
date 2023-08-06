import setuptools
import os
from setuptools.command.install import install
import sys

# get key package details from insightspy/__version__.py
about = {}  # type: ignore
here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, "insightspy", "__version__.py")) as f:
    exec(f.read(), about)

# load the README file and use it as the long_description for PyPI
with open("README.md", "r") as f:
    readme = f.read()

# circleci.py version
VERSION = about["__version__"]


class VerifyVersionCommand(install):
    """Custom command to verify that the git tag matches our version"""

    description = "verify that the git tag matches our version"

    def run(self):
        tag = os.getenv("CIRCLE_TAG")

        if tag != VERSION:
            info = "Git tag: {0} does not match the version of this app: {1}".format(
                tag, VERSION
            )
            sys.exit(info)


# package configuration - for reference see:
# https://setuptools.readthedocs.io/en/latest/setuptools.html#id9
setuptools.setup(
    name=about["__title__"],
    description=about["__description__"],
    long_description=readme,
    long_description_content_type="text/markdown",
    version=VERSION,
    author=about["__author__"],
    author_email=about["__author_email__"],
    url=about["__url__"],
    packages=setuptools.find_packages(),
    install_requires=["pandas", "tqdm", "requests"],
    include_package_data=True,
    python_requires=">=3.7.*",
    classifiers=about["__classifiers__"],
    cmdclass={
        "verify": VerifyVersionCommand,
    },
)
