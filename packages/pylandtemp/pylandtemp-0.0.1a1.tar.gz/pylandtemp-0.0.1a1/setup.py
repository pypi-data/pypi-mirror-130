from setuptools import setup, find_packages
import pathlib

here = pathlib.Path(__file__).parent.resolve()
long_description = (here / "README.md").read_text(encoding="utf-8")

setup(
    name="pylandtemp",
    version="0.0.1-alpha.1",
    description="Compute land surface temperature(LST) from Landsat-8 data",
    author="Oladimeji Mudele",
    license="Apache",
    long_description_content_type="text/markdown",
    long_description=long_description,
    url="https://github.com/pylandtemp/pylandtemp",
    # packages=["pylandtemp", "emissivity", "temperature"],
    packages=find_packages(),
    install_requires=[
        "numpy",
    ],
    keywords="Image processing, Landsat, Satellite images",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Education",
        "Topic :: Software Development :: Build Tools",
        "Programming Language :: Python :: 3.8",
    ],
    python_requires=">=3.8",
)
