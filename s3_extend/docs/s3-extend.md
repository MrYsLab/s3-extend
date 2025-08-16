## Installing The Python Extension Servers

Follow [these instructions](https://packaging.python.org/en/latest/guides/installing-using-pip-and-virtual-environments/) to create a virtual environment.

After activating the virtual environment, open a terminal window and type:


```angular2html
pip install s3-extend
```
### Raspberry Pi Install Instructions
If you are installing on a Raspberry Pi 2, 3, or 4 install the pigpio library by 
typing:

```angular2html
pip install pigpio
```

#### Special Install Instructions For Bullseye Version Of Raspberry Pi OS

In addition to installing both s3-extend and pigpio as mentioned above,
you also need to add the libopenblas library and firefox browser. You must use 
firefox as the browser when using the [Scratch 3 editor](https://mryslab.github.io/s3onegpio/).

##### Install libopenblas
```ABAP
sudo apt install libopenblas-base libopenblas-dev
```

##### Install Firefox
Chrome does not with s3-extend. To install firefox:

```ABAP
sudo apt install firefox-esr -y
```

**IMPORTANT NOTE:** _Raspberry PI 5 is not supported._

<br>
 It may take several minutes to download and install the necessary
Python packages to support all the extensions.
 


