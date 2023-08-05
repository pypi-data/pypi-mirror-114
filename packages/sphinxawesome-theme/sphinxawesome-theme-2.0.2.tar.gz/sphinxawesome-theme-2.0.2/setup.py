# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['sphinxawesome_theme']

package_data = \
{'': ['*'], 'sphinxawesome_theme': ['static/*']}

install_requires = \
['beautifulsoup4>=4.9.1,<5.0.0',
 'sphinx>4',
 'sphinxawesome-sampdirective>=1.0.3,<2.0.0']

extras_require = \
{':python_version < "3.8"': ['importlib_metadata>=1.6.1,<3.0.0']}

entry_points = \
{'sphinx.html_themes': ['sphinxawesome_theme = sphinxawesome_theme']}

setup_kwargs = {
    'name': 'sphinxawesome-theme',
    'version': '2.0.2',
    'description': 'An awesome theme for the Sphinx documentation generator',
    'long_description': '# Sphinx awesome theme\n\n\n![GitHub](https://img.shields.io/github/license/kai687/sphinxawesome-theme?color=blue&style=for-the-badge)\n![PyPI](https://img.shields.io/pypi/v/sphinxawesome-theme?color=eb5&style=for-the-badge&logo=pypi)\n![Netlify](https://img.shields.io/netlify/e6d20a5c-b49e-4ebc-80f6-59fde8f24e22?logo=netlify&style=for-the-badge)\n![GitHub Workflow Status](https://img.shields.io/github/workflow/status/kai687/sphinxawesome-theme/Lint?label=Lint&logo=Github&style=for-the-badge)\n\n<!-- readme-start -->\n\nThis is an awesome theme and a set of extensions for the\n[Sphinx](https://www.sphinx-doc.org/en/master/) documentation generator. Using this\ntheme and extension, you can change the look of your documentation website and add a\nnumber of useful improvements. See the theme in action at\n[sphinxawesome.xyz](https://sphinxawesome.xyz).\n\n## Getting started\n\nYou can install the awesome theme from the Python package index and modify the Sphinx\nconfiguration file `conf.py`.\n\nTo get started using this theme, follow these steps:\n\n1. Install the theme as a Python package:\n\n   ```console\n   pip install sphinxawesome-theme\n   ```\n\n   See [How to install the theme](https://sphinxawesome.xyz/how-to/install/) for more information.\n\n1. Add the `html_theme` configuration option to the Sphinx configuration file\n   `conf.py`:\n\n   ```python\n   html_theme = "sphinxawesome_theme"\n   ```\n\n   See [How to use the theme](https://sphinxawesome.xyz/how-to/use/) for more information.\n\n## Features\n\nThis theme is designed with readability and usability in mind. The theme includes\nseveral extensions that enhance the usability:\n\n- **Awesome code blocks**\n\n    - Code blocks have a header section, displaying the optional caption, as well as the\n      programming language used for syntax highlighting\n    - The code block headers contain a **Copy** button, allowing you to copy code\n      snippets to the clipboard.\n    - The theme adds two new options to Sphinx\'s `code-block` directive:\n      `emphasize-added` and `emphasize-removed`, for highlighting changes within other\n      highlighted code.\n\n- **Awesome new directive for highlighting placeholder variables**. The theme supports a\n  new directive `samp`, which is the equivalent of the built-in\n  `:samp:` interpreted text role. This allows you to highlight placeholder variables\n  in code blocks.\n\n- **Awesome user experience improvements**. These small features make the theme more\n  usable:\n\n    - Better keyboard navigation:\n\n      <!-- vale 18F.Clarity = NO -->\n      - Use the `Tab` key to navigate through all sections on the page\n      - Use the *Skip to Content* link to bypass the navigation links\n      - Use the `/` key (forward Slash) to start a search\n      <!-- vale 18F.Clarity = YES -->\n\n    - Better "permalink" mechanism:\n\n      - Hovering over an element with a permalink reveals a *Link* icon\n      - Selecting the *Link* icon copies the link to the clipboard\n      - Notes, warnings and other admonitions have permalinks by default\n\n    - Collapsible elements:\n\n      - Nested navigation links---all pages are reachable from all other pages\n      - Code definitions---code object definitions (functions, classes, modules, etc.), for example, obtained via the `sphinx.ext.autodoc` extension.\n',
    'author': 'Kai Welke',
    'author_email': 'kai687@pm.me',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/kai687/sphinxawesome-theme',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.6.2,<4.0.0',
}


setup(**setup_kwargs)
