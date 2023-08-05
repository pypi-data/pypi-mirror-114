# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['minos',
 'minos.saga',
 'minos.saga.definitions',
 'minos.saga.executions',
 'minos.saga.executions.executors']

package_data = \
{'': ['*']}

install_requires = \
['dependency-injector>=4.32.2,<5.0.0',
 'minos-microservice-common>=0.1.6,<0.2.0']

setup_kwargs = {
    'name': 'minos-microservice-saga',
    'version': '0.0.8',
    'description': 'Saga Library for MinOS project.',
    'long_description': "# Minos Microservice Saga\n\n[![codecov](https://codecov.io/gh/Clariteia/minos_microservice_saga/branch/main/graph/badge.svg)](https://codecov.io/gh/Clariteia/minos_microservice_saga)\n![Tests](https://github.com/Clariteia/minos_microservice_saga/actions/workflows/python-tests.yml/badge.svg)\n\nMinos is a framework which helps you create [reactive](https://www.reactivemanifesto.org/) microservices in Python.\nInternally, it leverages Event Sourcing, CQRS and a message driven architecture to fulfil the commitments of an\nasynchronous environment.\n\n## Documentation\n\nThe official documentation as well as the API you can find it under https://clariteia.github.io/minos_microservice_saga/. \nPlease, submit any issue regarding documentation as well!\n\n## Set up a development environment\n\nMinos uses `poetry` as its default package manager. Please refer to the\n[Poetry installation guide](https://python-poetry.org/docs/#installation) for instructions on how to install it.\n\nNow you con install all the dependencies by running\n```bash\nmake install\n```\n\nIn order to make the pre-commits checks available to git, run\n```bash\npre-commit install\n```\n\nMake yourself sure you are able to run the tests. Refer to the appropriate section in this guide.\n\n## Run the tests\n\nIn order to run the tests, please make sure you have the [Docker Engine](https://docs.docker.com/engine/install/)\nand [Docker Compose](https://docs.docker.com/compose/install/) installed.\n\nMove into `tests/` directory\n\n```bash\ncd tests/\n```\nRun service dependencies:\n\n```bash\ndocker-compose up -d\n```\n\nInstall library dependencies:\n\n```bash\nmake install\n```\n\nRun tests:\n\n```bash\nmake test\n```\n\n## How to contribute\n\nMinos being an open-source project, we are looking forward to having your contributions. No matter whether it is a pull\nrequest with new features, or the creation of an issue related to a bug you have found.\n\nPlease consider these guidelines before you submit any modification.\n\n### Create an issue\n\n1. If you happen to find a bug, please file a new issue filling the 'Bug report' template.\n2. Set the appropriate labels, so we can categorise it easily.\n3. Wait for any core developer's feedback on it.\n\n### Submit a Pull Request\n\n1. Create an issue following the previous steps.\n2. Fork the project.\n3. Push your changes to a local branch.\n4. Run the tests!\n5. Submit a pull request from your fork's branch.\n\n## Credits\n\nThis package was created with ![Cookiecutter](https://github.com/audreyr/cookiecutter) and the ![Minos Package](https://github.com/Clariteia/minos-pypackage) project template.\n",
    'author': 'Clariteia Devs',
    'author_email': 'pypi@clariteia.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://clariteia.com',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
