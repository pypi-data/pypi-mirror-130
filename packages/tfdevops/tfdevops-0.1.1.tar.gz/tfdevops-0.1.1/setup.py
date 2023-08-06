# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['tfdevops']

package_data = \
{'': ['*']}

install_requires = \
['boto3>=1.18.16,<2.0.0',
 'click>=8.0.1,<9.0.0',
 'jmespath>=0.10.0,<0.11.0',
 'jsonschema>=3.2.0,<4.0.0']

entry_points = \
{'console_scripts': ['tfdevops = tfdevops.cli:cli']}

setup_kwargs = {
    'name': 'tfdevops',
    'version': '0.1.1',
    'description': 'Terraform Support for AWS DevOps Guru',
    'long_description': "# tfdevops\n\nTerraform support for Amazon DevOps Guru. The service natively only supports AWS CloudFormation stacks.\nhttps://aws.amazon.com/devops-guru/features/\n\nThis project provides support for terraform users by automatically\nconverting terraform state to an imported CloudFormation stack\nand optionally enabling it with DevOps guru.\n\nNote Amazon DevOps Guru only supports roughly 25 resources.\nhttps://aws.amazon.com/devops-guru/pricing/\n\n\n## How it works\n\n- Translates terraform state into a CloudFormation template with a retain deletion policy\n- Creates a CloudFormation stack with imported resources\n- Enrolls the stack into Amazon DevOps Guru\n\n## Usage\n\nInstall it.\n\n```\npip install tfdevops\n```\n\nYou've got a deployed terraform root module extant, let's generate a CloudFormation template and a set of importable resources for it\n\n```\ntfdevops cfn -d ~/path/to/terraform/module --template mycfn.json --resources importable-ids.json\n```\n\n\nAnd now we can go ahead and create a CloudFormation stack, import resources, and activate DevOps Guru on our stack.\n\n```\ntfdevops deploy --template mycfn.json --resources importable-ids.json\n...\nINFO:tfdevops:Found existing stack, state:IMPORT_COMPLETE\nINFO:tfdevops:Creating import change set, 8 resources to import\nINFO:tfdevops:Executing change set to import resources\nINFO:tfdevops:Waiting for import to complete\nINFO:tfdevops:Cloudformation Stack Deployed - Terraform resources imported\n```\n\nYou can now visit the stack in the DevOps Guru dashboard.\n\nDepending on the level activity of the resources it can take DevOps Guru a few hours to generate any actionable insight.\n\n\nAs a bonus, we can validate the generated template (or any other pure CloudFormation template, aka sans intrinsics funcs or vars ), with the following\ncommand, which will download the jsonschema for the various resource types and validate each template resource against its schema.\n\n```\ntfdevops validate --template mycfn.json\n```\n\n## Large Resource/Templates\n\nAWS CloudFormation has various size limitations (50k api upload, 500k s3 upload) on the resource size it supports, both the `gen` and `deploy` subcommands support passing\nin an s3 path for the template and some resources which have larger configuration (step function workflows, etc). Note the s3 path for deploy is the actual template\npath.\n\n## FAQ\n\n1. Is this a generic terraform to CloudFormation converter?\n\nNo, while it has some facilities that resemble that, its very targeted at simply producing enough cfn to make Amazon DevOps Guru work.\n\n## Supported resources\n\n\nAt the moment tfdevops supports the following resources\n\n - AWS::StepFunctions::StateMachine\n - AWS::ECS::Service\n - AWS::SQS::Queue\n - AWS::SNS::Topic\n - AWS::RDS::DBInstance\n - AWS::Lambda::Function\n - AWS::Events::Rule\n - AWS::DynamoDB::Table",
    'author': 'Kapil Thangavelu',
    'author_email': 'kapilt@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
