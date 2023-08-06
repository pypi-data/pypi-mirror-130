# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['cdn_proxy',
 'cdn_proxy.cloudflare',
 'cdn_proxy.cloudfront',
 'cdn_proxy.cloudfront.req_lambda']

package_data = \
{'': ['*'],
 'cdn_proxy.cloudfront.req_lambda': ['build/*',
                                     'build/static/css/*',
                                     'build/static/js/*',
                                     'public/*',
                                     'src/*']}

install_requires = \
['boto3>=1.18.25,<2.0.0',
 'botocore>=1.21.25,<2.0.0',
 'cloudflare>=2.8.15,<3.0.0',
 'requests>=2.26.0,<3.0.0',
 'typer>=0.3.2,<0.4.0',
 'urllib3>=1.26.7,<2.0.0']

entry_points = \
{'console_scripts': ['cdn-proxy = cdn_proxy.__main__:main']}

setup_kwargs = {
    'name': 'cdn-proxy',
    'version': '0.1.3',
    'description': 'Take advantage of IP whitelisting of shared CDNs.',
    'long_description': None,
    'author': 'Ryan Gerstenkorn',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6.2,<4.0.0',
}


setup(**setup_kwargs)
