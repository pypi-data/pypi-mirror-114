# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pycm']

package_data = \
{'': ['*']}

install_requires = \
['cryptography>=3.3.1,<4.0.0',
 'python-dotenv>=0.15.0,<0.16.0',
 'pyyaml>=5.3.1,<6.0.0']

entry_points = \
{'console_scripts': ['pycm = pycm.cli:pycm']}

setup_kwargs = {
    'name': 'python-configuration-management',
    'version': '2.0.5',
    'description': 'A merge conflict-less solution to committing an encrypted configuration to the repo with secrets and non-secrets side-by-side.',
    'long_description': '# Quick start\n\nThis package features an opinionated, python configuration management system, focused on combining both secret\nand non-secret keys in the same configuration file. The values for secret keys are encrypted and can\nbe committed to the repo, but since each key is separated on a line-by-line basis, merge conflicts\nshouldn\'t cause much trouble.\n\n## Install\n\n`pip install python-configuration-management`\n\n## cli\n\n### Generate a key\n\nIn a terminal, enter:\n\n```bash\npycm generate-key\n```\n\nFollow the instructions printed to the console. For example, if you\'re setting up a production configuration,\nmake a file called `.env-production` in the root of your project. Inside of it, save the key generated\nabove to a variable called `ENC_KEY`.\n\n### Upsert a secret\n\nTo insert or update a secret, enter:\n\n```bash\npycm upsert --environment <your environment>\n```\n\nAnd follow the prompts.\n\n### Insert a non-secret\n\nSimply open the .yml file for the generated stage (the naming scheme is `config-<environment>.yaml`),\nand insert a row. It should look like this:\n\n```yaml\nUSERNAME: whatsup1994 # non-secret\nPASSWORD:\n  secret: true\n  value: gAAAAABf2_kxEgWXQzJ0SlRmDy6lbXe-d3dWD68W4aM26yiA0EO2_4pA5FhV96uMWCLwpt7N6Y32zXQq-gTJ3sREbh1GOvNh5Q==\n```\n\n### Manually editing the file\n\nYou can change the values of non-secrets by hand, as well as the keynames, but clearly you must\nnot change the value of secrets by hand, as they\'re encrypted. Changing the order of any of the\nkeys is perfectly fine.\n\n### Print secrets to the console\n\nTo show the decrypted values of all the secrets in the console, enter:\n\n```bash\npycm reveal --environment <your-environment>\n```\n\n### Re-encrypt a config file\n\nTo re-encrypt all secret values for a given environment\'s config file, pass\n\n```bash\npycm reencrypt --environment <your-environment> --new-key <your-new-key>\n```\n\nIf you do not provide a key, a new one will be generated for you.\n\n## Extras\n\nIn the root of your project, you can create a file called `config-required.json`.\n\nThe JSON object can be a list or a dictionary. This is useful for validating the presence of your\nkeys on start-up.\n\n# Using the config in your python code\n\nThere are two ways to use this library. You can either have a dotenv file with your `ENC_KEY`,\nor you can place the `ENC_KEY` in your environment variables. If you use a dotenv, make sure\nthe file follows this naming scheme: `.env-[environment]`.\n\nAs for accessing the config, if you don\'t mind a little magic, you can use `inject_config`.\n\n```python\n# settings.py\nfrom pycm import inject_config\n\n# development is the environment name\ninject_config("development", sys.modules[__name__], use_dotenv=True)\n```\n\nIf you want more verbosity, you can import the following function which will return\nthe config as a normalized dictionary that\'s flat and has all secrets decrypted.\n\n```python\n# settings.py\nfrom pycm import get_config\n\n# config = {"USERNAME": "helloworld", "PASSWORD": "im decrypted}\nconfig = get_config("development", use_dotenv=True)\n\nUSERNAME = config["USERNAME"]\n# ...\n```\n\n## Advanced usage\n\nAll file paths within the libary are relative to root by default. To change this\nbehaviour, set an environment variable called `PYCM_ROOT` which stores the relative\npath to the root of your project (where your `.env-[environment]` and `config-[environment].yml`\nfiles are stored).\n\n---\n\nThis project uses [poetry](https://python-poetry.org/) for dependency management\nand packaging.\n',
    'author': 'Alex Drozd',
    'author_email': 'alex@kicksaw.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/Kicksaw-Consulting/python-configuration-management',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
