# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['nautilus_librarian',
 'nautilus_librarian.mods',
 'nautilus_librarian.mods.dvc',
 'nautilus_librarian.mods.dvc.domain',
 'nautilus_librarian.mods.dvc.typer',
 'nautilus_librarian.mods.git',
 'nautilus_librarian.mods.git.domain',
 'nautilus_librarian.mods.git.typer',
 'nautilus_librarian.mods.gpg',
 'nautilus_librarian.mods.gpg.domain',
 'nautilus_librarian.mods.gpg.typer',
 'nautilus_librarian.mods.libvips',
 'nautilus_librarian.mods.libvips.domain',
 'nautilus_librarian.mods.libvips.typer',
 'nautilus_librarian.mods.namecodes',
 'nautilus_librarian.mods.namecodes.domain',
 'nautilus_librarian.mods.namecodes.typer',
 'nautilus_librarian.typer']

package_data = \
{'': ['*']}

install_requires = \
['GitPython>=3.1.24',
 'PyGithub>=1.55',
 'dvc[azure]>=2.8.3,<3.0.0',
 'mypy>=0.910,<0.911',
 'pyvips>=2.1.16',
 'typer[all]>=0.4.0,<0.5.0']

entry_points = \
{'console_scripts': ['nautilus-librarian = nautilus_librarian.main:app']}

setup_kwargs = {
    'name': 'nautilus-librarian',
    'version': '0.2.0',
    'description': 'A Python Console application to handle media libraries like Git and DVC',
    'long_description': '# Nautilus Librarian\n\n[![CodeQL](https://github.com/Nautilus-Cyberneering/librarian/actions/workflows/codeql-analysis.yml/badge.svg)](https://github.com/Nautilus-Cyberneering/librarian/actions/workflows/codeql-analysis.yml)\n[![Deploy Documentation](https://github.com/Nautilus-Cyberneering/librarian/actions/workflows/deploy-documentation.yml/badge.svg)](https://github.com/Nautilus-Cyberneering/librarian/actions/workflows/deploy-documentation.yml)\n[![Lint Code Base](https://github.com/Nautilus-Cyberneering/librarian/actions/workflows/mega-linter.yml/badge.svg)](https://github.com/Nautilus-Cyberneering/librarian/actions/workflows/mega-linter.yml)\n[![Publish Docker image](https://github.com/Nautilus-Cyberneering/librarian/actions/workflows/publish-docker-image.yml/badge.svg)](https://github.com/Nautilus-Cyberneering/librarian/actions/workflows/publish-docker-image.yml)\n[![Publish GitHub Release](https://github.com/Nautilus-Cyberneering/librarian/actions/workflows/publish-github-release.yml/badge.svg)](https://github.com/Nautilus-Cyberneering/librarian/actions/workflows/publish-github-release.yml)\n[![Publish package to PyPI](https://github.com/Nautilus-Cyberneering/librarian/actions/workflows/publish-pypi-package.yml/badge.svg)](https://github.com/Nautilus-Cyberneering/librarian/actions/workflows/publish-pypi-package.yml)\n[![Test](https://github.com/Nautilus-Cyberneering/librarian/actions/workflows/test.yml/badge.svg)](https://github.com/Nautilus-Cyberneering/librarian/actions/workflows/test.yml)\n\nA Python Console application to handle media libraries with [Git](https://git-scm.com/) and [Dvc](https://github.com/iterative/dvc).\n\nDocumentation: [https://nautilus-cyberneering.github.io/librarian/](https://nautilus-cyberneering.github.io/librarian/)\n\n## Install\n\nRequirements:\n\n- Libvips\n- Python 3.9\n\nInstall Python Package:\n\n```shell\npip install nautilus-librarian\n```\n\nPlease for a complete installation and development guide read the [documentation](https://nautilus-cyberneering.github.io/librarian/).\n',
    'author': 'Jose Celano',
    'author_email': 'jose@nautilus-cyberneering.de',
    'maintainer': 'Jose Celano',
    'maintainer_email': 'jose@nautilus-cyberneering.de',
    'url': 'https://github.com/Nautilus-Cyberneering/librarian',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
