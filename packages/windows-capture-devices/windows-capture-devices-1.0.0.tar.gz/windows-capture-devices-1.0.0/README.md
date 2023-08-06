# List Capture Devices on Windows using DirectShow
This is a simple and lightweight Python extension that allows developers to enumerate capture devices. The device names can be used to open capture devices with, for instance, [PyAV](https://pyav.org/). The extension can be used as follows:

```python
from windows_capture_devices import get_capture_devices
device_list = get_capture_devices()
```

We use this extension in the `WebcamSource` of our [**multisensor-pipeline**](https://github.com/DFKI-Interactive-Machine-Learning/multisensor-pipeline).

## Setup

* From PyPI (recommended)
  ```commandline
  pip install windows-capture-devices
  ```
* From source (we recommend to use an Anaconda environment for building the package)
  ```commandline
  python setup.py build install
  ```
* Build a wheel
  ```commandline
  pip install wheel
  python setup.py bdist_wheel 
  ```

## PyAV Example
We include an example for grabbing an image frame using PyAV in `demo.py`. The demo has additional dependencies:

```commandline
conda install av -c conda-forge
pip install Pillow
```

## Credits
This repository is forked from https://github.com/yushulx/python-capture-device-list.