# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['nautobot_chatops_ansible', 'nautobot_chatops_ansible.tests']

package_data = \
{'': ['*'],
 'nautobot_chatops_ansible': ['static/nautobot_ansible/*'],
 'nautobot_chatops_ansible.tests': ['fixtures/*']}

install_requires = \
['nautobot-chatops>=1.1.0,<2.0.0', 'requests>=2.25.1,<3.0.0']

entry_points = \
{'nautobot.workers': ['ansible = nautobot_chatops_ansible.worker:ansible']}

setup_kwargs = {
    'name': 'nautobot-chatops-ansible',
    'version': '1.0.0',
    'description': 'Nautobot Chatpops Ansible Tower integration',
    'long_description': '# nautobot-plugin-chatops-ansible\n\nA plugin for [Nautobot](https://github.com/nautobot/nautobot) [Chatops Plugin](https://github.com/nautobot/nautobot-plugin-chatops/)\n\n## Installation\n\n### Build Status\n\n| Branch      | Status |\n|-------------|------------|\n| **main** | [![Build Status](https://www.travis-ci.com/nautobot/nautobot-plugin-chatops-ansible.svg?token=D7kytCzfCypoGoueSBqJ&branch=main)](https://www.travis-ci.com/github/nautobot/nautobot-plugin-chatops-ansible) |\n| **develop** | [![Build Status](https://www.travis-ci.com/nautobot/nautobot-plugin-chatops-ansible.svg?token=D7kytCzfCypoGoueSBqJ&branch=develop)](https://www.travis-ci.com/github/nautobot/nautobot-plugin-chatops-ansible) |\n\nThe plugin is available as a Python package in PyPI and can be installed with pip\n\n```shell\npip install git+https://github.com/nautobot/nautobot-plugin-chatops-ansible.git\n```\n\nThis ChatOps Plugin to Nautobot ChatOps Plugin requires the following list of environment variables to be added into the environment.\n\n- `NAUTOBOT_TOWER_URI`: Ansible Tower HTTP URI\n- `NAUTOBOT_TOWER_USERNAME`: Ansible Tower username\n- `NAUTOBOT_TOWER_PASSWORD`: Ansible Tower password\n\nOnce you have updated your environment file, restart both nautobot and nautobot-worker\n\n```\n$ sudo systemctl restart nautobot nautobot-worker\n```\n\n## Usage\n\n### Command setup\n\nAdd a slash command to Slack called `/ansible`.\nSee the [nautobot-chatops installation guide](https://github.com/nautobot/nautobot-plugin-chatops/blob/develop/docs/chat_setup.md) for instructions on adding a slash command to your Slack channel.\n\nYou may need to adjust your [Access Grants in Nautobot](https://github.com/nautobot/nautobot-plugin-chatops/blob/develop/docs/chat_setup.md#grant-access-to-the-chatbot) depending on your security requirements.\n\n## Contributing\n\nPull requests are welcomed and automatically built and tested against multiple version of Python and multiple version of Nautobot through TravisCI.\n\nThe project is packaged with a light development environment based on `docker-compose` to help with the local development of the project and to run the tests within TravisCI.\n\nThe project is following Network to Code software development guideline and is leveraging:\n\n- Black, Pylint, Bandit and pydocstyle for Python linting and formatting.\n- Django unit test to ensure the plugin is working properly.\n\n### CLI Helper Commands\n\nThe project is coming with a CLI helper based on [invoke](http://www.pyinvoke.org/) to help setup the development environment. The commands are listed below in 3 categories `dev environment`, `utility` and `testing`.\n\nEach command can be executed with `invoke <command>`. All commands support the arguments `--nautobot-ver` and `--python-ver` if you want to manually define the version of Python and Nautobot to use. Each command also has its own help `invoke <command> --help`\n\n#### Local dev environment\n\n```no-highlight\n  build            Build all docker images.\n  debug            Start Nautobot and its dependencies in debug mode.\n  destroy          Destroy all containers and volumes.\n  start            Start Nautobot and its dependencies in detached mode.\n  stop             Stop Nautobot and its dependencies.\n```\n\n#### Utility\n\n```no-highlight\n  cli              Launch a bash shell inside the running Nautobot container.\n  create-user      Create a new user in django (default: admin), will prompt for password.\n  makemigrations   Run Make Migration in Django.\n  nbshell          Launch a nbshell session.\n```\n\n#### Testing\n\n```no-highlight\n  tests            Run all tests.\n  pydocstyle       Run pydocstyle to validate docstring formatting adheres to NTC defined standards.\n  bandit           Run bandit to validate basic static code security analysis.\n  black            Run black to check that Python files adhere to its style standards.\n  unittest         Run Django unit tests for the plugin.\n```\n\n## Questions\n\nFor any questions or comments, feel free to swing by the [Network to Code slack channel](https://networktocode.slack.com/) (channel #networktocode).\nSign up [here](http://slack.networktocode.com/)\n',
    'author': 'Network to Code, LLC',
    'author_email': 'opensource@networktocode.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/nautobot/nautobot-plugin-chatops-ansible',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
