# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['img2ansi',
 'img2ansi.ansi',
 'img2ansi.ascii',
 'img2ansi.block',
 'img2ansi.braile']

package_data = \
{'': ['*']}

install_requires = \
['Pillow>=8.0.0,<9.0.0']

entry_points = \
{'console_scripts': ['img2ascii = img2ansi.img2ascii:main',
                     'img2block = img2ansi.img2block:main',
                     'img2braile = img2ansi.img2braile:main']}

setup_kwargs = {
    'name': 'img2ansi',
    'version': '0.1.2',
    'description': 'Convert image to ascii/unicode ANSI sequence',
    'long_description': '<div align="center">\n  <h3>\nimg2ansi is a simple package containing three CLI to convert an image to an ASCII, BRAILE/DOT, BLOCK representation with support for <a href ="https://en.wikipedia.org/wiki/ANSI_escape_code" > ANSI escape code sequence </a>\n  </h3>\n</div>\n\n<div align="center">\n  <a href="https://github.com/dax99993/img2ansi/blob/main/demo/demo.md">Demo</a>\n  <br/><br/>\n  <a href="https://github.com/dax99993/img2ansi/blob/main/LICENSE">\n    <img src="https://img.shields.io/badge/License-GPL2-greee.svg?style=flat-square" alt="license" />\n  </a>\n  <a href="https://pypi.org/project/PIL/">\n    <img src="https://img.shields.io/badge/Dependencies-PIL-blue.svg?style=flat-square" alt="dependencies" />\n  </a>\n  <a href="https://pypi.org/project/img2ansi/">\n    <img src="https://img.shields.io/badge/Package-img2ansi-red.svg?style=flat-square" alt="dependencies" />\n  </a>\n</div>\n\n## Installation\n\n```bash\n$ Python3 -m pip install img2ansi\n```\n\n## Features\n- ASCII convertion\n- BRAILE/DOT convertion\n- Block convertion\n- Custom ASCII character set\n- Invert character set\n- No echo **/** echo to terminal\n- Resize of image\n- Save to a file\n- True color\n\n## ANSI support\n- Bold\n- Blink\n- True color Foreground\n- True color Background \n\n## Todo\n- [x] Simple Ascii convertion\n- [x] Color support\n- [ ] Multiple file handling\n- [ ] Simple animation\n\n## Usage\nimg2ansi contains three modules to perform different kind of convertion\n-img2ascii\n-img2braile\n-img2block\n```\nusage: img2ascii [-h] [-a Character Set] [-F R G B] [-B R G B] [-b] [-c] [-f]\n                 [-i] [-k] [-n] [-r Width Height] [-o [output filename]]\n                 inputImage\n\nConvert img to Ascii representation\n\npositional arguments:\n  inputImage            image to be converted\n\noptional arguments:\n  -h, --help            show this help message and exit\n  -a Character Set, --asciicharset Character Set\n                        ascii character set (default : " .~*:+zM#&@$" )\n  -F R G B, --frgdcolor R G B\n                        All characters with RGB24 foreground color\n  -B R G B, --bkgdcolor R G B\n                        All characters with RGB24 background color\n  -b, --bold            bold flag\n  -c, --color           foreground text as img colors\n  -f, --fullscreen      fullscreen flag\n  -i, --invertPattern   "invert ascii character set\n  -k, --blink           blink flag\n  -n, --noecho          no echo flag\n  -r Width Height, --resize Width Height\n                        resize image (0 0 keeps original size), if given -r\n                        100 0 keeps aspectratio with 100px width\n  -o [output filename], --save [output filename]\n                        save file (if no output filename) defaults to\n                        ascii.txt\n\nBy default uses parameters -r 0 0 -a " .~*:+zM#&@$"\n\n```\n\n```\nusage: img2braile [-h] [-b] [-F R G B] [-B R G B] [-f] [-i] [-k] [-n]\n                  [-r Width Height] [-o [output filename]] [-t Threshold]\n                  inputImage\n\nConvert img to Braile representation\n\npositional arguments:\n  inputImage            image to be converted\n\noptional arguments:\n  -h, --help            show this help message and exit\n  -b, --bold            bold flag\n  -F R G B, --frgdcolor R G B\n                        All characters with RGB24 foreground color\n  -B R G B, --bkgdcolor R G B\n                        All characters with RGB24 background color\n  -f, --fullscreen      fullscreen flag\n  -i, --invertPattern   "invert Braile characters flag\n  -k, --blink           blink flag\n  -n, --noecho          no echo flag\n  -r Width Height, --resize Width Height\n                        resize image (0 0 keeps original size), if given -r\n                        100 0 keeps aspectratio with 100px width\n  -o [output filename], --save [output filename]\n                        save file (if no output filename) defaults to\n                        braile.txt\n  -t Threshold, --threshold Threshold\n                        set threshold to binarize img in braile convertion\n                        (0-255)\n\nBy default -r 0 0 -t 127\n\n```\n\n```\nusage: img2block [-h] [-f] [-W] [-k] [-n] [-r Width Height]\n                 [-o [output filename]]\n                 inputImage\n\nConvert img to Block representation\n\npositional arguments:\n  inputImage            image to be converted\n\noptional arguments:\n  -h, --help            show this help message and exit\n  -f, --fullscreen      fullscreen flag\n  -W, --wholeblock      "Use one block per terminal cell\n  -k, --blink           blink flag\n  -n, --noecho          no echo flag\n  -r Width Height, --resize Width Height\n                        resize image (0 0 keeps original size), if given -r\n                        100 0 keeps aspectratio with 100px width\n  -o [output filename], --save [output filename]\n                        save file (if no output filename) defaults to\n                        block.txt\n\nBy default uses 2 blocks per terminal cell and -r 0 0\n\n```\n\n## License\n[GPL2](https://github.com/dax99993/img2ansi/blob/main/LICENSE)\n',
    'author': 'Daniel Bañuelos',
    'author_email': 'dax99993@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
