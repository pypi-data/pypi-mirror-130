'''
# Cloudwatch Auto Retention

![release](https://github.com/stroobants-dev/cloudwatch-auto-retention/actions/workflows/release.yml/badge.svg)[![npm version](https://badge.fury.io/js/cloudwatch-auto-retention.svg)](https://badge.fury.io/js/cloudwatch-auto-retention)[![PyPI version](https://badge.fury.io/py/cloudwatch-auto-retention.svg)](https://badge.fury.io/py/cloudwatch-auto-retention)

Cloudwatch Auto Retention is an AWS CDK construct library that will check once a month if you have any Cloudwatch Log Groups in the region it is deployed with a never-expire retention and auto-fix this to one month. This is a cost-optimization as Cloudwatch Logs have a very high storage cost. If you need Cloudwatch logs for longer you should set an automated S3 export (cloudwatch-logs-s3-export is in the works 😚).

## Getting started

### TypeScript

#### Installation

##### NPM

```
npm install --save cloudwatch-auto-retention
```

##### yarn

```
yarn add cloudwatch-auto-retention
```

#### Usage

```python
# Example automatically generated from non-compiling source. May contain errors.
import * as cdk from '@aws-cdk/core';
import { CloudwatchAutoRetention } from 'cloudwatch-auto-retention';
import { RetentionDays } from 'aws-cdk-lib/aws-logs';
import { Schedule } from 'aws-cdk-lib/aws-events';

const mockApp = new cdk.App();
const stack = new cdk.Stack(mockApp, '<your-stack-name>');

new CloudwatchAutoRetention(stack, 'cloudwatch-auto-retention');

// With retention set
new CloudwatchAutoRetention(stack, 'cloudwatch-auto-retention', {
    retention: RetentionDays.ONE_MONTH
});

// With schedule for the Lambda function set
new CloudwatchAutoRetention(stack, 'cloudwatch-auto-retention', {
    schedule: Schedule.cron({ minute: '0', hour: '1', day: '1' })
});
```

### Python

#### Installation

```bash
$ pip install cloudwatch-auto-retention
```

#### Usage

```python
import aws_cdk.core as cdk
from cdk_cloudwatch_auto_retention import CloudwatchAutoRetention

app = cdk.App()
stack = cdk.Stack(app, "<your-stack-name>")

CdkCloudwatchAutoRetention(stack, "cloudwatch-auto-retention")
```

## Overview

A Cloudwatch cron rule will trigger a Lambda that will go over all Cloudwatch Log Groups and check if the retention is never-expire. If so, it will change it to one month default or whatever you set as `retention`.

![](https://raw.githubusercontent.com/stroobants-dev/cloudwatch-auto-retention/main/images/overview.png)
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

import aws_cdk.aws_events
import aws_cdk.aws_logs
import constructs


class CloudwatchAutoRetention(
    constructs.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="cloudwatch-auto-retention.CloudwatchAutoRetention",
):
    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        retention: typing.Optional[aws_cdk.aws_logs.RetentionDays] = None,
        schedule: typing.Optional[aws_cdk.aws_events.Schedule] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param retention: 
        :param schedule: 
        '''
        props = CloudwatchAutoRetentionProps(retention=retention, schedule=schedule)

        jsii.create(self.__class__, self, [scope, id, props])


@jsii.data_type(
    jsii_type="cloudwatch-auto-retention.CloudwatchAutoRetentionProps",
    jsii_struct_bases=[],
    name_mapping={"retention": "retention", "schedule": "schedule"},
)
class CloudwatchAutoRetentionProps:
    def __init__(
        self,
        *,
        retention: typing.Optional[aws_cdk.aws_logs.RetentionDays] = None,
        schedule: typing.Optional[aws_cdk.aws_events.Schedule] = None,
    ) -> None:
        '''
        :param retention: 
        :param schedule: 
        '''
        self._values: typing.Dict[str, typing.Any] = {}
        if retention is not None:
            self._values["retention"] = retention
        if schedule is not None:
            self._values["schedule"] = schedule

    @builtins.property
    def retention(self) -> typing.Optional[aws_cdk.aws_logs.RetentionDays]:
        result = self._values.get("retention")
        return typing.cast(typing.Optional[aws_cdk.aws_logs.RetentionDays], result)

    @builtins.property
    def schedule(self) -> typing.Optional[aws_cdk.aws_events.Schedule]:
        result = self._values.get("schedule")
        return typing.cast(typing.Optional[aws_cdk.aws_events.Schedule], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudwatchAutoRetentionProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "CloudwatchAutoRetention",
    "CloudwatchAutoRetentionProps",
]

publication.publish()
