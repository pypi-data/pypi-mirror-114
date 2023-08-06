# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['livemasjid']

package_data = \
{'': ['*']}

install_requires = \
['paho-mqtt>=1.5.1,<2.0.0',
 'requests>=2.26.0,<3.0.0',
 'websocket>=0.2.1,<0.3.0']

setup_kwargs = {
    'name': 'livemasjid',
    'version': '0.1.2',
    'description': 'This package provides a pythonic interface to subscribe to updates from Livemasjid as well as to get sthe current status of Livemasjid streams.',
    'long_description': '#Livemasjid\n\nThis package provides a pythonic interface to subscribe \nto updates from Livemasjid as well as to get the current\nstatus of Livemasjid streams.\n\n```python\nfrom livemasjid import Livemasjid\n\ndef my_callback(topic, message, status):\n    print(topic)\n    print(message)\n    print(status)\n\n\nif __name__ == "__main__":\n    lm = Livemasjid(subscriptions=[\'activestream\'])\n    lm.register_on_message_callback(my_callback)\n    lm.update_status()\n    status = lm.get_status()\n    lm.start()\n```',
    'author': 'Yusuff Lockhat',
    'author_email': '45769466+lockhaty@users.noreply.github.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
