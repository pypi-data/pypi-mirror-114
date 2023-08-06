# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['anyflow']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'anyflow',
    'version': '0.2.0',
    'description': 'a simplest common middleware framework for python.',
    'long_description': "# anyflow\n\na simplest common middleware framework for python.\n\n## HOW-TO-USE\n\n``` py\nfrom anyflow import Flow\n\nflow = Flow()\n\n@flow.use()\ndef middleware_1(ctx, next):\n    ctx.state['value'] = 1\n    # call the next middleware (middleware_2):\n    return next()\n\n@flow.use()\ndef middleware_2(ctx, next):\n    print(ctx.state['value'])\n    # next middleware does not exists, call nothing:\n    return next()\n\nflow.run()\n```\n",
    'author': 'Cologler',
    'author_email': 'skyoflw@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
