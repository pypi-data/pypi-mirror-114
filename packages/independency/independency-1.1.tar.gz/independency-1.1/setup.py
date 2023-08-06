# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['independency']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'independency',
    'version': '1.1',
    'description': 'Dependency injection container',
    'long_description': "# Independency\nIndependency is a DI container library. Unlike many other Python DI containers Independency operates in the local scope. It's inspired by [punq](https://github.com/bobthemighty/punq), so the API is very similar.\n\nIndependency supports generics and other specific typings.\n\n\n## Installation\n\n```bash\npip install independency\n```\n\n## Examples\nLet's begin with a simple example.\n```python3\nimport requests\n\nfrom independency import Container, ContainerBuilder\n\n\nclass Config:\n    def __init__(self, url: str):\n        self.url = url\n\n\nclass Getter:\n    def __init__(self, config: Config):\n        self.config = config\n\n    def get(self):\n        return requests.get(self.config.url)\n\n\ndef create_container() -> Container:\n    builder = ContainerBuilder()\n    builder.singleton(Config, Config, url='http://example.com')\n    builder.singleton(Getter, Getter)\n    return builder.build()\n\n\ndef main():\n    container = create_container()\n    getter: Getter = container.resolve(Getter)\n    print(getter.get().status_code)\n\n\nif __name__ == '__main__':\n    main()\n```\n",
    'author': 'apollon',
    'author_email': 'Apollon76@yandex.ru',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/Apollon76/di',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
