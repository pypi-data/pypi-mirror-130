# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['aria2_rpc_client']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'aria2-rpc-client',
    'version': '0.4.5',
    'description': 'Aria2 RPC Client',
    'long_description': '# How to using this package\n\n## Installing\n\n```\npip install aria2_rpc_client\n```\n\n## Using\n\n```python\nfrom aria2_rpc_client import DefaultClient\nfrom aria2_rpc_client import DefaultConnection\nfrom aria2_rpc_client import FileDownloadOptions\n\n# Make connection, enter aria2 rpc server information\nconnection = DefaultConnection("localhost", "6800", "top_secret_key")\n\n# Make client\nclient = DefaultClient(connection)\n\n# Download options\noptions = FileDownloadOptions()\noptions.set_filename("changed.mkv")\noptions.set_dir("/home/user/downloads")\noptions.add_header("token", "da78d676ds6a86dsa6d8sa6d8")\n\n# Download start & set options\nresult = client.add_uri(["https://jell.yfish.us/media/jellyfish-15-mbps-hd-h264.mkv"], options)\n\n# Get defined GID number from aria2\nprint(result)\n# 6be2fb970af88d07\n\n# Set download pause\npause_download = client.pause(result)\nprint(pause_download)\n# 6be2fb970af88d07\n```\n',
    'author': 'Özkan ŞEN',
    'author_email': 'ozkansen@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/ozkansen/aria2_rpc_client',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
