'''
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
'''
import abc
import builtins
import datetime
import enum
import typing

import jsii
import publication
import typing_extensions

from ._jsii import *

import aws_cdk.aws_codepipeline
import aws_cdk.aws_ec2
import aws_cdk.aws_imagebuilder
import aws_cdk.aws_kms
import aws_cdk.aws_sns
import aws_cdk.core


class AmiPipelineLib(
    aws_cdk.core.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="halloumi-ami-pipelines.AmiPipelineLib",
):
    '''Construct for creating a Codepipeline, EC2 Image builder pipeline from 1 pipeline configuration.'''

    def __init__(
        self,
        scope: aws_cdk.core.Construct,
        id: builtins.str,
        pipeline_config: typing.Any,
        component_deps_config: typing.Sequence[typing.Any],
        component_builder: "ComponentBuilder",
        *,
        channel: typing.Optional[builtins.str] = None,
        extra_params: typing.Optional[typing.Sequence["ComponentParameter"]] = None,
        slack_webhook_url: typing.Optional[builtins.str] = None,
        username: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Constructor.

        :param scope: -
        :param id: -
        :param pipeline_config: -
        :param component_deps_config: -
        :param component_builder: -
        :param channel: 
        :param extra_params: 
        :param slack_webhook_url: 
        :param username: 
        '''
        optional_params = AmiPipelineOptional(
            channel=channel,
            extra_params=extra_params,
            slack_webhook_url=slack_webhook_url,
            username=username,
        )

        jsii.create(AmiPipelineLib, self, [scope, id, pipeline_config, component_deps_config, component_builder, optional_params])

    @jsii.member(jsii_name="createCleanerTask")
    def create_cleaner_task(self) -> None:
        return typing.cast(None, jsii.invoke(self, "createCleanerTask", []))

    @jsii.member(jsii_name="createCodepipelineProject")
    def create_codepipeline_project(self) -> None:
        return typing.cast(None, jsii.invoke(self, "createCodepipelineProject", []))

    @jsii.member(jsii_name="createImagebuilderPipeline")
    def create_imagebuilder_pipeline(self) -> None:
        return typing.cast(None, jsii.invoke(self, "createImagebuilderPipeline", []))

    @jsii.member(jsii_name="createScheduledTask")
    def create_scheduled_task(self) -> None:
        return typing.cast(None, jsii.invoke(self, "createScheduledTask", []))

    @jsii.member(jsii_name="getLookupCriteria")
    def get_lookup_criteria(
        self,
        parent_image: typing.Any,
    ) -> aws_cdk.aws_ec2.LookupMachineImageProps:
        '''
        :param parent_image: -
        '''
        return typing.cast(aws_cdk.aws_ec2.LookupMachineImageProps, jsii.invoke(self, "getLookupCriteria", [parent_image]))

    @jsii.member(jsii_name="getNextRecipeVersion")
    def get_next_recipe_version(self, recipe_name: builtins.str) -> builtins.str:
        '''
        :param recipe_name: -
        '''
        return typing.cast(builtins.str, jsii.invoke(self, "getNextRecipeVersion", [recipe_name]))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="componentBuilder")
    def component_builder(self) -> "ComponentBuilder":
        return typing.cast("ComponentBuilder", jsii.get(self, "componentBuilder"))

    @component_builder.setter
    def component_builder(self, value: "ComponentBuilder") -> None:
        jsii.set(self, "componentBuilder", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="componentDepsConfig")
    def component_deps_config(self) -> typing.List[typing.Any]:
        return typing.cast(typing.List[typing.Any], jsii.get(self, "componentDepsConfig"))

    @component_deps_config.setter
    def component_deps_config(self, value: typing.List[typing.Any]) -> None:
        jsii.set(self, "componentDepsConfig", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        jsii.set(self, "id", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="pipelineConfig")
    def pipeline_config(self) -> typing.Any:
        return typing.cast(typing.Any, jsii.get(self, "pipelineConfig"))

    @pipeline_config.setter
    def pipeline_config(self, value: typing.Any) -> None:
        jsii.set(self, "pipelineConfig", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="slackConfig")
    def slack_config(self) -> "SlackConfiguration":
        return typing.cast("SlackConfiguration", jsii.get(self, "slackConfig"))

    @slack_config.setter
    def slack_config(self, value: "SlackConfiguration") -> None:
        jsii.set(self, "slackConfig", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="sourceActionBuilder")
    def source_action_builder(self) -> "SourceActionBuilder":
        return typing.cast("SourceActionBuilder", jsii.get(self, "sourceActionBuilder"))

    @source_action_builder.setter
    def source_action_builder(self, value: "SourceActionBuilder") -> None:
        jsii.set(self, "sourceActionBuilder", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="codepipeline")
    def codepipeline(self) -> typing.Optional[aws_cdk.aws_codepipeline.Pipeline]:
        return typing.cast(typing.Optional[aws_cdk.aws_codepipeline.Pipeline], jsii.get(self, "codepipeline"))

    @codepipeline.setter
    def codepipeline(
        self,
        value: typing.Optional[aws_cdk.aws_codepipeline.Pipeline],
    ) -> None:
        jsii.set(self, "codepipeline", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="diskSize")
    def disk_size(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "diskSize"))

    @disk_size.setter
    def disk_size(self, value: typing.Optional[jsii.Number]) -> None:
        jsii.set(self, "diskSize", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="distributionConfig")
    def distribution_config(
        self,
    ) -> typing.Optional[aws_cdk.aws_imagebuilder.CfnDistributionConfiguration]:
        return typing.cast(typing.Optional[aws_cdk.aws_imagebuilder.CfnDistributionConfiguration], jsii.get(self, "distributionConfig"))

    @distribution_config.setter
    def distribution_config(
        self,
        value: typing.Optional[aws_cdk.aws_imagebuilder.CfnDistributionConfiguration],
    ) -> None:
        jsii.set(self, "distributionConfig", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="ebsEncryptionKey")
    def ebs_encryption_key(self) -> typing.Optional[aws_cdk.aws_kms.Key]:
        return typing.cast(typing.Optional[aws_cdk.aws_kms.Key], jsii.get(self, "ebsEncryptionKey"))

    @ebs_encryption_key.setter
    def ebs_encryption_key(self, value: typing.Optional[aws_cdk.aws_kms.Key]) -> None:
        jsii.set(self, "ebsEncryptionKey", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="extraParameters")
    def extra_parameters(self) -> typing.Optional[typing.List["ComponentParameter"]]:
        return typing.cast(typing.Optional[typing.List["ComponentParameter"]], jsii.get(self, "extraParameters"))

    @extra_parameters.setter
    def extra_parameters(
        self,
        value: typing.Optional[typing.List["ComponentParameter"]],
    ) -> None:
        jsii.set(self, "extraParameters", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="imagePipeline")
    def image_pipeline(
        self,
    ) -> typing.Optional[aws_cdk.aws_imagebuilder.CfnImagePipeline]:
        return typing.cast(typing.Optional[aws_cdk.aws_imagebuilder.CfnImagePipeline], jsii.get(self, "imagePipeline"))

    @image_pipeline.setter
    def image_pipeline(
        self,
        value: typing.Optional[aws_cdk.aws_imagebuilder.CfnImagePipeline],
    ) -> None:
        jsii.set(self, "imagePipeline", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="infrastructure")
    def infrastructure(
        self,
    ) -> typing.Optional[aws_cdk.aws_imagebuilder.CfnInfrastructureConfiguration]:
        return typing.cast(typing.Optional[aws_cdk.aws_imagebuilder.CfnInfrastructureConfiguration], jsii.get(self, "infrastructure"))

    @infrastructure.setter
    def infrastructure(
        self,
        value: typing.Optional[aws_cdk.aws_imagebuilder.CfnInfrastructureConfiguration],
    ) -> None:
        jsii.set(self, "infrastructure", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="recipe")
    def recipe(self) -> typing.Optional[aws_cdk.aws_imagebuilder.CfnImageRecipe]:
        return typing.cast(typing.Optional[aws_cdk.aws_imagebuilder.CfnImageRecipe], jsii.get(self, "recipe"))

    @recipe.setter
    def recipe(
        self,
        value: typing.Optional[aws_cdk.aws_imagebuilder.CfnImageRecipe],
    ) -> None:
        jsii.set(self, "recipe", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="topic")
    def topic(self) -> typing.Optional[aws_cdk.aws_sns.Topic]:
        return typing.cast(typing.Optional[aws_cdk.aws_sns.Topic], jsii.get(self, "topic"))

    @topic.setter
    def topic(self, value: typing.Optional[aws_cdk.aws_sns.Topic]) -> None:
        jsii.set(self, "topic", value)


@jsii.data_type(
    jsii_type="halloumi-ami-pipelines.AmiPipelineOptional",
    jsii_struct_bases=[],
    name_mapping={
        "channel": "channel",
        "extra_params": "extraParams",
        "slack_webhook_url": "slackWebhookUrl",
        "username": "username",
    },
)
class AmiPipelineOptional:
    def __init__(
        self,
        *,
        channel: typing.Optional[builtins.str] = None,
        extra_params: typing.Optional[typing.Sequence["ComponentParameter"]] = None,
        slack_webhook_url: typing.Optional[builtins.str] = None,
        username: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param channel: 
        :param extra_params: 
        :param slack_webhook_url: 
        :param username: 
        '''
        self._values: typing.Dict[str, typing.Any] = {}
        if channel is not None:
            self._values["channel"] = channel
        if extra_params is not None:
            self._values["extra_params"] = extra_params
        if slack_webhook_url is not None:
            self._values["slack_webhook_url"] = slack_webhook_url
        if username is not None:
            self._values["username"] = username

    @builtins.property
    def channel(self) -> typing.Optional[builtins.str]:
        result = self._values.get("channel")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def extra_params(self) -> typing.Optional[typing.List["ComponentParameter"]]:
        result = self._values.get("extra_params")
        return typing.cast(typing.Optional[typing.List["ComponentParameter"]], result)

    @builtins.property
    def slack_webhook_url(self) -> typing.Optional[builtins.str]:
        result = self._values.get("slack_webhook_url")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def username(self) -> typing.Optional[builtins.str]:
        result = self._values.get("username")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AmiPipelineOptional(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ArnComponentRef(
    metaclass=jsii.JSIIMeta,
    jsii_type="halloumi-ami-pipelines.ArnComponentRef",
):
    def __init__(self, arn: builtins.str, name: builtins.str) -> None:
        '''
        :param arn: -
        :param name: -
        '''
        jsii.create(ArnComponentRef, self, [arn, name])

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        jsii.set(self, "name", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="ref")
    def ref(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "ref"))

    @ref.setter
    def ref(self, value: builtins.str) -> None:
        jsii.set(self, "ref", value)


class ComponentBuilder(
    metaclass=jsii.JSIIMeta,
    jsii_type="halloumi-ami-pipelines.ComponentBuilder",
):
    def __init__(
        self,
        scope: aws_cdk.core.Construct,
        component_defs: typing.Sequence[typing.Any],
    ) -> None:
        '''
        :param scope: -
        :param component_defs: -
        '''
        jsii.create(ComponentBuilder, self, [scope, component_defs])

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="cacheDir")
    def cache_dir(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "cacheDir"))

    @cache_dir.setter
    def cache_dir(self, value: builtins.str) -> None:
        jsii.set(self, "cacheDir", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="componentDependenciesMap")
    def component_dependencies_map(
        self,
    ) -> typing.Mapping[builtins.str, typing.Union[ArnComponentRef, aws_cdk.aws_imagebuilder.CfnComponent]]:
        return typing.cast(typing.Mapping[builtins.str, typing.Union[ArnComponentRef, aws_cdk.aws_imagebuilder.CfnComponent]], jsii.get(self, "componentDependenciesMap"))

    @component_dependencies_map.setter
    def component_dependencies_map(
        self,
        value: typing.Mapping[builtins.str, typing.Union[ArnComponentRef, aws_cdk.aws_imagebuilder.CfnComponent]],
    ) -> None:
        jsii.set(self, "componentDependenciesMap", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="componentDeps")
    def component_deps(self) -> typing.List[typing.Any]:
        return typing.cast(typing.List[typing.Any], jsii.get(self, "componentDeps"))

    @component_deps.setter
    def component_deps(self, value: typing.List[typing.Any]) -> None:
        jsii.set(self, "componentDeps", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="scope")
    def scope(self) -> aws_cdk.core.Construct:
        return typing.cast(aws_cdk.core.Construct, jsii.get(self, "scope"))

    @scope.setter
    def scope(self, value: aws_cdk.core.Construct) -> None:
        jsii.set(self, "scope", value)


