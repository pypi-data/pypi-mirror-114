import sys
from pathlib import Path

from setuptools import setup

import pyall.constants as C

assert sys.version_info >= (3, 8), "pyall requires Python 3.8+"

__all__ = ["CURRENT_DIR", "get_long_description"]

CURRENT_DIR = Path(__file__).parent


def get_long_description():
    readme_md = CURRENT_DIR / "README.md"
    with open(readme_md, encoding="utf8") as ld_file:
        return ld_file.read()


setup(
    name="pyall",
    version=C.VERSION,
    description=C.DESCRIPTION,
    long_description=get_long_description(),
    long_description_content_type="text/markdown",
    keywords=["__all__"],
    author="Hakan Çelik",
    author_email="hakancelik96@outlook.com",
    url="https://github.com/hakancelik96/pyall",
    project_urls={
        "Documentation": "https://pyall.hakancelik.dev/",
        "Issues": "https://github.com/hakancelik96/pyall/issues",
    },
    license="GNU General Public License v3.0",
    license_file="LICENSE",
    python_requires=">=3.8",
    packages=["pyall"],
    install_requires=[],
    extras_require={
        "docs": [
            "mkdocs==1.2.1",
            "mkdocs-material==7.1.9",
            "mkdocs-markdownextradata-plugin==0.2.4",
            "mkdocs-minify-plugin==0.4.0",
            "mkdocs-git-revision-date-localized-plugin==0.9.2",
        ],
        "dev": [
            "pytest==6.2.4",
            "pytest-cov==2.12.1",
        ],
    },
    zip_safe=False,
    include_package_data=True,
    classifiers=[
        "Development Status :: 4 - Beta",
        "License :: OSI Approved :: MIT License",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Environment :: Console",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: Implementation :: CPython",
    ],
    entry_points={"console_scripts": ["pyall = pyall.main:main"]},
)
