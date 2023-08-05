# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ocpp_asgi']

package_data = \
{'': ['*']}

install_requires = \
['ocpp>=0.8.3,<0.9.0']

setup_kwargs = {
    'name': 'ocpp-asgi',
    'version': '0.2.0',
    'description': 'ocpp-asgi provides ASGI compliant interface for implementing event-driven server-side support for OCPP protocol with Python',
    'long_description': '# OCPP-ASGI\n\nocpp-asgi provides **ASGI compliant** interface for implementing **event-driven** **server-side** support for OCPP protocol with Python. It depends on and extends [mobilityhouse/ocpp](https://github.com/mobilityhouse/ocpp). \n\nThe key features are:\n* ASGI compliant interface supporting both WebSocket and HTTP protocols.\n* Event-driven and "stateless" approach for implementing action handlers for OCPP messages. \n* Highly-scalable and supports serverless (e.g. AWS Lambda) with compatible ASGI server.\n* Requires small and straightforward changes from ocpp to action handlers (but is not backwards compatible).\n\nDisclaimer! This library is still in alpha state. It has some rough edges.\n\n# Getting started\n\n## Installation\n\n```\npip install ocpp-asgi\n```\n\nAlso ASGI server is required e.g. [uvicorn](https://www.uvicorn.org) or [mangum](https://www.uvicorn.org) when deployed to AWS Lambda with API Gateway.\n```\npip install uvicorn\n```\n\n## Run the examples\n\nThere are two kind of examples how to implement central system with ocpp-asgi: standalone and serverless. Both examples use same ocpp action handlers (routers).\n\n### Running standalone example\n\nRun the following commands e.g. in different terminal windows (or run the files within IDE).\n\nStart Central System:\n```\npython ./examples/central_system/standalone/central_system.py\n```\n\nStart Charging Station:\n```\npython ./examples/charging_station.py\n```\n\n### Running serverless example\n\nRun the following commands in different terminal windows (or run the files within IDE).\n\nStart Central System HTTP backend:\n```\npython ./examples/central_system/serverless/central_system_http.py\n```\n\nStart Central System WebSocket proxy:\n```\npython ./examples/central_system/serverless/central_system_proxy.py\n```\n\nStart Charging Station:\n```\npython ./examples/charging_station.py\n```',
    'author': 'Ville Kärkkäinen',
    'author_email': 'ville.karkkainen@outlook.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/villekr/ocpp-asgi',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