@jsii.data_type(
    jsii_type="halloumi-ami-pipelines.ComponentDependency",
    jsii_struct_bases=[],
    name_mapping={
        "branch": "branch",
        "name": "name",
        "path": "path",
        "platform": "platform",
        "type": "type",
        "url": "url",
    },
)
class ComponentDependency:
    def __init__(
        self,
        *,
        branch: builtins.str,
        name: builtins.str,
        path: builtins.str,
        platform: builtins.str,
        type: builtins.str,
        url: builtins.str,
    ) -> None:
        '''
        :param branch: 
        :param name: 
        :param path: 
        :param platform: 
        :param type: 
        :param url: 
        '''
        self._values: typing.Dict[str, typing.Any] = {
            "branch": branch,
            "name": name,
            "path": path,
            "platform": platform,
            "type": type,
            "url": url,
        }

    @builtins.property
    def branch(self) -> builtins.str:
        result = self._values.get("branch")
        assert result is not None, "Required property 'branch' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def path(self) -> builtins.str:
        result = self._values.get("path")
        assert result is not None, "Required property 'path' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def platform(self) -> builtins.str:
        result = self._values.get("platform")
        assert result is not None, "Required property 'platform' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def type(self) -> builtins.str:
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def url(self) -> builtins.str:
        result = self._values.get("url")
        assert result is not None, "Required property 'url' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComponentDependency(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="halloumi-ami-pipelines.ComponentParameter",
    jsii_struct_bases=[],
    name_mapping={"component_name": "componentName", "parameters": "parameters"},
)
class ComponentParameter:
    def __init__(
        self,
        *,
        component_name: builtins.str,
        parameters: typing.Mapping[builtins.str, builtins.str],
    ) -> None:
        '''
        :param component_name: 
        :param parameters: 
        '''
        self._values: typing.Dict[str, typing.Any] = {
            "component_name": component_name,
            "parameters": parameters,
        }

    @builtins.property
    def component_name(self) -> builtins.str:
        result = self._values.get("component_name")
        assert result is not None, "Required property 'component_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def parameters(self) -> typing.Mapping[builtins.str, builtins.str]:
        result = self._values.get("parameters")
        assert result is not None, "Required property 'parameters' is missing"
        return typing.cast(typing.Mapping[builtins.str, builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ComponentParameter(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ComponentSynchronizer(
    metaclass=jsii.JSIIMeta,
    jsii_type="halloumi-ami-pipelines.ComponentSynchronizer",
):
    '''Ensures that component dependencies are downloaded and available.'''

    def __init__(self) -> None:
        jsii.create(ComponentSynchronizer, self, [])

    @jsii.member(jsii_name="synchronize")
    def synchronize(
        self,
        component_defs: typing.Sequence[ComponentDependency],
    ) -> builtins.str:
        '''
        :param component_defs: -
        '''
        return typing.cast(builtins.str, jsii.ainvoke(self, "synchronize", [component_defs]))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="cacheDir")
    def cache_dir(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "cacheDir"))

    @cache_dir.setter
    def cache_dir(self, value: builtins.str) -> None:
        jsii.set(self, "cacheDir", value)


class PipelineBuilder(
    metaclass=jsii.JSIIMeta,
    jsii_type="halloumi-ami-pipelines.PipelineBuilder",
):
    def __init__(self, config: typing.Any) -> None:
        '''
        :param config: -
        '''
        jsii.create(PipelineBuilder, self, [config])

    @jsii.member(jsii_name="create")
    def create(
        self,
        stack: aws_cdk.core.Construct,
        pipeline_config_dir: builtins.str,
    ) -> typing.List[AmiPipelineLib]:
        '''
        :param stack: -
        :param pipeline_config_dir: -
        '''
        return typing.cast(typing.List[AmiPipelineLib], jsii.ainvoke(self, "create", [stack, pipeline_config_dir]))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="cacheDir")
    def cache_dir(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "cacheDir"))

    @cache_dir.setter
    def cache_dir(self, value: builtins.str) -> None:
        jsii.set(self, "cacheDir", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="config")
    def config(self) -> typing.Any:
        return typing.cast(typing.Any, jsii.get(self, "config"))

    @config.setter
    def config(self, value: typing.Any) -> None:
        jsii.set(self, "config", value)


