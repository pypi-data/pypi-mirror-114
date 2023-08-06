# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['dependencmake', 'dependencmake.resources']

package_data = \
{'': ['*']}

install_requires = \
['GitPython>=3.1.13,<4.0.0',
 'PyYAML>=5.4.1,<6.0.0',
 'furl>=2.1.0,<3.0.0',
 'packaging>=21.0,<22.0',
 'path>=15.1.0,<16.0.0',
 'tqdm>=4.56.2,<5.0.0']

extras_require = \
{':python_version < "3.7"': ['importlib-resources>=5.1.0,<6.0.0'],
 ':python_version >= "3.6" and python_version < "3.7"': ['dataclasses>=0.8,<0.9']}

entry_points = \
{'console_scripts': ['dependencmake = dependencmake.__main__:main']}

setup_kwargs = {
    'name': 'dependencmake',
    'version': '0.1.0',
    'description': 'Dependencies manager for projects using CMake',
    'long_description': "[![Build Status](https://travis-ci.com/pzehner/dependencmake.svg?branch=master)](https://travis-ci.com/pzehner/dependencmake)\n[![codecov](https://codecov.io/gh/pzehner/dependencmake/branch/master/graph/badge.svg?token=XE5V2XO9XM)](https://codecov.io/gh/pzehner/dependencmake)\n\n# DependenCmake\n\nYet another dependency manager for projects using [CMake](https://cmake.org).\n\nAccording to CMake [documentation](https://cmake.org/cmake/help/git-stage/guide/using-dependencies/index.html), the best way to consume a CMake dependency is to install it and find it.\nUsing includes just creates mess.\n\nThis helper can fetch, build and install CMake dependencies in a specific directory that you can add to your project with `-DCMAKE_PREFIX_PATH`.\nIt keeps your system environment clean as you won't mix libraries up.\nThis can be also convenient for Fortran projects where installing libraries is not the standard due to the volatility of `mod` files.\n\n## Install\n\nThis package is managed with [Poetry](https://python-poetry.org/):\n\n```sh\npip install poetry\n```\n\nInstall from downloaded repository with:\n\n```sh\npoetry install --no-dev\n```\n\n## Usage\n\nThe generic usage of the command is:\n\n```sh\nENV=value dependencmake action path/to/cmake/dir\n```\n\nwhich is pretty close to how CMake is called.\nThe program will fetch/build/install desired dependencies and stored the result of the different actions in a `dependencmake` directory in the current directory.\n\nThe program will look for a `dependencmake.yaml` file in the specified directory, where dependencies are listed:\n\n```yaml\ndependencies:\n  - name: My dependency\n    url: file://my_server/my_dep.zip\n    cmake_args: -DUSE_MPI=ON\n  - name: My other dependency\n    url: http://my_repo/my_other_dep.git\n    git_hash: 25481515\n```\n\nMore info on the accepted parameters in the [configuration file](#configuration-file) section.\n\nThe program accepts several actions:\n\n- `create-config` to create a new configuration file;\n- `list` to list dependencies collected in the configuration file;\n- `fetch` to fetch dependencies and copy them on local disk;\n- `build` to fetch and build dependencies;\n- `install` to fetch, build and install dependencies;\n- `clean` to clean the cache.\n\nThe `build` and `install` actions will take any other arguments and pass them directly to CMake at configure step.\n\nIf you call `fetch`, `build` or `install` a second time, already fetched dependencies will most likely not be fetched again.\nGit dependencies will be pulled (unless `git_no_update` is set) and other kind of dependencies will rest untouched.\n\nExample of workflow:\n\n```sh\nmkdir build\ncd build\ndependencmake install .. -DCMAKE_BUILD_TYPE=Release\ncmake .. -DCMAKE_PREFIX_PATH=$PWD/dependencmake/install -DCMAKE_BUILD_TYPE=Release\nmake\n```\n\nthe `-DCMAKE_INSTALL_PREFIX` argument is required to tell CMake where dependencies are installed.\n\nIt is possible to set the install prefix to a custom value with the `install-prefix` argument.\nIn this case dependencies will be installed in this directory instead of in the DependenCmake cache:\n\n```sh\nmkdir build\ncd build\ndependencmake install --install-prefix lib/extern .. -DCMAKE_BUILD_TYPE=Release\ncmake .. -DCMAKE_PREFIX_PATH=$PWD/lib/extern -DCMAKE_BUILD_TYPE=Release\nmake\n```\n\n## Configuration file\n\nThe configuration file uses the [YAML format](https://en.wikipedia.org/wiki/YAML).\nIt stores dependencies information in the `dependencies` key as a list.\nEach item contains the following possible keys:\n\n- `name`:\n  Name of the dependency, used for display.\n  Mandatory;\n- `url`:\n  URL where to get the dependency.\n  Can be a Git repository, online only (must end by `.git`),\n  an archive, online or local (must end by `.zip`, `.tar`, `.tar.bz2`, `.tbz2`, `.tar.gz`, `.tgz`, `.tar.xz` or `.txz`),\n  or a plain directory, local only.\n  Mandatory;\n- `git_hash`:\n  Git hash to checkout to in case of Git repository.\n  The hash can be a commit hash or a tag.\n  Optional;\n- `git_no_update`:\n  When set to `true`, if the Git repository has been cloned, it will not been pulled on another run.\n  Optional;\n- `cmake_subdir`:\n  Subdirectory where to find the CMakeLists.txt file if it is not in the top directory.\n  Optional;\n- `cmake_args`:\n  Specific arguments to pass to CMake at configuration time.\n  Optional;\n- `jobs`:\n  Number of jobs to use when building the dependency.\n  By default, number of CPU cores * 2 + 1.\n  Optional.\n\n## Cache\n\nDependenCmake will put generated data in a `dependencmake` cache folder in the current working directory:\n\n```\ndependencmake/\n+-- build/\n+-- fetch/\n+-- install/\n```\n\nIt's pretty clear what the purpose of each subfolder of the cache is.\n`fetch` and `build` both contain a subfolder for each dependency.\nThe dependency directory name is the lower case and slugified name of the dependency, appended with a MD5 hash of the URL.\nThis allows to make the directory unique per couple name/URL and humanly readable.\n`install` has no logic enforced and is populated according to the `install` directives of the `CMakeLists.txt` files of the dependencies.\n\n## Additionnal checks\n\nAfter fetching dependencies, they are checked to detect patterns not managed by the program.\nFor now, diamond dependencies (where the same dependency is requested by two others) are invalid if they are not strictly equivalent.\n",
    'author': 'Paul Zehner',
    'author_email': 'paul.zehner@alumni.enseeiht.fr',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/pzehner/dependencmake',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.6.1,<4.0.0',
}


setup(**setup_kwargs)
