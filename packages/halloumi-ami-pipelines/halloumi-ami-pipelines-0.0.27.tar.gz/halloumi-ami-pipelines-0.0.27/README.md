# Introduction

AMI Pipelines is a library for creating EC2 Image Builder pipelines with configurations on a given path. EC2 Image Builder pipelines are pipelines that can help create AMI images, based on 1 or more steps, called components, in a defined image recipe. These pipelines will create the AMI's as configured. All you need is to create one or more YAML files in a given directory and the library will create the necessary CodePipelines, EC2 Image Builder pipelines and components for you.

Supported parent images:

* CentOS7
* CentOS8
* Ubuntu1804
* Ubuntu2004

This is a sample configuration:

```YAML
---
pipeline:
  parent_image: AmazonLinux2 # or Ubuntu2004 or CentOS7

  sources: # Sources for use in the source stage of the Codepipeline.
    - name: Bucket
      type: s3
      bucket: kah-imagebuilder-s3-bucket-fra
      object: test.zip
    - name: Codecommit
      type: codecommit
      repo_name: testrepo
      branch: develop
  recipe:
    name: DemoCentos
    components:
        - name: install_cloudwatch_agent # Reference to a name in the component_dependencies section
        - name: another_ec2_ib_component_from_github
        - name: install_nginx
  schedule: cron(0 4 1 * ? *)
  shared_with: # Optional: Share images with another account. Image will be copied.
    - region: eu-west-1
      account_id: 123456789


component_dependencies:
  - name: another_ec2_ib_component_from_github
    type: git
    branch: master
    url: git@github.com:rainmaker2k/echo-world-component.git
  - name: install_cloudwatch_agent
    type: git
    branch: master
    url: git@github.com:rainmaker2k/ec2ib_install_cloudwatch.git
  - name: install_nginx
    branch: master
    type: git
    url: git@github.com:sentiampc/ami-pipelines-base-components.git
    path: nginx # Optional: If you have multiple component configurations in this repository.
  - name: aws_managed_component
    type: aws_arn
    arn: arn:aws:imagebuilder:eu-central-1:aws:component/amazon-cloudwatch-agent-linux/1.0.0
```

# Get started

This is a Typescript project, managed through Projen. Projen is project management tool that will help you manage most of the boilerplate scaffolding, by configuring the `.projenrc.js` file.

If you have not done so already, install projen through `npm`:

```
$ npm install -g projen
```

or

```
$ npx projen
```

Also install yarn.

```
$ npm install -g yarn
```

When you first checkout this project run:

```
$ projen
```

This will create all the necessary files from what is configured in `.projenrc.js`, like package.json, .gitignore etc... It will also pull in all the dependencies.

If everything is successful, you can run the build command to compile and package everything.

```
$ projen build
```

This will create a dist directory and create distibutable packages for NPM and Pypi.

# Examples

## Python

Here is an example of a stack in CDK to create the pipelines. This example assumes you have the YAML configurations stored in `.\ami_config\`

```Python
from aws_cdk import core
from ami_pipelines import PipelineBuilder

import os
import yaml
import glob


class DemoPyPipelineStack(core.Stack):

    def __init__(self, scope: core.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        print("Creating pipeline")
        pipeline_builder = PipelineBuilder()
        pipelines = pipeline_builder.create(self, "ami_config")
```

This assumes you have at least one pipeline config YAML in the `ami_config` directory.
