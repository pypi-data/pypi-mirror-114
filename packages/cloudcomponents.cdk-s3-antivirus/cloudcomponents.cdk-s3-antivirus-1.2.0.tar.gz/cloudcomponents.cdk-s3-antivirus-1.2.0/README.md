[![cloudcomponents Logo](https://raw.githubusercontent.com/cloudcomponents/cdk-constructs/master/logo.png)](https://github.com/cloudcomponents/cdk-constructs)

# @cloudcomponents/cdk-s3-antivirus

[![Build Status](https://github.com/cloudcomponents/cdk-constructs/workflows/Build/badge.svg)](https://github.com/cloudcomponents/cdk-constructs/actions?query=workflow=Build)
[![cdkdx](https://img.shields.io/badge/buildtool-cdkdx-blue.svg)](https://github.com/hupe1980/cdkdx)
[![typescript](https://img.shields.io/badge/jsii-typescript-blueviolet.svg)](https://www.npmjs.com/package/@cloudcomponents/cdk-s3-antivirus)
[![python](https://img.shields.io/badge/jsii-python-blueviolet.svg)](https://pypi.org/project/cloudcomponents.cdk-s3-antivirus/)

> Antivirus for Amazon S3

## Install

TypeScript/JavaScript:

```bash
npm i @cloudcomponents/cdk-s3-antivirus
```

Python:

```bash
pip install cloudcomponents.cdk-s3-antivirus
```

## How to use

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
from aws_cdk.aws_lambda_destinations import SnsDestination
from aws_cdk.aws_s3 import Bucket
from aws_cdk.aws_sns import Topic
from aws_cdk.aws_sns_subscriptions import EmailSubscription
from aws_cdk.core import Construct, RemovalPolicy, Stack, StackProps

from cloudcomponents.cdk_s3_antivirus import Scanner

class S3AntivirusStack(Stack):
    def __init__(self, scope, id, *, description=None, env=None, stackName=None, tags=None, synthesizer=None, terminationProtection=None, analyticsReporting=None):
        super().__init__(scope, id, description=description, env=env, stackName=stackName, tags=tags, synthesizer=synthesizer, terminationProtection=terminationProtection, analyticsReporting=analyticsReporting)

        bucket = Bucket(self, "Bucket",
            auto_delete_objects=True,
            removal_policy=RemovalPolicy.DESTROY
        )

        topic = Topic(self, "Topic")
        topic.add_subscription(EmailSubscription(process.env.DEVSECOPS_TEAM_EMAIL))

        scanner = Scanner(self, "Scanner",
            on_result=SnsDestination(topic),
            on_error=SnsDestination(topic)
        )

        scanner.add_source_bucket(bucket)
```

## API Reference

See [API.md](https://github.com/cloudcomponents/cdk-constructs/tree/master/packages/cdk-s3-antivirus/API.md).

## Example

See more complete [examples](https://github.com/cloudcomponents/cdk-constructs/tree/master/examples).

## License

[MIT](https://github.com/cloudcomponents/cdk-constructs/tree/master/packages/cdk-s3-antivirus/LICENSE)
