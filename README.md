# python-pkgbuild
Python library to parse pacman's .SRCINFO file

## Usage
```
>>> from pkgbuild import SRCINFO
>>> import json
>>> srcinfo = SRCINFO("/path/to/.SRCINFO")
>>> json.dumps(srcinfo.content)
'{"pkgrel": "1", "options": ["debug", "!strip"], "pkgbase": "sway-git", "license": "MIT", 
"pkgname": "sway-git", "makedepends": ["cmake", "git", "asciidoc"], "optdepends": 
["rxvt-unicode: Default terminal emulator.", "dmenu: Default for launching applications.", 
"imagemagick: For taking screenshots.", "ffmpeg: For recording screencasts.", "i3status: To 
display system information with a bar."], "url": "https://github.com/SirCmpwn/sway", "pkgdesc": 
"i3 compatible window manager for Wayland", "arch": ["i686", "x86_64"], "source": 
"sway::git+https://github.com/SirCmpwn/sway.git", "sha1sums": "SKIP", "pkgver": "r1302.016a774", 
"depends": ["wlc-git", "xorg-server-xwayland", "xcb-util-image", "json-c", "pango", "cairo", 
"wayland", "gdk-pixbuf2"]}'
```

## Installation
```
python setup.py install
```
It is also available in the [AUR](https://aur.archlinux.org/packages/python-pkgbuild)
