<p align="left">
<img src="./preview/pyfetch.png">
</p>

# pyfetch
Stylish and simple fetch for your terminal that is customizable and fast.

# Dependencies
* [Python 3](https://python.org)
* [fontawesome](https://fontawesome.com/) on your system
* [distro](https://pypi.org/project/distro/) package on PyPi (only for linux systems)
* [psutil](https://pypi.org/project/psutil/) package on PyPi
* [colorama](https://pypi.org/project/colorama/) package on PyPi

# Installation

## Installation through the binary
* Get the latest release through [here](https://github.com/kreat0/pyfetch/releases)
* Copy the binary to /usr/bin 
* Make it an executable by running `chmod +x /usr/bin/pyfetch`

## Installation from source
* Clone the repo
* Type `pip install distro colorama psutil` to install the dependencies (for Windows, it's only `pip install colorama psutil` but for Gentoo its `pip install distro colorama psutil --user`. The binary may also be accessable at `pip3`, `python3 -m pip`, `python -m pip`, `py3 -m pip`, or `py -m pip`.)
* Type `make install` as root
* Enjoy!

## Installation through the AUR package
```
git clone https://aur.archlinux.org/packages/pyfetch-git.git
cd pyfetch-git
makepkg -si
```
Or use an AUR helper like `yay`:
`yay -S pyfetch-git`

# Credits
* Yellowsink
* mugman
