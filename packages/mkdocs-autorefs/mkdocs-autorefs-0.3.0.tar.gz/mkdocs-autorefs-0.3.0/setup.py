# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['mkdocs_autorefs']

package_data = \
{'': ['*']}

install_requires = \
['Markdown>=3.3,<4.0', 'mkdocs>=1.1,<2.0']

entry_points = \
{'mkdocs.plugins': ['autorefs = mkdocs_autorefs.plugin:AutorefsPlugin']}

setup_kwargs = {
    'name': 'mkdocs-autorefs',
    'version': '0.3.0',
    'description': 'Automatically link across pages in MkDocs.',
    'long_description': '# mkdocs-autorefs\n\n[![ci](https://github.com/mkdocstrings/autorefs/workflows/ci/badge.svg)](https://github.com/mkdocstrings/autorefs/actions?query=workflow%3Aci)\n[![pypi version](https://img.shields.io/pypi/v/mkdocs-autorefs.svg)](https://pypi.org/project/mkdocs-autorefs/)\n[![gitter](https://badges.gitter.im/join%20chat.svg)](https://gitter.im/mkdocstrings/community)\n\nAutomatically link across pages in MkDocs.\n\n## Installation\n\nWith `pip`:\n```bash\npython3 -m pip install mkdocs-autorefs\n```\n\n## Usage\n\n```yaml\n# mkdocs.yml\nplugins:\n  - search\n  - autorefs\n```\n\nIn one of your Markdown files (e.g. `doc1.md`) create some headings:\n\n```markdown\n## Hello, world!\n\n## Another heading\n\nLink to [Hello, World!](#hello-world) on the same page.\n```\n\nThis is a [*normal* link to an anchor](https://www.mkdocs.org/user-guide/writing-your-docs/#linking-to-pages). MkDocs generates anchors for each heading, and they can always be used to link to something, either within the same page (as shown here) or by specifying the path of the other page.\n\nBut with this plugin, you can **link to a heading from any other page** on the site *without* needing to know the path of either of the pages, just the heading title itself.  \nLet\'s create another Markdown page to try this, `subdir/doc2.md`:\n\n```markdown\nWe can [link to that heading][hello-world] from another page too.\n\nThis works the same as [a normal link to that heading](../doc1.md#hello-world).\n```\n\nLinking to a heading without needing to know the destination page can be useful if specifying that path is cumbersome, e.g. when the pages have deeply nested paths, are far apart, or are moved around frequently. And the issue is somewhat exacerbated by the fact that [MkDocs supports only *relative* links between pages](https://github.com/mkdocs/mkdocs/issues/1592).\n\nNote that this plugin\'s behavior is undefined when trying to link to a heading title that appears several times throughout the site. Currently it arbitrarily chooses one of the pages.\n\n## Requirements\n\n`mkdocs-autorefs` requires Python 3.6 or above.\n\n<details>\n<summary>To install Python 3.6, I recommend using <a href="https://github.com/pyenv/pyenv"><code>pyenv</code></a>.</summary>\n\n```bash\n# install pyenv\ngit clone https://github.com/pyenv/pyenv ~/.pyenv\n\n# setup pyenv (you should also put these three lines in .bashrc or similar)\nexport PATH="${HOME}/.pyenv/bin:${PATH}"\nexport PYENV_ROOT="${HOME}/.pyenv"\neval "$(pyenv init -)"\n\n# install Python 3.6\npyenv install 3.6.12\n\n# make it available globally\npyenv global system 3.6.12\n```\n</details>\n',
    'author': 'Oleh Prypin',
    'author_email': 'oleh@pryp.in',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/mkdocstrings/autorefs',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
