# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['mytoyota']

package_data = \
{'': ['*']}

install_requires = \
['httpx>=0.17.1,<0.18.0',
 'langcodes>=3.1.0,<4.0.0',
 'pendulum>=2.1.2,<3.0.0',
 'uuid>=1.30,<2.0']

setup_kwargs = {
    'name': 'mytoyota',
    'version': '0.3.0',
    'description': 'Python client for Toyota Connected Services.',
    'long_description': '# Toyota Connected Services Python module\n\n### [!] **This is still in beta**\n\n## Description\n\nPython 3 package to communicate with Toyota Connected Services.\n\n## Installation\n\nThis package can be installed through `pip`.\n\n```text\npip install mytoyota\n```\n\n## Usage\n\n```python\nimport asyncio\nfrom mytoyota.client import MyT\n\nusername = "jane@doe.com"\npassword = "MyPassword"\nlocale = "da-dk"\n\nclient = MyT(username=username, password=password, locale=locale, region="europe")\n\n\nasync def get_information():\n    print("Logging in...")\n    await client.login()\n\n    print("Retrieving cars...")\n    # Returns information about the cars registered to your account\n    cars = await client.get_vehicles()\n\n    print(await client.gather_all_information_json())\n\n    statistics = await client.get_driving_statistics_from_date_json(cars[0][\'vin\'])\n\n    print(statistics)\n\n    statistics = await client.get_driving_statistics_from_week_json(cars[0][\'vin\'])\n\n    print(statistics)\n\n    statistics = await client.get_driving_statistics_from_month_json(cars[0][\'vin\'])\n\n    print(statistics)\n\nloop = asyncio.get_event_loop()\nloop.run_until_complete(get_information())\nloop.close()\n\n```\n\n## Docs\n\nComing soon...\n\n## Contributing\n\nThis python module uses poetry and pre-commit.\n\nTo start contributing, fork this repository and run `poetry install`. Then create a new branch. Before making a PR, please run pre-commit `poetry run pre-commit run --all-files` and make sure that all tests passes locally first.\n\n## Note\n\nAs I [@DurgNomis-drol](https://github.com/DurgNomis-drol) is not a professional programmer. I will be maintain it as best as I can. If someone is interested in helping with this, they are more the welcome to message me to be a collaborator on this project.\n\n## Credits\n\nA huge thanks go to [@calmjm](https://github.com/calmjm) for making [tojota](https://github.com/calmjm/tojota).\n',
    'author': 'Simon Grud Hansen',
    'author_email': 'simongrud@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/DurgNomis-drol/mytoyota',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
