import pathlib
from setuptools import setup

HERE = pathlib.Path(__file__).parent

README = (HERE/"README.rst").read_text()

setup(
    name="groveGPS",
    version="1.0.2",
    description="Connect to Grove GPS and perform calculations on GPS values",
    long_description=README,
    long_description_content_type="text/x-rst",
    url="https://github.com/Paolo-dono/Grove_GPS",
    author="Paulus Jacobus de Bruyn",
    author_email="mailforpaolo@yahoo.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    packages=["grove_gps","location_calcs"],
    include_package_data=True,
    install_requires=[
        "pyserial",
        "datetime",
    ],
)