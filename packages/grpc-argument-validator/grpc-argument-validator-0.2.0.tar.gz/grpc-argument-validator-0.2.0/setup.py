# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['grpc_argument_validator']

package_data = \
{'': ['*']}

install_requires = \
['grpcio', 'protobuf']

setup_kwargs = {
    'name': 'grpc-argument-validator',
    'version': '0.2.0',
    'description': 'gRPC argument validator utility.',
    'long_description': '# gRPC argument validator\ngRPC argument validator is a library that provides decorators to automatically validate arguments in requests to rpc methods.\n\n<!-- GETTING STARTED -->\n## Getting Started\n\nThis is an example of how you may give instructions on setting up your project locally.\nTo get a local copy up and running follow these simple example steps.\n\n### Prerequisites\n\nPoetry is required to locally run the tests for this library\n* poetry\n  ```sh\n  pip install --user poetry\n  ```\n\n### Installation\n1. Clone the repo\n   ```sh\n   git clone https://github.com/messagebird/python-grpc-argument-validator.git\n   ```\n2. Install packages\n   ```sh\n   poetry install\n   ```\n3. Run the tests\n   ```sh\n   cd src/tests\n   poetry run python -m unittest\n   ```\n\n### Installation via pip\n```sh\npip install grpc-argument-validator\n```\n\n\n<!-- USAGE EXAMPLES -->\n## Example\n```python\nfrom google.protobuf.descriptor import FieldDescriptor\nfrom grpc_argument_validator import validate_args\nfrom grpc_argument_validator import AbstractArgumentValidator, ValidationResult, ValidationContext\n\nclass PathValidator(AbstractArgumentValidator):\n\n    def check(self, name: str, value: Path, field_descriptor: FieldDescriptor, validation_context: ValidationContext) -> ValidationResult:\n        if len(value.points) > 5:\n            return ValidationResult(valid=True)\n        return ValidationResult(False, f"path for \'{name}\' should be at least five points long")\n\nclass RouteService(RouteCheckerServicer):\n    @validate_args(\n        non_empty=["tags", "tags[]", "path.points"],\n        validators={"path": PathValidator()},\n    )\n    def Create(self, request: Route, context: grpc.ServicerContext):\n        return BoolValue(value=True)\n```\n\n\n\n\n<!-- CONTRIBUTING -->\n## Contributing\n\nContributions are what make the open source community such an amazing place to be learn, inspire, and create. Any contributions you make are **greatly appreciated**.\n\n1. Fork the Project\n2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)\n3. Commit your Changes (`git commit -m \'Add some AmazingFeature\'`)\n4. Push to the Branch (`git push origin feature/AmazingFeature`)\n5. Open a Pull Request\n\n\n## Documentation\nGenerate the docs by running:\n```sh\npdoc --html -o docs src/grpc_argument_validator\n```\n\n\n<!-- LICENSE -->\n## License\n\nDistributed under The BSD 3-Clause License. Copyright (c) 2021, MessageBird\n',
    'author': 'Jos van de Wolfshaar',
    'author_email': 'jos@messagebird.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/messagebird/python-grpc-argument-validator',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
