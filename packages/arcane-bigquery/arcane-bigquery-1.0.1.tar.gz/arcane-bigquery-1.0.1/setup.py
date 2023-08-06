# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['arcane']

package_data = \
{'': ['*']}

install_requires = \
['google-cloud-bigquery>=2.16.1,<3.0.0']

setup_kwargs = {
    'name': 'arcane-bigquery',
    'version': '1.0.1',
    'description': 'Override google bigquery python client',
    'long_description': "# Arcane bigquery\n\nThis package is based on [google-cloud-bigquery](https://pypi.org/project/google-cloud-bigquery/).\n\n## Get Started\n\n```sh\npip install arcane-bigquery\n```\n\n## Example Usage\n\n```python\nfrom arcane import bigquery\nclient = bigquery.Client()\n\ndataset_ref = client.dataset('name')\ndataset = bigquery.Dataset(dataset_ref)\ndataset.location = 'US'\ndataset = client.create_dataset(dataset)\n```\n\nCreate clients with credentials:\n\n```python\nfrom arcane import bigquery\n\n# Import your configs\nfrom configure import Config\n\nclient = bigquery.Client.from_service_account_json(Config.KEY, project=Config.GCP_PROJECT)\n\n```\n",
    'author': 'Arcane',
    'author_email': 'product@arcane.run',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<3.10',
}


setup(**setup_kwargs)
