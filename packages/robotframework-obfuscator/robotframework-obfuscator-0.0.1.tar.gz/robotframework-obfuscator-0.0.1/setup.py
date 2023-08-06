import shutil
from pathlib import Path

from setuptools import find_packages, setup

_here = Path(__file__).parent.resolve()
_parent = _here.parent
_root = _parent.parent

_readme = _here / "README.md"
_license = _here / "LICENSE"
_copyright = _here / "COPYRIGHT"

# Note: always overwrite files from the original place if those exist.

_origin = _parent / _readme.name
if _origin.exists():
    shutil.copy2(_origin, _readme)

for path in [_license, _copyright]:
    _origin = _root / path.name
    if _origin.exists():
        shutil.copy2(_origin, path)


setup(
    name="robotframework-obfuscator",
    version="0.0.1",  # Note: here and in 'robotframework_obsfuscator/__init__.py'
    description="An obfuscator for Robot Framework code",
    long_description=_readme.read_text(),
    url="https://github.com/robocorp/robotframework-obfuscator",
    author="Fabio Zadrozny",
    license="Apache-2.0",
    copyright="Robocorp Technologies, Inc.",
    packages=find_packages(),
    zip_safe=False,
    long_description_content_type="text/markdown",
    python_requires=">=3.7",
    # List run-time dependencies here. These will be installed by pip when
    # your project is installed. For an analysis of "install_requires" vs pip's
    # requirements files see:
    # https://packaging.python.org/en/latest/requirements.html
    install_requires=["robotframework >=3.2", "robotframework-lsp >=0.29"],
    # List additional groups of dependencies here (e.g. development
    # dependencies). You can install these using the following syntax,
    # for example:
    # $ pip install -e .[test]
    extras_require={
        "test": [
            "pytest",
            "pytest-xdist",
        ],
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: POSIX",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Topic :: Text Editors",
        "Topic :: Text Editors :: Integrated Development Environments (IDE)",
        "Topic :: Software Development :: Debuggers",
        "Framework :: Robot Framework",
        "Framework :: Robot Framework :: Tool",
    ],
    package_data={},
    # To provide executable scripts, use entry points in preference to the
    # "scripts" keyword. Entry points provide cross-platform support and allow
    # pip to create the appropriate form of executable for the target platform.
    entry_points={
        "console_scripts": ["rf_obfuscator = robotframework_obfuscator.__main__:main"],
    },
)
