# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['comments_bot']

package_data = \
{'': ['*']}

install_requires = \
['aiodns>=3.0.0,<4.0.0',
 'aiohttp>=3.7.4,<4.0.0',
 'cchardet>=2.1.7,<3.0.0',
 'requests>=2.25.1,<3.0.0']

setup_kwargs = {
    'name': 'comments.bot',
    'version': '1.0.0',
    'description': 'A simple API wrapper for the comments.bot',
    'long_description': '# Comments.bot\n\n<p align="center">\n<a href="https://pypi.org/project/comments.bot/"><img src="https://img.shields.io/pypi/v/comments.bot" alt="PyPI"></a>\n<a href="https://pypi.org/project/comments.bot/"><img src="https://img.shields.io/pypi/pyversions/comments.bot.svg" alt="Supported Python Versions"></a>\n<a href="https://pepy.tech/project/comments.bot"><img src="https://pepy.tech/badge/comments.bot" alt="Downloads"></a>\n</p>\n\nA simple API wrapper to interact with [comments.bot](https://comments.bot) api.\n\n\n## Installation\n\nThe latest version of comments.bot is available via `pip`:\n\n```shell\npip install --upgrade comments.bot\n```\n\nAlso, you can download the source code and install using:\n\n```shell\npoetry install\n```\n\n**Note:** You need to have [poetry](https://python-poetry.org/) installed on your system\n\n## Usage\n\nThe library can be used in both Sync and Async!\nFor both there are 2 client which can be imported from comments_bot - SyncClient, AsyncClient.\n\n```python3\nfrom comments_bot import SyncClient, AsyncClient\nfrom asyncio import run\n\nasyncClient = AsyncClient(api_key="some api key", owner_id=12345678)  # Async Client\nsyncClient = SyncClient(api_key="some api key", owner_id=12345678)  # Sync Client\n\n# Both of the clients have same function - createPost, editPost, deletePost\npost_text_id, link_text = syncClient.createPost(text="hey")  # Post a text message\npost_photo_id, link_photo = syncClient.createPost(type="photo", photo_url="some url", caption="some text for caption")  # Post a photo\n\nstatus, post_text_id = syncClient.editPost(post_id=post_text_id, text="some other message")\n\nstatus = syncClient.deletePost(post_id=post_id)  # Deletes the post from comments.bot\n```\n\nYou can use the below methods for both SyncClient and AsyncClient.\n\n## Methods Available:\n\n### createPost() arguments:\n\n- owner_id:\n  - required if not passed on Client.\n\n- type:\n  - must be `text` or `photo`. `text` is used by default if not specified.\n\n- text:\n  - required if `type` equals to `text`. It must be a string betwen 0-4056 characters.\n\n- photo_url:\n  - required if `type` equals to `photo`. It must be a string containing a link to the image.\n\n- caption:\n  - Caption for the image. Only valid for `photo` type.\n\n- parse_mode:\n  - Parse mode for the text/caption. It must be `markdown` or `html`.\n\n- administrators:\n  - A string with user_ids (numbers) separated by comma. Example: `123456789,987654321,012345678`.\n\n- disable_notifications:\n  - Pass True if you don\'t want to receive notifications about new comments for your post.\n\n### editPost() arguments:\n\n- type:\n  - must be `text` or `photo`. `text` is used by default if not specified.\n\n- text:\n  - required if `type` equals to `text`. It must be a string betwen 0-4056 characters.\n\n- photo_url:\n  - required if `type` equals to `photo`. It must be a string containing a link to the image.\n\n- caption:\n  - Caption for the image. Only valid for `photo` type.\n\n- parse_mode:\n  - Parse mode for the text/caption. It must be `markdown` or `html`.\n\n### deletePost() arguments:\n\n- post_id:\n  - Pass the post id to be deleted\n\n\n## Contribuiting\n\nWanna help and improve this project?\n\nMake sure to follow these before opening a PR:\n\n- Make sure your PR passes the test and is formatted according to pre-commit.\n- Make sure the package is working without any issues!\n\n## License\n\nThis project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details\n',
    'author': 'Divkix',
    'author_email': 'techdroidroot@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/Divkix/comments.bot',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6.2,<4.0.0',
}


setup(**setup_kwargs)
