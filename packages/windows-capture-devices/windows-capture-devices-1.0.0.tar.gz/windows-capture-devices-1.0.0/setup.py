import setuptools
from distutils.core import setup, Extension

setup(
    name='windows-capture-devices',
    version='1.0.0',
    author='Michael Barz',
    author_email='michael.barz@dfki.de',
    license='MIT',
    url="https://github.com/DFKI-Interactive-Machine-Learning/python-capture-device-list",
    description='A lightweight package to list capture devices on Windows using DirectShow',
    ext_modules=[
        Extension(
            'windows_capture_devices',
            sources=['windows_capture_devices.cpp']
        )
    ]
)
