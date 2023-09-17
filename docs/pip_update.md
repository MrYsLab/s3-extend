## What Is pip?

Python packages are available for download from the [Python Package Index (aka pypi)](https://pypi.org/).
The installation program used to interact with pypi is named ***pip***.

The pip utility is often installed alongside Python, but this is not always the case.

If you are a Windows user or using Raspberry PI OS on the Raspberry Pi, 
pip should be available to you without any additional installation steps. 
However, you will need to make sure that you are using the latest version. 
Verifying the pip version and instructions on updating pip are explained a little further down on this page.

## Determining If Pip Is Installed On Your System

To determine if pip is installed on your system, 
open a command or terminal window, and for Windows, type:

```bash
pip --version
```

For Linux or macOS, type:
```bash
pip3 --version
```

If a version is reported, you can skip down to the section on verifying
if you have the latest version and how to update it if you do not. Otherwise,
please continue reading.

### Installing pip3 For Ubuntu 19.10 And Later

Make sure your package list is up to date. 

Open a terminal and enter:

```bash
sudo apt update
```
   
Next, install pip3 by entering the following command in your terminal:

``` bash
sudo apt install python3-pip
```

### Installing pip3 For Mac
Refer to [this article](https://evansdianga.com/install-pip-osx/) for
instructions.

## Verifying The pip3 Version
To properly install the s3-extend package, the latest version of pip
must be used. At the time of this writing, that version is 20.2.2.

To check the version of pip or pip3 installed on your computer, open a command or
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
 
If your pip version is earlier than 20.2.2, you should update it to
the latest version. To do so, open a command or terminal window and type the
following:

### Windows

```
python -m pip install --upgrade pip
```

### Mac and Linux (Including Raspberry Pi)

```
pip3 install --upgrade pip
```
<br>


