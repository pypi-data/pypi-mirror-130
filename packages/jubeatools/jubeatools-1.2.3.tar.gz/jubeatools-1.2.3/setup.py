# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['jubeatools',
 'jubeatools.cli',
 'jubeatools.cli.tests',
 'jubeatools.cli.tests.data',
 'jubeatools.formats',
 'jubeatools.formats.jubeat_analyser',
 'jubeatools.formats.jubeat_analyser.memo',
 'jubeatools.formats.jubeat_analyser.memo1',
 'jubeatools.formats.jubeat_analyser.memo2',
 'jubeatools.formats.jubeat_analyser.mono_column',
 'jubeatools.formats.jubeat_analyser.tests',
 'jubeatools.formats.jubeat_analyser.tests.data',
 'jubeatools.formats.jubeat_analyser.tests.memo',
 'jubeatools.formats.jubeat_analyser.tests.memo1',
 'jubeatools.formats.jubeat_analyser.tests.memo2',
 'jubeatools.formats.jubeat_analyser.tests.mono_column',
 'jubeatools.formats.konami',
 'jubeatools.formats.konami.eve',
 'jubeatools.formats.konami.eve.tests',
 'jubeatools.formats.konami.jbsq',
 'jubeatools.formats.malody',
 'jubeatools.formats.malody.tests',
 'jubeatools.formats.malody.tests.data',
 'jubeatools.formats.memon',
 'jubeatools.formats.tests',
 'jubeatools.testutils']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.0.3,<9.0.0',
 'construct-typing>=0.4.2,<0.5.0',
 'construct>=2.10,<3.0',
 'marshmallow-dataclass[union,enum]>=8.4.1,<9.0.0',
 'marshmallow>=3.6.0,<4.0.0',
 'more-itertools>=8.4.0,<9.0.0',
 'multidict>=5.1.0,<6.0.0',
 'parsimonious>=0.8.1,<0.9.0',
 'path>=15.1.2,<16.0.0',
 'python-constraint>=1.4.0,<2.0.0',
 'simplejson>=3.17.0,<4.0.0',
 'sortedcontainers>=2.3.0,<3.0.0']

entry_points = \
{'console_scripts': ['jubeatools = jubeatools.cli.cli:convert']}

setup_kwargs = {
    'name': 'jubeatools',
    'version': '1.2.3',
    'description': 'A toolbox for jubeat file formats',
    'long_description': '# Jubeatools\nA toolbox to convert between jubeat file formats\n\n## How to install\n```sh\npip install jubeatools\n```\n\nYou need Python 3.8 or greater\n\n## How to use\n```sh\njubeatools ${source} ${destination} -f ${output format} (... format specific options)\n```\n\n## Which formats are supported\n|                 |                      | input | output |\n|-----------------|----------------------|:-----:|:------:|\n| memon           | v0.2.0               | ✔️     | ✔️      |\n|                 | v0.1.0               | ✔️     | ✔️      |\n|                 | legacy               | ✔️     | ✔️      |\n| jubeat analyser | #memo2               | ✔️     | ✔️      |\n|                 | #memo1               | ✔️     | ✔️      |\n|                 | #memo                | ✔️     | ✔️      |\n|                 | mono-column (1列形式) | ✔️     | ✔️      |\n| jubeat (arcade) | .eve                 | ✔️     | ✔️      |\n| jubeat plus     | .jbsq                | ✔️     | ✔️      |\n| malody          | .mc (Pad Mode)       | ✔️     | ✔️      |\n',
    'author': 'Stepland',
    'author_email': '16676308+Stepland@users.noreply.github.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/Stepland/jubeatools',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
