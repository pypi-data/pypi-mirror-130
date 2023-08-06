# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['djaxei', 'djaxei.migrations', 'djaxei.providers']

package_data = \
{'': ['*'], 'djaxei': ['templates/djaxei/*']}

install_requires = \
['django>=1.11,<4']

extras_require = \
{'openpyxl': ['openpyxl<4'],
 'xlsxwriter': ['xlsxwriter>=1.2.8'],
 'xlwt': ['xlwt>=1.2.0']}

setup_kwargs = {
    'name': 'djaxei',
    'version': '0.7.0',
    'description': 'A django admin extension for importing exporting records from/to xls/ods',
    'long_description': '# A django admin extension for importing exporting records from/to xls/ods\n\nA Python library project using:\n* pytest\n* flake8\n* tox\n* bumpversion\n* isort\n\n* Free software: MIT license\n* Documentation: __TBD__\n\n\n# Features\n\n- Requires Python >=3.6.1\n- Currently work only with xlsxwriter\n\n- Could help if use [direnv](https://direnv.net/) in dev environment\n\n* TODO\n\n# Dev setup\n\n1. install direnv\n2. install pyenv\n3. clone project: `git clone https://github.com/GigiusB/djaxei.git`\n4. `cd djaxei`\n5. ```pyenv install `cat .python-version` ```\n6. `pip install -U poetry` # this should install poetry in your pyenv python\n7. `cp .env.example .env`\n8. `cp .envrc.example .envrc`\n9. `direnv allow`\n10. ```poetry env use `pyenv which python` ```\n11. `cd .. ; cd -`  # see if it loads the env\n12. poetry install\n13. pytest\n\nCredits\n-------\n\n',
    'author': 'Giovanni Bronzini',
    'author_email': 'g.bronzini@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/GigiusB/djaxei.git',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.6.1,<4',
}


setup(**setup_kwargs)
