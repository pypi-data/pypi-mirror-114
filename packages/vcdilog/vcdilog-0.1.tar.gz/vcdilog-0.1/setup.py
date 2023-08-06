# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['vcdilog']

package_data = \
{'': ['*']}

install_requires = \
['logging_tree', 'python-json-logger', 'pyyaml']

setup_kwargs = {
    'name': 'vcdilog',
    'version': '0.1',
    'description': 'best practice low-config python logging',
    'long_description': '# vcdilog: logging as easy as print statements\n\nYou almost certainly should be using log statement instead of messy print statements. `vcdilog` makes this easy.\n\n\n## Install\n\nYou can install `vcdilog` using pip:\n\n```\n$ pip install vcdilog\n```\n\nIf using poetry, simply add this line to your `pyproject.toml` file.\n\n```\nvcdilog = "*"\n```\n\n## Philosophy\n\nThe built in python logging library is highly customizable, but hard to visualize and understand. `vcdilog` doesn\'t try to replace what is in the standard library, but streamlines it with sensible defaults.\n\n\n## Basic, instead-of-print-statements usage\n\nAll you need is two lines of setup: One import, and one line to add a handler for stdout/stderr output.\n\n```\nfrom vcdilog import log\nlog.add_std_handler()\n\nlog.info(\'hello world\')  # .info, .warning, .debug, etc\n```\n\n\n## More flexible usage\n\nYou can create a log object:\n\nfrom vcdilog import Logger\n\nlog = Logger()\n\nCrucially, you don’t need to give the logger a name, it will figure out the current module name automatically and use that. This same method is used by the print-statements example above - they\'ll be logged to an appropriately-named logger automatically, based on the module they\'re in.\n\nYou can set a log level with:\n\n```\nlog.set_level(level="DEBUG")\n```\n\nDEBUG means all logged messages will actually get logged. When you add a handler with e.g. `add_std_handler`, the handler will be assigned the `DEBUG` level by default, and so will the associated logger.\n\nFor production usage, a lower level should ordinarily be set to avoid overly verbose logging.\n\n\n## Other handlers\n\nSo far three handlers are supported.\n\n```\nx.add_std_handler()\nx.add_null_handler()\nx.add_json_handler()\n```\n\nAs per the above, the standard output handler logs to the console. It uses some customization log errors to stderr and normal messages to stdout, just like `print()` does, which means you can use logging calls instead of print statements.\n\nThe null handler should be used in libraries - it’s best practice when publishing a library to create a logger but add only a null handler and no others to that users of the library don’t get unwanted log messages (if they want to see them, they’ll add their own handlers).\n\nThen there’s the json handler. That logs json-formatted log items to a file.\n\nFor instance, the following:\n\n```\nlog.info("classic message", extra={"special": "value", "run": 12})\n```\n\nWill result in:\n\n```\n{"message": "classic message", "special": "value", "run": 12}\n```\n\nIn the log file (log.json by default)\n\n## Basic prefect support\n\nGetting a prefect logger is as easy as:\n\n```\nprefect_logger = vcdilog.get_prefect_logger()\n```\n\nand you can do...\n\n```\nvcdilog.set_prefect_extra_loggers([\'boto3\', \'whatever\'])\n```\n\nto have those loggers inherit the prefect logging config.\n\nMore prefect support is on the way!',
    'author': 'Robert Lechte',
    'author_email': 'robert.lechte@dpc.vic.gov.au',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
