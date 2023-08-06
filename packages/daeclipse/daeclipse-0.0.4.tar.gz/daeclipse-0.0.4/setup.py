# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['daeclipse', 'daeclipse.models']

package_data = \
{'': ['*']}

install_requires = \
['Pillow>=8.3.1,<9.0.0',
 'PyYAML>=5.4.1,<6.0.0',
 'beautifulsoup4>=4.9.3,<5.0.0',
 'browser-cookie3>=0.12.1,<0.13.0',
 'cli-ui>=0.14.1,<0.15.0',
 'pick>=1.0.0,<2.0.0',
 'requests>=2.26.0,<3.0.0',
 'typer>=0.3.2,<0.4.0']

setup_kwargs = {
    'name': 'daeclipse',
    'version': '0.0.4',
    'description': 'A Python library for DeviantArt Eclipse functionality',
    'long_description': '# dAEclipse\n`daeclipse` is a Python library for DeviantArt Eclipse functionality.\n\nThis repo also contains a handy CLI to expose and test `daeclipse` capabilities.\n\n```bash\npython3 cli.py --help\n```\n```\nUsage: cli.py [OPTIONS] COMMAND [ARGS]...\n\n  DeviantArt Eclipse CLI\n\nOptions:\n  --install-completion [bash|zsh|fish|powershell|pwsh]\n                                  Install completion for the specified shell.\n  --show-completion [bash|zsh|fish|powershell|pwsh]\n                                  Show completion for the specified shell, to\n                                  copy it or customize the installation.\n\n  --help                          Show this message and exit.\n\nCommands:\n  add-art-to-groups  Submit DeviantArt deviation to groups.\n  gif-preset         Generate an animated pixel icon gif based on a stored preset.\n  gif-random         Generate an animated pixel icon gif with randomized assets.\n```\n\n## Installation\n\n```bash\npython3 -m pip install daeclipse\n```\n\n## Usage\n\n```py\nimport daeclipse\n\n# Fetches a list of group names the user is a member of.\n# You will need to be logged into DeviantArt and have a chrome page open.\neclipse = daeclipse.Eclipse()\ngroups, has_more, next_offset, total = eclipse.get_groups("Pepper-Wood", 0)\nfor group in groups:\n    print(group.username)\n```\n\n## Caveats / Disclaimer\n\nDeviantArt\'s history as a website is storied. Prior to the release of Eclipse, there were two options with creating tooling around its UI:\n- The [Public DeviantArt API](https://www.deviantart.com/developers/). See [accompanying Python wrapper](https://pypi.org/project/deviantart/). The API is relatively easy to use - and utilizes OAuth2 for authentication - but its endpoints and functionality are sparce. It also was not updated for some time but now appears to be getting a handful of new endpoints based on the changelog.\n- The internal [DeviantArt Interactive Fragment Interface (DiFi)](https://github.com/danopia/deviantart-difi/wiki). DiFi has a wide range of functionality but is volatile/unreliable and difficult to use - especially compared to modern APIs.\n\nOn October 2019, DeviantArt announced [DeviantArt Eclipse](https://www.deviantart.com/team/journal/DeviantArt-Eclipse-is-Here-814629875), a new UI (mostly) built in React. There are still a handful of pages on the website that expose the old website (i.e. https://www.deviantart.com/groups/) where functionality hasn\'t been completely ported. But with the new React UI brought along a third option for tooling:\n- The internal **DeviantArt NAPI**, currently undocumented. The structure of its endpoints resembles RESTful practices, and authentication is done through scraping a CSRF token on the website or using a user\'s stored `.deviantart.com` cookies.\n\nThe implementation in this library relies on the DeviantArt NAPI. As such, functionality may break without warning depending on whether the internal DeviantArt team makes changes to these endpoints.\n\n## Contributing\n\nPull requests are welcome. For major changes, please open an issue first to discuss what you would like to change. Please make sure to update tests as appropriate.\n\n## License\n[MIT](https://github.com/Pepper-Wood/daeclipse/blob/main/LICENSE)\n',
    'author': 'Kathryn DiPippo',
    'author_email': 'dipippo.k@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://kathryndipippo.com/daeclipse/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6.2,<4.0.0',
}


setup(**setup_kwargs)
