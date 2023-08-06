# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['shhell']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'shhell',
    'version': '0.0.0',
    'description': 'Subprocess replacement with fancy API to build commands, typing and, hopefully, autocompletion  support ✨',
    'long_description': '# Shhell\n\nSubprocess replacement ~~done right~~ with fancy API to build commands, autocompletion and typing support ✨\n\nI was not satisfied with API of subprocess/sh/plumbum, so I decided to at least define how the perfect API should look like for me. \n\nComing soon, sometime or just never.\n\nHow I want API to look like:\n```py\nimport shhell\n\nshhell.sh(c=shhell.curl(*\'fsSL\', \'https://raw.github.com/ohmyzsh/ohmyzsh/master/tools/install.sh\')).run()\n```\nwhich will be translated to:\n```shell\nsh -c "$(curl -fsSL \'https://raw.github.com/ohmyzsh/ohmyzsh/master/tools/install.sh\')"\n```\n\n`shhell.<cmd>(...)` will produce an instance of special class, which can invoke and get result from command both synchronously and asynchronously, allowing flexibility:  \n```py\nimport asyncio\nimport shhell\n\nOUTPUT_FILE = "example.mp4"\n\nasync def download():\n    await shhell.curl(\n        *\'fsSL\',\n        "https://file-examples-com.github.io/uploads/2017/04/file_example_MP4_1920_18MG.mp4",\n        output=OUTPUT_FILE\n    )\n\nasync def print_file_size():\n    while True:\n        await shhell.echo(f\'\\t{await shhell.stat(OUTPUT_FILE, printf="%s")}\')\n        await asyncio.sleep(0.1)\n\nasyncio.run(\n    asyncio.wait(\n        [\n            asyncio.create_task(download()), \n            asyncio.create_task(print_file_size())\n        ],\n        return_when=asyncio.FIRST_COMPLETED\n    )\n)\n```\n\n## Pipes, redirects, subshells?\nI like how plumbum deos this, i.e. using python magic methods allowing `|`, `>` support. In fact, if I\'m going to write this library, I\'m going to steal a lot of ideas from plumbum, changing little things that I don\'t like.   \n\n## How autocompletion would even work?\nCode generation, of course! However, it\'s not going to be easy, if achievable at all...\n\nOne of the options is generating signatures upon package build for executables available in PATH (expected args, types, docs) from -h/--help/man output for the command for linux/macOS.\nThis option is only viable on CI/CD stages, however. \n\nThere should be api available for users to generate code structures for their own non-standard executables.\n\n    Note: all the generated code will serve only cosmetic purpose, whether a signature was generated for a specific executable or not, the runtime result should always remain the same.\n\nSo `shhell/executables/cowsay.py` would look like this:\n```py\nfrom typing import Any, Literal\nfrom shhell.command import Command\nfrom shhell.executable import Executable\n\n@Executable.from_dummy\ndef cowsay(\n    *args: Literal["b", "d", "g", "p", "s", "t", "w", "y", "l", "n"],\n    # __message this is positional only optional argument\n    __message: str = ...,\n    # these arguments are keyword only (e=\'??\' will be converted to -e \'??\')\n    e: Any = "eyes",\n    f: Any = "cowfile",\n    T: Any = "tongue",\n    W: Any = "wrapcolumn",\n) -> Command:\n    """\n    cow{say,think} version 3.03, (c) 1999 Tony Monroe\n    Usage: cowsay [-bdgpstwy] [-h] [-e eyes] [-f cowfile]\n          [-l] [-n] [-T tongue] [-W wrapcolumn] [message]\n    """\n...\n```\n_However, I think it\'s better to have a separate file for each executable, and just add imports for them_\n',
    'author': 'Bobronium',
    'author_email': 'appkiller16@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
