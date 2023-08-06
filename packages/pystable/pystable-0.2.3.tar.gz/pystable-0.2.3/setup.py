# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pystable', 'pystable._extensions']

package_data = \
{'': ['*'],
 'pystable._extensions': ['linux/gclib-2-31/*',
                          'linux/gclib-2-33/*',
                          'macOS/arm/*',
                          'macOS/i386/*']}

install_requires = \
['setuptools>=57.1.0,<58.0.0']

setup_kwargs = {
    'name': 'pystable',
    'version': '0.2.3',
    'description': 'Python wrapper for the libstable C library',
    'long_description': "# pystable\n\nPython wrapper for the [`libstable`](https://www.jstatsoft.org/article/view/v078i01) C library.\n\n## Example\n\nTo fit with ML estimation:\n\n```python\nimport pystable\n\ninit_fit = {'alpha': 2, 'beta': 0, 'sigma': 1, 'mu': 0,\n            'parameterization': 1}\ndist = pystable.create(init_fit['alpha'], init_fit['beta'],\n                       init_fit['sigma'], init_fit['mu'],\n                       init_fit['parameterization'])\n\npystable.fit(dist, data, len(data))\nfit_params = [dist.contents.alpha, dist.contents.beta,\n              dist.contents.sigma, dist.contents.mu_0, dist.contents.mu_1]\n```\n\n## Setup\n### Dependencies\nInstall the GNU Scientific Library (GSL).\n\nArch Linux:\n```\n$ yay gsl\n```\n\nMac:\n```\n$ brew install gsl\n```\n\nUbuntu:\n```\n$ sudo apt install gsl-bin libgsl0-dev\n```\n\n### Build `libstable`\n```\n$ cd libstable\n$ make\n```\n\nor\n\n```\n$ poetry build\n```\n\n## TODO\n- [x] `import ctypes as ct`\n- [x] create lib structure\n- [x] create example file utilizing pystable lib\n- [ ] typings\n- [ ] handle errors\n  - [ ] handle NULL pointer errors\n  - [ ] handle `err`\n- [x] `stable_checkparams`\n  - [x] impl\n  - [x] test\n  - [x] example\n  - [ ] handle error\n  - [ ] test error\n- [x] `stable_create`\n  - [x] impl\n  - [x] test\n  - [x] example\n- [x] `stable_cdf`\n  - [x] impl\n  - [x] test\n  - [x] example\n- [x] `stable_pdf`\n  - [x] impl\n  - [x] test\n  - [x] example\n- [x] `stable_fit`\n  - [x] impl\n  - [ ] test\n  - [ ] example\n- [ ] `stable_q`\n  - [x] impl\n  - [x] test\n  - [ ] example\n- [ ] `stable_rnd`\n  - [x] impl\n  - [ ] test\n  - [ ] example\n",
    'author': 'RJ Rybarczyk',
    'author_email': 'rj@rybar.tech',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/overlay-market/pystable',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9.5,<4.0.0',
}


setup(**setup_kwargs)