@jsii.data_type(
    jsii_type="halloumi-ami-pipelines.SlackConfiguration",
    jsii_struct_bases=[],
    name_mapping={
        "channel": "channel",
        "slack_webhook_url": "slackWebhookUrl",
        "username": "username",
    },
)
class SlackConfiguration:
    def __init__(
        self,
        *,
        channel: typing.Optional[builtins.str] = None,
        slack_webhook_url: typing.Optional[builtins.str] = None,
        username: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param channel: 
        :param slack_webhook_url: 
        :param username: 
        '''
        self._values: typing.Dict[str, typing.Any] = {}
        if channel is not None:
            self._values["channel"] = channel
        if slack_webhook_url is not None:
            self._values["slack_webhook_url"] = slack_webhook_url
        if username is not None:
            self._values["username"] = username

    @builtins.property
    def channel(self) -> typing.Optional[builtins.str]:
        result = self._values.get("channel")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def slack_webhook_url(self) -> typing.Optional[builtins.str]:
        result = self._values.get("slack_webhook_url")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def username(self) -> typing.Optional[builtins.str]:
        result = self._values.get("username")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SlackConfiguration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SlackNotification(
    aws_cdk.core.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="halloumi-ami-pipelines.SlackNotification",
):
    def __init__(
        self,
        scope: aws_cdk.core.Construct,
        id: builtins.str,
        sns_topic: aws_cdk.aws_sns.Topic,
        slack_config: SlackConfiguration,
        recipename: builtins.str,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param sns_topic: -
        :param slack_config: -
        :param recipename: -
        '''
        jsii.create(SlackNotification, self, [scope, id, sns_topic, slack_config, recipename])

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="snsTopic")
    def sns_topic(self) -> aws_cdk.aws_sns.Topic:
        return typing.cast(aws_cdk.aws_sns.Topic, jsii.get(self, "snsTopic"))

    @sns_topic.setter
    def sns_topic(self, value: aws_cdk.aws_sns.Topic) -> None:
        jsii.set(self, "snsTopic", value)


