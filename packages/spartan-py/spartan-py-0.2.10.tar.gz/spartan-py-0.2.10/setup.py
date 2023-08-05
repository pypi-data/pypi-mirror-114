# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['spartan']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'spartan-py',
    'version': '0.2.10',
    'description': 'Library for spartan protocol',
    'long_description': '# spartan-py\n\nBasic spartan protocol implementation as a python library.\n\n```python\nimport spartan\n\nres = spartan.get("spartan://mozz.us/echo", "hi")\nwhile True:\n    buf = res.read()\n    if not buf:\n        break\n    sys.stdout.buffer.write(buf)\nres.close()\n```\n\nTry it in the REPL:\n```python\n>>> import spartan\n>>> req = spartan.Request("spartan.mozz.us")\n>>> req\nRequest(host=\'spartan.mozz.us\', port=300, path=\'/\') data-length=0\n>>> print(req)\n\'spartan.mozz.us / 0\'\n>>> res = req.send()\n>>> res\n2 text/gemini\n>>> res.read()\n[...]\n>>> res.close()\n```\n\n## install\n\n```\npip3 install spartan-py\n```\n\n## API\n\n- `Request(host: str, port: int = 300, path: str = "/", data: str = "")`\n  - `send() -> Response` - send the request\n  - `__repr__()`\n  - `__str__()`\n- `Response(socket)`\n  - `read()`\n  - `close()` - close the socket\n  - `.status` - status code\n  - `.meta` - meta string for the status\n  - `.file` - socket file\n  - `.request` - the Request object for this response\n  - `__repr__()`\n  - `__str__()`\n- `Status` - statuses\n  - `success = 2`\n  - `redirect = 3`\n  - `client_error = 4`\n  - `server_error = 5`\n- `get(url: str, data: str = "") -> Response` - if the query string part in the URL exists, data will be ignored.\n\n## TODO\n- [ ] invalid url handling\n- [ ] util functions like parsing meta and getting status type\n- [ ] basic CLI usage\n- [ ] async methods\n',
    'author': 'Hedy Li',
    'author_email': 'hedy@tilde.cafe',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://sr.ht/~hedy/spartan-py',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
