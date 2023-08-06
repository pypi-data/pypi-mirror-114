# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ecs_tool',
 'ecs_tool.plugins',
 'ecs_tool.plugins.cluster',
 'ecs_tool.plugins.service',
 'ecs_tool.plugins.task']

package_data = \
{'': ['*']}

install_requires = \
['arrow>=1.1.0,<2.0.0',
 'asciiplot>=0.1.1,<0.2.0',
 'boto3>=1.9,<2.0',
 'click-log>=0.3.2,<0.4.0',
 'click>=8.0,<9.0',
 'loguru>=0.5.3,<0.6.0',
 'rich>=10.3.0,<11.0.0']

entry_points = \
{'console_scripts': ['ecs = ecs_tool.cli:safe_cli']}

setup_kwargs = {
    'name': 'ecs-tool',
    'version': '0.10.0',
    'description': 'ecs-tool tries to eliminate common caveats for your day-to-day work with Elastic Container Service (ECS).',
    'long_description': '# ECS Tool\n[![PyPI](https://img.shields.io/pypi/v/ecs-tool.svg)](https://pypi.org/project/ecs-tool/) ![](https://img.shields.io/pypi/pyversions/ecs-tool.svg) ![](https://img.shields.io/pypi/l/ecs-tool.svg)\n\n[aws-ecs](https://docs.aws.amazon.com/cli/latest/reference/ecs/index.html) on steroids.\n\necs-tool tries to eliminate common caveats for your day-to-day work with Elastic Container Service (ECS).\n\nDashboards with important information about your services, more intuitive CLI interface and more.\n\n### New version (`0.10`) is still in Beta.\n\n## Screenshots\n<a href="https://user-images.githubusercontent.com/164009/127609861-145265c3-5b1a-4ed2-a55b-2d400f7b0975.png" title="Dashboard"><img width="150" alt="Dashboard" src="https://user-images.githubusercontent.com/164009/127609795-ac1a5684-a334-418b-932f-15880bfe7066.png"></a>\n<a href="https://user-images.githubusercontent.com/164009/127610177-ca44d337-a2a3-469b-b413-8221e9c4598e.png" title="Cluster listing"><img width="150" alt="Cluster listing" src="https://user-images.githubusercontent.com/164009/127610175-c3ebd211-dc65-4770-8f69-360c1fb5bf89.png"></a>\n<a href="https://user-images.githubusercontent.com/164009/127610437-3d2f153e-7554-4284-9454-cfed8e2a3ac8.png" title="Serices list"><img width="150" alt="Services list" src="https://user-images.githubusercontent.com/164009/127610439-e8d0b543-3062-47c8-918f-4edd30bdf6eb.png"></a>\n\n## Summary of functionalities\n### Cluster\n* <a href="https://user-images.githubusercontent.com/164009/127610177-ca44d337-a2a3-469b-b413-8221e9c4598e.png">Listing of all clusters</a>\n### Service\n* <a href="https://user-images.githubusercontent.com/164009/127610437-3d2f153e-7554-4284-9454-cfed8e2a3ac8.png">Listing of all services</a>\n* <a href="https://user-images.githubusercontent.com/164009/127609861-145265c3-5b1a-4ed2-a55b-2d400f7b0975.png">Dashboard</a>, which includes `CPUUtilization` and `MemoryUtilization` plots for service (refreshed automatically)\n### Task\n* Run task, returns information about ran task, e.g. logs output from it (refreshed automatically)\n\nMore detailed information about available commands below.\n\n## Installation & usage\n\n### As python package\n```shell\npip install ecs-tool\n\necs\n\n# with aws-vault\naws-vault exec my-aws-profile -- ecs \n```\n\n### With docker\n```shell\n# build image\ndocker build -t ecs-tool\n\ndocker run -it --rm --name ecs-tool ecs-tool ecs\n\n# with aws-vault\ndocker run -it --rm --env-file <(aws-vault exec my-aws-profile -- env | grep "^AWS_") --name ecs-tool ecs-tool ecs\n```\n\n## What `ecs-tool` can do?\n\n### List of available clusters\n```shell\necs cluster list\n```\n\n### List of available services\n```shell\necs service list [OPTIONS]\n\nOptions:\n  --cluster TEXT\n```\n\n### Dashboard for service\n```shell\necs service dashboard [OPTIONS] SERVICE\n\nOptions:\n  --cluster TEXT\n```\n\n### Run task\n```shell\necs task run [OPTIONS] TASK_DEFINITION [COMMAND]...\n\nOptions:\n  --cluster TEXT\n  --network-configuration TEXT\n  --capacity-provider-strategy TEXT\n```\n\n`TASK_DEFINITION` - you can either provide full definition e.g. `my-definition:123` or just name, `my-definition`. If no number is provided, latest version is assumed.\n\n`[COMMAND]` - any command that should be executed on ECS task\n\nExamples:\n\n**Running with Fargate**\n```shell\necs task run epsy-dynks --capacity-provider-strategy \'{"capacityProvider": "FARGATE"}\' --network-configuration \'{"awsvpcConfiguration":{"subnets":["subnet-1234567890"],"securityGroups":["sg-123456789"],"assignPublicIp":"DISABLED"}}\' --  my_command subcommand --one-option --another-option="test"\n```\n\n## Can I use grep?\nYes! All commands results (but dashboards) can be filtered with `grep`\n',
    'author': 'Daniel Ancuta',
    'author_email': 'whisller@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/whisller/ecs-tool',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
