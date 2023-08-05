# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['kkloader']

package_data = \
{'': ['*']}

install_requires = \
['msgpack>=1.0.2,<2.0.0']

setup_kwargs = {
    'name': 'kkloader',
    'version': '0.1.4',
    'description': 'a simple deserializer / serializer for Koikatu / EmotionCreators data.',
    'long_description': '# KoikatuCharaLoader\nA simple deserializer / serializer for Koikatu / EmotionCreators character data.\n\n[日本語マニュアルがここにあります](README.ja.md)\n\n# Installation\nYou can install this module from [PyPI](https://pypi.org/project/kkloader/).\n```\n$ pip install kkloader\n```\nIf this does not work, try the following command (for Windows users, maybe).\n```\n$ python -m pip install kkloader\n```\n\n# Basic Usage\n```python\n$ python\n>>> from kkloader import KoikatuCharaData # Load a module.\n>>> kc = KoikatuCharaData.load("./data/kk_chara.png") # Load a character data.\n>>> kc["Parameter"]["nickname"] # Print character\'s nickname.\n\'かずのん\'\n>>> kc["Parameter"]["nickname"] = "chikarin" # Renaming nickname.\n>>> kc.save("./kk_chara_modified.png") # Save to `kk_chara_modified.png`.\n```\nthat\'s it :)\n\n# Mechanism of the Blockdata\n\nA character data of koikatu consists of some *blockdata*.\nThe *blockdata* is a collection of character parameters.\nA typical Koikatsu character data contains the following blockdata:\n\n| name of blockdata | description                                                  |\n| ----------------- | ------------------------------------------------------------ |\n| Custom            | Values for the character\'s face, body, and hairstyle.        |\n| Coordinate        | Values for clothes and accessories worn by characters.       |\n| Parameter         | Values for character names, birthdays, preferences, etc.     |\n| Status            | Values for clothed states, etc. (I\'m not sure how they are used in the game) |\n| About             | userID & dataID (added from Koikatu Sunshine)                |\n| KKEx              | Values used in MOD                                           |\n\nYou can check which block data exists from `blockdata` in KoikatuCharaData.\n```\n>>> kc.blockdata\n[\'Custom\', \'Coordinate\', \'Parameter\', \'Status\']\n```\nIf there is block data in an unknown format, it can be checked with `unknown_blockdata`.\n\n### Access to Blockdata\nThe blockdata can be accessed as a member variable of the `KoikatuCharaData` class, or accessed as a dictionary.\n```python\n>>> kc.Custom\n<kkloader.KoikatuCharaData.Custom object at 0x7f406bf18460>\n>>> kc["Custom"]\n<kkloader.KoikatuCharaData.Custom object at 0x7f406bf18460>\n```\nSo, these lines both access the same `kc.Custom`.\n\n### Find Variables\n\nBy using the `prettify` method, the contents of the variables contained in the block of data will be displayed in an easy-to-read format.\nThis is useful to find which variables exists.\n```\n>>> kc["Custom"].prettify()\n{\n  "face": {\n    "version": "0.0.2",\n    "shapeValueFace": [\n      ...\n    ],\n    "headId": 0,\n    "skinId": 0,\n    "detailId": 0,\n    "detailPower": 0.41674190759658813,\n    ...\n```\n\n# Export to JSON file\n```\nfrom kkloader import KoikatuCharaData\n\nk = KoikatuCharaData.load("./data/kk_chara.png")\nk.save_json("data.json") \n```\n\n`data.json`\n```data.json\n{\n  "product_no": 100,\n  "header": "\\u3010KoiKatuChara\\u3011",\n  "version": "0.0.0",\n  "Custom": {\n    "face": {\n      "version": "0.0.2",\n      "shapeValueFace": [\n        0.5403226017951965,\n        1.0,\n        0.2016129046678543,\n        0.0,\n        0.22580644488334656,\n        0.0,\n        0.0,\n        0.1794193685054779,\n        0.0,\n...\n```\nIf you add `include_image=True` to the argument of `save_json`, base64-encoded images will be included in json.\n\n# Recipes\n\n### Rename Character\'s Name\n```python\nfrom kkloader import KoikatuCharaData\n\nk = KoikatuCharaData.load("./data/kk_chara.png")\nk["Parameter"]["lastname"] = "春野"\nk["Parameter"]["firstname"] = "千佳"\nk["Parameter"]["nickname"] = "ちかりん"\nk.save("./data/kk_chara_modified")\n```\n\n### Set the Height of Character to 50\n```python\nfrom kkloader import KoikatuCharaData\n\nk = KoikatuCharaData.load("./data/kk_chara.png")\nk["Custom"]["body"]["shapeValueBody"][0] = 0.5\nk.save("./data/kk_chara_modified.png")  \n```\n\n### Remove Swim Cap\n```python\nfrom kkloader import KoikatuCharaData\n\nk = KoikatuCharaData.load("./data/kk_chara.png")\nfor i,c in enumerate(k["Coordinate"]):\n    for n,p in enumerate(c["accessory"]["parts"]):\n        if p["id"] == 5:\n            k["Coordinate"][i]["accessory"]["parts"][n]["type"] = 120\nk.save("./data/kk_chara_modified.png")  \n```\n\n### Remove Under Hair\n```python\nfrom kkloader import KoikatuCharaData\nkc = KoikatuCharaData.load("./data/kk_chara.png")\nkc["Custom"]["body"]["underhairId"] = 0\nkc.save("./data/kk_chara_modified.png")\n```\n\n# Acknowledgements\n- [martinwu42/pykoikatu](https://github.com/martinwu42/pykoikatu)',
    'author': 'great-majority',
    'author_email': 'yosaku.ideal+github@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/great-majority/KoikatuCharaLoader',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
