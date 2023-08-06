# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['jce']

package_data = \
{'': ['*']}

install_requires = \
['pydantic>=1.8.1,<2.0.0', 'typing-extensions>=3.7.4,<5.0.0']

setup_kwargs = {
    'name': 'jcestruct',
    'version': '0.1.5',
    'description': 'JCE Encode/Decode',
    'long_description': '# Jce Struct\n\nTencent JCE Encode/Decode with fully pydantic support\n\n## Before Using\n\n`JceStruct` is base on **python type hint** ([doc](https://www.python.org/dev/peps/pep-0484/)) and [Pydantic](https://pydantic-docs.helpmanual.io/).\n\nRead links above if first time using `type hint` or `pydantic model`.\n\n`Data validation` and `IDE type checking` are **all supported**.\n\n## Installation\n\nInstall directly\n\n```bash\npip install JceStruct\n# or\npoetry add JceStruct\n```\n\nor install from source (using poetry)\n\n```bash\npip install git+https://github.com/yanyongyu/JceStruct.git\n# or\npoetry add git+https://github.com/yanyongyu/JceStruct.git\n```\n\nor clone and install\n\n```bash\ngit clone https://github.com/yanyongyu/JceStruct.git\ncd JceStruct\npoetry install  # with editable mode\n```\n\n## Usage\n\n### Create Struct\n\nCreate your struct by inheriting `JceStruct` and define your fields with `JceField`.\n\n> You can also combine your model fields with typing `Optional`, `Union`...\n\n```python\nfrom jce import types, JceStruct, JceField\n\n\nclass ExampleStruct(JceStruct):\n    # normal definition\n    field1: types.INT32 = JceField(jce_id=1)\n    # define type in options\n    field2: float = JceField(jce_id=2, jce_type=types.DOUBLE)\n    # define an optional field with default value\n    field3: Optional[types.BOOL] = JceField(None, jce_id=3)\n    # nested struct supported\n    field4: types.LIST[OtherStruct] = JceField(types.LIST(), jce_id=4)\n    # optional other pydantic field\n    extra_pydantic_field: str = "extra_pydantic_field"\n```\n\n### Encode/Decode\n\nYou can initialize a struct and encode it, or encode single field using `to_bytes` method.\n\n```python\n# simple struct encode\nexample: ExampleStruct = ExampleStruct(\n    field1=1, field2=2., field4=types.LIST[OtherStruct()]\n)\nbytes = example.encode()\n\n# single field encode\nbytes = types.STRING.to_bytes(jce_id=0, value="example")\n```\n\nYou can decode bytes using `decode` classmethod of the struct, decode single field using `from_bytes` classmethod, or only get single list field using `decode_list` method of list inner struct.\n\n```python\n# simple struct decode\nexample: ExampleStruct = ExampleStruct.decode(bytes, extra_pydantic_field="extra")\n\n# single field decode\nstring, length = types.STRING.from_bytes(data=bytes, **extra)\n\n# decode list from example struct\nothers: List[OtherStruct] = OtherStruct.decode_list(bytes, jce_id=3, **extra)\n```\n\n### Custom Encoder/Decoder\n\nJust inherit JceEncoder/JceDecoder and add it to your struct configuration.\n\n```python\nfrom jce import JceStruct, JceEncoder\n\n\nclass CustomEncoder(JceEncoder):\n    pass\n\n\nclass ExampleStruct(JceStruct):\n\n    class Config:\n        jce_encoder = CustomEncoder\n        # jce_decoder = CustomDecoder\n```\n\n### Custom types\n\nJust inherit JceType and implement abstruct methods\n\n```python\nfrom jce import types\n\n\nclass CustomType(types.JceType):\n    ...\n```\n\n### Change default types\n\nBy default, head bytes are treated like this:\n\n```python\n{\n    0: BYTE,\n    1: INT16,\n    2: INT32,\n    3: INT64,\n    4: FLOAT,\n    5: DOUBLE,\n    6: STRING1,\n    7: STRING4,\n    8: MAP,\n    9: LIST,\n    10: STRUCT_START,\n    11: STRUCT_END,\n    12: ZERO_TAG,\n    13: BYTES\n}\n```\n\nfield will be converted to the type defined in struct when validate.\n\nto change it:\n\n```python\nclass ExampleStruct(JceStruct):\n\n    class Config:\n        jce_default_type = {\n            # add all types here\n        }\n```\n\n## Command Line Usage\n\n```bash\npython -m jce 1f2e3d4c5b6a79\n```\n',
    'author': 'yanyongyu',
    'author_email': 'yanyongyu_1@126.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/yanyongyu/JceStruct',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
