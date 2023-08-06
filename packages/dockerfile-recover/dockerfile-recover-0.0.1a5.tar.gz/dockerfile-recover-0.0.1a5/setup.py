# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['dockerfile_recover', 'dockerfile_recover.parser']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.0.1,<9.0.0', 'docker>=5.0.0,<6.0.0', 'six>=1.16.0,<2.0.0']

entry_points = \
{'console_scripts': ['dockerfile-recover = dockerfile_recover.__main__:main']}

setup_kwargs = {
    'name': 'dockerfile-recover',
    'version': '0.0.1a5',
    'description': 'dockerfile-recover is a tool to reconstruct Dockerfile by reverse engineering a docker image',
    'long_description': '# dockerfile-recover\ndockerfile-recover is a tool to reconstruct Dockerfile by reverse engineering a docker image\n\n# Installation\n\n## With pip\n```\npip install dockerfile-recover\n```\n## In a container\n```\ndocker pull purificant/dockerfile-recover\n```\n\n# Usage\n\n## When installing with pip\n```\ndocker pull <the image you want to reverse engineer>\ndockerfile-recover <image name>\n```\nFor example\n```\ndockerfile-recover python\ndockerfile-recover django\ndockerfile-recover redis\ndockerfile-recover node\n```\n\nor run as python module\n```\npython -m dockerfile_recover nginx\n```\n\n## When running in a container\n\n```\ndocker pull <the image you want to reverse engineer>\ndocker run -it -v /var/run/docker.sock:/var/run/docker.sock purificant/dockerfile-recover python -m dockerfile_recover <image name>\n```',
    'author': None,
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/purificant/dockerfile-recover',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