class SourceAction(
    metaclass=jsii.JSIIMeta,
    jsii_type="halloumi-ami-pipelines.SourceAction",
):
    def __init__(
        self,
        source_output: aws_cdk.aws_codepipeline.Artifact,
        action: aws_cdk.aws_codepipeline.IAction,
    ) -> None:
        '''
        :param source_output: -
        :param action: -
        '''
        jsii.create(SourceAction, self, [source_output, action])

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="action")
    def action(self) -> aws_cdk.aws_codepipeline.IAction:
        return typing.cast(aws_cdk.aws_codepipeline.IAction, jsii.get(self, "action"))

    @action.setter
    def action(self, value: aws_cdk.aws_codepipeline.IAction) -> None:
        jsii.set(self, "action", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="sourceOutput")
    def source_output(self) -> aws_cdk.aws_codepipeline.Artifact:
        return typing.cast(aws_cdk.aws_codepipeline.Artifact, jsii.get(self, "sourceOutput"))

    @source_output.setter
    def source_output(self, value: aws_cdk.aws_codepipeline.Artifact) -> None:
        jsii.set(self, "sourceOutput", value)


class SourceActionBuilder(
    metaclass=jsii.JSIIMeta,
    jsii_type="halloumi-ami-pipelines.SourceActionBuilder",
):
    def __init__(
        self,
        scope: aws_cdk.core.Construct,
        sources: typing.Any,
        id_prefix: builtins.str,
    ) -> None:
        '''
        :param scope: -
        :param sources: -
        :param id_prefix: -
        '''
        jsii.create(SourceActionBuilder, self, [scope, sources, id_prefix])

    @jsii.member(jsii_name="createPipelineSources")
    def create_pipeline_sources(self) -> typing.List[SourceAction]:
        return typing.cast(typing.List[SourceAction], jsii.invoke(self, "createPipelineSources", []))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="idPrefix")
    def id_prefix(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "idPrefix"))

    @id_prefix.setter
    def id_prefix(self, value: builtins.str) -> None:
        jsii.set(self, "idPrefix", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="scope")
    def scope(self) -> aws_cdk.core.Construct:
        return typing.cast(aws_cdk.core.Construct, jsii.get(self, "scope"))

    @scope.setter
    def scope(self, value: aws_cdk.core.Construct) -> None:
        jsii.set(self, "scope", value)

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="sources")
    def sources(self) -> typing.Any:
        return typing.cast(typing.Any, jsii.get(self, "sources"))

    @sources.setter
    def sources(self, value: typing.Any) -> None:
        jsii.set(self, "sources", value)


class SsmUpdateConstruct(
    aws_cdk.core.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="halloumi-ami-pipelines.SsmUpdateConstruct",
):
    def __init__(
        self,
        scope: aws_cdk.core.Construct,
        id: builtins.str,
        sns_topic: aws_cdk.aws_sns.Topic,
        pipeline_config: typing.Any,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param sns_topic: -
        :param pipeline_config: -
        '''
        jsii.create(SsmUpdateConstruct, self, [scope, id, sns_topic, pipeline_config])


@jsii.data_type(
    jsii_type="halloumi-ami-pipelines.StringComponentMap",
    jsii_struct_bases=[],
    name_mapping={},
)
class StringComponentMap:
    def __init__(self) -> None:
        self._values: typing.Dict[str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "StringComponentMap(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "AmiPipelineLib",
    "AmiPipelineOptional",
    "ArnComponentRef",
    "ComponentBuilder",
    "ComponentDependency",
    "ComponentParameter",
    "ComponentSynchronizer",
    "PipelineBuilder",
    "SlackConfiguration",
    "SlackNotification",
    "SourceAction",
    "SourceActionBuilder",
    "SsmUpdateConstruct",
    "StringComponentMap",
]

publication.publish()
