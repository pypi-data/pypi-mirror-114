# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pygitstat']

package_data = \
{'': ['*']}

install_requires = \
['Colr>=0.9.1,<0.10.0',
 'click-default-group>=1.2.2,<2.0.0',
 'click>=7.1.2,<8.0.0',
 'tqdm>=4.54.1,<5.0.0']

entry_points = \
{'console_scripts': ['gitstat = pygitstat.gitstat:cli']}

setup_kwargs = {
    'name': 'pygitstat',
    'version': '0.5.0',
    'description': 'Succinctly display information about git repositories.',
    'long_description': '# gitstat\n\n## About\n\n![(screenshot)](images/screenshots/screenshot.png?raw=true "Basic usage")\n\n```\nUsage: gitstat [OPTIONS] COMMAND [ARGS]...\n\n  Succinctly display information about git repositories.\n\n  Gitstat looks for unstaged changes, uncommitted changes,\n  untracked/unignored files, unpushed commits, and whether a pull from\n  upstream is required.\n\n  Gitstat can maintain a list of repos about which it will report. Use\n  "gitstat track" to add repo(s) to its list.\n\n  If no paths to git repos are specified on the command line, gitstat will\n  show information about the repos it is tracking.\n\n  Run "gitstat COMMAND --help" for help about a specific command.\n\nOptions:\n  --version  Show the version and exit.\n  --help     Show this message and exit.\n\nCommands:\n  check*      Check repo(s).\n  fetch       Fetch from origin.\n  ignore      Ignore repo(s).\n  is-tracked  Show whether one or more repos are tracked by gitstat.\n  pull        Pull from origin (if no local changes).\n  showclone   Show "git clone" commands needed to clone missing repos.\n  track       Track repo(s).\n  unignore    Un-ignore repo(s).\n  untrack     Untrack repo(s).\n```\n\nGitstat has been designed with being careful in mind.\nGitstat makes no changes to git repos, except for the \'fetch\' and \'pull\' commands. (`gitstat fetch` simply runs `git fetch`,\nand `gitstat pull` will pull from origin *only if* there are no local changes and a pull is required.)\n\n\n## Requirements\n\n* Python 3.6+\n* git\n\n\n## Installation\n\n    pip install --user -i https://test.pypi.org/simple/ gitstat\n\n\n## Quick start\n\nShow information about a repository:\n\n    gitstat ~/myproject\n\nNote that this is the same as:\n\n    gitstat check ~/myproject\n\n("check" is the default command.)\n\nYou use `~/myproject` all the time; let\'s tell gitstat to remember it:\n\n    gitstat track ~/myproject\n\nNow when you run Gitstat with no parameters, it will include the status of `~/myproject`.\n\nTry editing/adding files in `~/myproject`, and/or commit (but don\'t push) changes, and run Gitstat again:\n\n    gitstat\n\nBy default, Gitstat will only output repos with changes.  To include repos that are up-to-date:\n\n    gitstat --all\n\nGitstat can fetch from origin:\n\n    gitstat fetch\n\nPull from origin:\n\n    gitstat pull\n\nGitstat will pull only if there are no local changes and if a pull from upstream is required.  You can run `gitstat fetch` to fetch first.\n\nGitstat can do more.  To get help with individual commands:\n\n    gitstat --help\n    gitstat check --help\n\n\n## Color customization\n\nThere are two config files, `repos.conf` which contains the list of all repos that Gitstat is tracking, and `gitstat.conf` which is used to configure Gitstat (currently it\'s just for colorization).  The config files live under `$XDG_CONFIG_HOME/gitstat/` (usually `~/.config/gitstat/`).\n\nYou can run `gitstat config` to show the locations of the files and colorization options:\n\n![gitstat colors](images/screenshots/colors.png)\n\n```ini\n# gitstat.conf\n\n# Run "gitstat config" to show the "Status" list and the default colors.\n# For each Status, a COLOR and STYLE can be specified.\n# STYLES can be: bold, dim, italic, underline, flash, reverse\n# COLORS can be:\n#   - a 6-hex string  #123456\n#   - an RGB tuple    (255, 0, 0)\n#   - a name          red\n\n[colors]\n# UNTRACKED_COLOR = (255, 0, 0)\n# UNTRACKED_STYLE = bold\n# PULL_REQUIRED_COLOR = #00FF11\n# UNCOMMITTED_COLOR = cyan\n```\n\n\n## Tips & tricks\n\n### Using with scripts\n\nSimilar to `git`, `gitstat --quiet` prints no output (except on error), and returns 1 if there are changes, else 0.\n\n### Clone missing repos\n\nIf moving to a new computer, or sharing Gitstat\'s config between multiple computers, `gitstat showclone` can be used to output a list of `git clone` commands for any repos Gitstat is tracking, but do not exist on the filesystem.  Then you can copy and paste the output to clone any missing repos.\n\n### Track every repo in your home directory\n\n    find ~/ -type d -name .git -exec gitstat track {} \\;\n\n(Gitstat is "smart" enough to know that the parent directory of a directory named `.git` is the actual repository.)\n\n### Are you tracking all the repos you want to track?\n\n    find ~/ -type d -name .git | xargs gitstat is-tracked --quiet-if-tracked\n\n\n## License\n\n```\nCopyright 2019-2021  John Begenisich\n\nThis program is free software: you can redistribute it and/or modify\nit under the terms of the GNU General Public License as published by\nthe Free Software Foundation, either version 3 of the License, or\n(at your option) any later version.\n\nThis program is distributed in the hope that it will be useful,\nbut WITHOUT ANY WARRANTY; without even the implied warranty of\nMERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the\nGNU General Public License for more details.\n\nYou should have received a copy of the GNU General Public License\nalong with this program.  If not, see <https://www.gnu.org/licenses/>.\n```\n',
    'author': 'John Begenisich',
    'author_email': 'john.begenisich@outlook.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://gitlab.com/johnivore/gitstat',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6.1,<4.0.0',
}


setup(**setup_kwargs)
