# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['callofduty']

package_data = \
{'': ['*']}

install_requires = \
['httpx>=0.18.2,<0.19.0']

setup_kwargs = {
    'name': 'callofduty.py',
    'version': '1.3.0',
    'description': 'CallofDuty.py is an asynchronous, object-oriented Python wrapper for the Call of Duty API.',
    'long_description': '<div align="center">\n\n![CallofDuty.py](https://i.imgur.com/HXy6Dkd.png)\n\n<a href="https://pypi.python.org/pypi/callofduty.py"><img src="https://img.shields.io/pypi/v/callofduty.py?label=Version&style=for-the-badge" /></a>\n<a href="https://pypi.python.org/pypi/callofduty.py"><img src="https://img.shields.io/pypi/dm/callofduty.py?style=for-the-badge" /></a>\n<a href="https://twitter.com/Mxtive"><img src="https://img.shields.io/twitter/follow/Mxtive?color=1da1f2&label=Twitter&style=for-the-badge" /></a>\n<a href="https://discord.gg/callofduty"><img src="https://img.shields.io/discord/136986169563938816?color=7289DA&label=Discord&style=for-the-badge" /></a>\n\n</div>\n\n# CallofDuty.py\n\nCallofDuty.py is an asynchronous, object-oriented Python wrapper for the Call of Duty API.\n\n## Features\n\n-   Asynchronous and Pythonic using `async` and `await`\n-   Type checks and editor completion using [Type Hints](https://www.python.org/dev/peps/pep-0484/)\n-   Object-oriented and predictable abstractions\n\n## Usage\n\nConstruct a new Call of Duty client, then use the various services on the client to access different parts of the Call of Duty API.\n\n### Installation\n\nCallofDuty.py requires Python 3.9 or greater. Once this requirement is met, simply install CallofDuty.py!\n\n```\npip install callofduty.py\n\n# or\n\npoetry add callofduty.py\n```\n\n### Example\n\nThe following is a complete example which demonstrates:\n\n-   Authenticating with the Call of Duty API\n-   Searching for a user\n-   Listing the first 3 search results\n-   Getting the Modern Warfare Multiplayer profile of the second result\n-   Displaying their basic statistics\n\n```py\nimport asyncio\n\nimport callofduty\nfrom callofduty import Mode, Platform, Title\n\n\nasync def main():\n    client = await callofduty.Login("YourEmail@email.com", "YourPassword")\n\n    results = await client.SearchPlayers(Platform.Activision, "Captain Price", limit=3)\n    for player in results:\n        print(f"{player.username} ({player.platform.name})")\n\n    me = results[1]\n    profile = await me.profile(Title.ModernWarfare, Mode.Multiplayer)\n\n    level = profile["level"]\n    kd = profile["lifetime"]["all"]["properties"]["kdRatio"]\n    wl = profile["lifetime"]["all"]["properties"]["wlRatio"]\n\n    print(f"\\n{me.username} ({me.platform.name})")\n    print(f"Level: {level}, K/D Ratio: {kd}, W/L Ratio: {wl}")\n\nasyncio.get_event_loop().run_until_complete(main())\n```\n\n## Releases\n\nCallofDuty.py follows [Semantic Versioning](https://semver.org/) for tagging releases of the project.\n\nChangelogs can be found on the [Releases](https://github.com/EthanC/CallofDuty.py/releases) page and follow the [Keep a Changelog](https://keepachangelog.com/) format.\n\n## Contributing\n\nThe goal is to cover the entirety of the Call of Duty API, so contributions are always welcome. The calling pattern is pretty well-established, so adding new methods is relatively straightforward. See [`CONTRIBUTING.md`](https://github.com/EthanC/CallofDuty.py/blob/master/.github/CONTRIBUTING.md) for details.\n\n## Thanks & Credits\n\n-   [Tustin](https://github.com/Tustin) - Call of Duty API Authorization Flow\n-   [Activision](https://www.activision.com/) - Call of Duty Logo & API Service\n',
    'author': 'EthanC',
    'author_email': 'EthanC@github.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/EthanC/CallofDuty.py',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
