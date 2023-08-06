# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['late_bound_arguments']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'late-bound-arguments',
    'version': '0.1.2',
    'description': 'Allows evaluating default arguments at function-call time',
    'long_description': '# Late-Bound Arguments\n\nThis package tries to emulate the behaviour of syntax proposed in [PEP 671](https://www.python.org/dev/peps/pep-0671/) via a decorator.\n\n## Usage\nMention the names of the arguments which are to be late-bound in the arguments of the `delay` decorator, and their default values as strings in the function signature.\n\nMutable default arguments:\n```python\nfrom late_bound_arguments import delay\n\n@delay("my_list")\ndef foo(my_list="[]"):\n    my_list.append(1)\n    return my_list\n\nprint(foo()) # [1]\nprint(foo()) # [1]\nprint(foo([1, 2, 3])) # [1, 2, 3, 1]\n```\n\nReferencing previous arguments:\n```python\nfrom late_bound_arguments import delay\n\n@delay("my_list", "n")\ndef foo(my_list="[1, 2]", n: int = "len(my_list)"):\n    return my_list, n\n\n\nprint(foo()) # ([1, 2], 2)\nprint(foo([1, 2, 3])) # ([1, 2, 3], 3)\n```\nAdditionally, the function signature is not overwritten, so `help(foo)` will provide the original signature retaining the default values.\n\n\n## Reasoning\n\nMutable defaults are often tricky to work with, and may not do what one might naively expect.\n\nFor example, consider the following function:\n```python\ndef foo(my_list=[]):\n    my_list.append(1)\n    return my_list\n\n    \nprint(foo())\nprint(foo())\n```\n\nOne might expect that this prints `[1]` twice, but it doesn\'t. Instead, it prints `[1]` and `[1, 1]`. \nA new list object is *not* created every time `foo` is called without providing the `b` argument: the list is only created once - when the function is defined - and the same list object is used for every call. As a result, if it is mutated in any call, the change is reflected in subsequent calls.\n\n\nA common workaround for this is using `None` as a placeholder for the default value, and replacing it inside the function body.\n```python\ndef foo(my_list=None):\n    if my_list is None: \n        my_list = []\n    ...\n```\nIn case `None` is a valid value for the argument, a sentinel object is created beforehand and used as the default instead.\n```python\n_SENTINEL = object()\ndef foo(my_list=_SENTINEL):\n    if my_list is _SENTINEL: \n        my_list = []\n    ...\n```\nHowever, this solution, apart from being unnecessarily verbose, has an additional drawback: `help(foo)` in a REPL will fail to inform of the default values, and one would have to go through the source code to find the true signature.',
    'author': 'Shakya Majumdar',
    'author_email': 'shakyamajumdar1@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/ShakyaMajumdar/late_bound_arguments',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
