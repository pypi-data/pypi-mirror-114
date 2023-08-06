# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['dynamic_beast']

package_data = \
{'': ['*']}

install_requires = \
['typer[all]>=0.3.2,<0.4.0']

entry_points = \
{'console_scripts': ['dynamic-beast = dynamic_beast.main:app']}

setup_kwargs = {
    'name': 'dynamic-beast',
    'version': '1.1.2',
    'description': '',
    'long_description': "# Dynamic BEAST\n\n[![PyPi](https://img.shields.io/pypi/v/dynamic-beast.svg)](https://pypi.org/project/dynamic-beast/)\n[![tests](https://github.com/Wytamma/dynamic-beast/actions/workflows/test.yml/badge.svg)](https://github.com/Wytamma/dynamic-beast/actions/workflows/test.yml)\n[![cov](https://codecov.io/gh/Wytamma/dynamic-beast/branch/master/graph/badge.svg)](https://codecov.io/gh/Wytamma/dynamic-beast)\n\nThis command line tool can be used to create a dynamic version of BEAST 2 XML files. This dynamic XML file can be used to set BEAST parameters at runtime, which can be useful for testing different configurations or quickly modifying parameters without having to edit the XML file. \n\n## Install\nInstall `dynamic-beast` with pip (requires python -V >= 3.6.2).\n\n```\npip install dynamic-beast\n```\n\n## Usage\n\nGive `dynamic-beast` the path to a BEAST2 XML file and specify where to save the dynamic XML file (if out file is not specified XML will be printed to screen).\n\n```\ndynamic-beast --outfile dynamic_BEAST.xml BEAST.xml\n```\n\nThis will produce a `dynamic_BEAST.xml` file that can be used as standard in a BEAST analysis.\n\n```\nbeast dynamic_BEAST.xml\n```\n\nTo modify parameters at run time use the `beast` definitions option `-D`.\n\n```bash\n# change the ChainLength to 1000. \nbeast -D 'mcmc.ChainLength=1000' dynamic_mcmc.xml\n``` \n\nMultiple definitions can be passed at the same time \n\n```bash\n# change the treelog and tracelog sampling freq to 10000. \nbeast -D 'treelog.logEvery=10000,tracelog.logEvery=10000' dynamic_mcmc.xml\n``` \n\n## Explanation\n\nThe `dynamic-beast` tool replaces all the parameter values in the XML file with the `$(id.key=value)` format. The value variable is the default value that was initially specified in the XML file. However, the value can be redefined when running a BEAST analysis by making use of the [BEAST2 definitions option](https://www.beast2.org/2021/03/31/command-line-options.html#-d) (`-D`) that allows for user specified values. \n\nTo ensure reproducibility you should recreate static XML files of runs using dynamic parameters, this can be achieved using the `-DFout` argument e.g., `beast -D ‘clockRate=0.0002’ -DFout static_mcmc.xml dynamic_mcmc.xml`. ",
    'author': 'Wytamma Wirth',
    'author_email': 'wytamma.wirth@me.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6.2,<4.0',
}


setup(**setup_kwargs)
