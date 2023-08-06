# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['intents',
 'intents.connectors',
 'intents.connectors._experimental',
 'intents.connectors._experimental.alexa',
 'intents.connectors.dialogflow_es',
 'intents.helpers',
 'intents.language',
 'intents.model']

package_data = \
{'': ['*']}

install_requires = \
['google-cloud-dialogflow>=2.0.0,<3.0.0', 'pyyaml>=5.4.1,<6.0.0']

setup_kwargs = {
    'name': 'intents',
    'version': '0.2a1',
    'description': 'Define and operate Dialogflow Agents with a simple, code-first, approach',
    'long_description': '# Intents ⛺\n\n[![Documentation Status](https://readthedocs.org/projects/intents/badge/?version=latest)](https://intents.readthedocs.io/en/latest/?badge=latest)\n[![codecov](https://codecov.io/gh/dariowho/intents/branch/master/graph/badge.svg?token=XAVLW70J8S)](https://codecov.io/gh/dariowho/intents)\n[![HEAD version](https://img.shields.io/badge/head-v0.2a1-blue.svg)](https://img.shields.io/badge/head-v0.2a1-blue.svg)\n[![PyPI version](https://badge.fury.io/py/intents.svg)](https://badge.fury.io/py/intents)\n\n**Intents** is an unofficial Python framework to define and operate Dialogflow Agents with a simple,\ncode-first approach. Its main benefits are:\n\n* **Agents are Python projects**. You will develop with autocomplete, static type checking\n  and everything you are already used to.\n* **Versioning and CI**. Agents can be versioned on Git, and programmatically\n  deployed just like software.\n* **Human-friendly prediction client**. Much more straightforward than the official\n  Python SDK\n\nA detailed view of the available features can be found in\n[STATUS.md](STATUS.md). Also, check out the\n[Projects](https://github.com/dariowho/intents/projects) page to keep track of\nrecent developments.\n\n## Install\n\n```sh\npip install intents==0.2a1\n```\n\n## Usage\n\nIntents are defined like standard Python **dataclasses**:\n\n```python\n@dataclass\nclass HelloIntent(Intent):\n    """A little docstring for my Intent class"""\n    user_name: Sys.Person = "Guido"\nMyAgent.register(HelloIntent)\n```\n\nTheir **language** resources are stored in separate YAML files:\n\n```yaml\nutterances:\n  - Hi! My name is $user_name{Guido}\n  - Hello there, I\'m $user_name{Mario}\n\nresponses:\n  default:\n    - text:\n      - Hi $user_name\n      - Hello $user_name, this is Bot!\n      - Nice to meet you, $user_name\n```\n\nAgents can be **uploaded** as Dialogflow ES projects directly from code:\n\n```python\ndf = DialogflowEsConnector(\'/path/to/service-account.json\', MyAgent)\ndf.upload()  # You will find it in your Dialogflow Console\n```\n\n*Intents* will act transparently as a **prediction** client:\n\n```python\n>>> predicted = df.predict("Hi there, my name is Mario")\nHelloIntent(user_name="Mario")\n>>> predicted.fulfillment_text\n"Hello Mario, this is Bot!"\n>>> predicted.user_name\n"Mario"\n```\n\nFor a complete working example, check out the included [Example Agent](example_agent/). Also, *Intents* **documentation** is published at https://intents.readthedocs.io/ 📚\n\n## Disclaimer\n\n*This project is not affiliated, associated, authorized, endorsed by, or in any way officially connected with Dialogflow. The names Dialogflow, Google, as well as related names, marks, emblems and images are registered trademarks of their respective owners.*\n',
    'author': 'Dario',
    'author_email': 'dario.chi@inventati.org',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/dariowho/intents',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
