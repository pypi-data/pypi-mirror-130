# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['packelf']

package_data = \
{'': ['*']}

entry_points = \
{'console_scripts': ['packelf = packelf.cli:main']}

setup_kwargs = {
    'name': 'packelf',
    'version': '0.2.0',
    'description': 'Pack ELF files in a given path to make them relocatable',
    'long_description': '# packelf\n\nA _packelf_ packs ELF files by relocating linked shared objects.\nIt copies linked shared objects into `.lib` directory of the given path and rewrite `rpath` of ELF files by [patchelf][] to make them relocatable.\n\n## Requirements\n\n- [patchelf][]\n\n[patchelf]: https://nixos.org/patchelf.html\n\n## Limitation\n\n- It may break ELF files which already use `rpath` to change reference of shared objects\n\n## See also\n\n- [refreeze-scripts](https://github.com/fixpoint/refreeze-scripts) - Make EXE files in `Scripts` directory relocatable\n',
    'author': 'Fixpoint, Inc.',
    'author_email': 'developer@fixpoint.co.jp',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/fixpoint/packelf',
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
