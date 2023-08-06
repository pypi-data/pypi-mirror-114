# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['sloth_ci_ext_logs']
install_requires = \
['sloth-ci>=2.2.0,<3.0.0']

setup_kwargs = {
    'name': 'sloth-ci-ext-logs',
    'version': '1.1.3',
    'description': 'File logging for Sloth CI',
    'long_description': "# File Logging for Sloth CI\n\nYou can customize your logging in a number of ways: set the output dir and filename, set log level and format, toggle and configure log rotation.\n\n\n## Installation\n\n    $ pip install sloth-ci-ext-logs\n\n\n## Usage\n\n    extensions:\n        logs:\n            # Use the module sloth_ci_ext_logs.\n            module: logs\n\n            # Set the log path. Default is the current dir.\n            path: debug_logs\n\n            # Log filename. If not given, the app's listen point is used.\n            filename: test_debug.log\n\n            # Log level (number or valid Python logging level name).\n            level: DEBUG\n\n            # Log format (refer to the https://docs.python.org/3/library/logging.html#logrecord-attributes).\n            # By default, this format is used: \n            # format: '%(asctime)s | %(name)30s | %(levelname)10s | %(message)s'\n\n            # Make logs rotating. Default is false.\n            # rotating: true\n\n            # If rotating, maximum size of a log file in bytes.\n            # max_bytes: 500\n\n            # If rotating, maximum number or log files to keep.\n            # backup_count: 10\n\n",
    'author': 'Constantine Molchanov',
    'author_email': 'moigagoo@live.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'py_modules': modules,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
