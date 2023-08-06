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
    'version': '0.1.0',
    'description': '',
    'long_description': '# Dynamic BEAST\n\nThis command line tool can be used to create a dynamic version of BEAST 2 XML files. This dynamic XML file can be used to set BEAST parameters at runtime, which can be useful for testing different configurations or quickly modifying parameters without having to edit the XML file. \n\nTo make a BEAST XML file dynamic simple pass it to the tool. \n\n```\ndynamic-beast BEAST.xml\n```\n\nThis will produce a `dynamic_BEAST.xml` file that can be used as standard in a BEAST analysis.\n\nThe `dynamic-beast` tool replaces all the parameter values in the XML file with `$(id.key=value)` format. The value variable is the default value that was initially specified in the XML file. However, the value can be redefined when running a BEAST analysis by making use of the BEAST2 definitions argument (`-D`) that allows for user specified values. \n\nFor example, change the sampling frequency of a sampling:\n\n```bash\nbeast -D ‘mcmc.ChainLength=100000000,treelog.logEvery=10000,tracelog.logEvery=10000’ dynamic_mcmc.xml\n``` \n\nTo ensure reproducibility you should recreate static XML files of runs using dynamic parameters, this can be achieved using the `-DFout` argument e.g., `beast -D ‘clockRate=0.0002’ -DFout static_mcmc.xml dynamic_mcmc.xml`. ',
    'author': 'Wytamma Wirth',
    'author_email': 'wytamma.wirth@me.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
