## What Is pip?

***pip*** is the package installer for Python. You can use pip to
install packages from the
[Python Package Index (aka pypi)](https://pypi.org/) and other indexes.
***pip*** is the tool used to download and install the s3-extend Python
packages from pypi.


***pip*** is typically installed when Python is installed. However, that
is not the case for Ubuntu 19.04. For the Mac, you may also need to
install it separately.

For Windows and Raspbian, pip is installed, so you can skip to the next
section verifying the pip version.

### Installing pip3 For Ubuntu 19.04

Make sure your package list is up to date. 

Open a terminal and enter:

```bash
sudo apt update
```
   
Next, install pip3 by entering the following command in your terminal:

``` bash
sudo apt install python3-pip
```

### Installing pip3 Mac
Refer to [this article](https://evansdianga.com/install-pip-osx/) for
instructions.

## Verifying The pip3 Version
To properly install the s3-extend package, the latest version of pip
must be used. At the time of this writing, that version is 19.2.3.

To check the pip3 version installed on your computer, open a command or
terminal window, and type the following:

### Windows

```
pip --version
```

### Mac and Linux (Including Raspberry Pi)

```
pip3 --version
```

## Updating pip3
 
If your pip version is earlier than 19.2.3, here is how to update it to
the latest version. Open a command or terminal windows and type the
following:

### Windows

```
python -m pip install --upgrade pip
```

### Mac and Linux (Including Raspberry Pi)

```
sudo pip install --upgrade pip
```
<br>
<br>
<br>


Copyright (C) 2019 Alan Yorinks All Rights Reserved

