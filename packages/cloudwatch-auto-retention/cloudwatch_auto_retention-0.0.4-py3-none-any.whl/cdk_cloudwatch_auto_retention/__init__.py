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
import { CdkCloudwatchAutoRetention } from 'cloudwatch-auto-retention';

const mockApp = new cdk.App();
const stack = new cdk.Stack(mockApp, '<your-stack-name>');

new CdkCloudwatchAutoRetention(stack, 'cloudwatch-auto-retention');
```

### Python

#### Installation

```bash
$ pip install cloudwatch-auto-retention
```

#### Usage

```python
import aws_cdk.core as cdk
from cdk_cloudwatch_auto_retention import CdkCloudwatchAutoRetention

app = cdk.App()
stack = cdk.Stack(app, "<your-stack-name>")

CdkCloudwatchAutoRetention(stack, "cloudwatch-auto-retention")
```

## Overview

A Cloudwatch cron rule will trigger a Lambda that will go over all Cloudwatch Log Groups and check if the retention is never-expire. If so, it will change it to one month.

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

import constructs


class CdkCloudwatchAutoRetention(
    constructs.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="cloudwatch-auto-retention.CdkCloudwatchAutoRetention",
):
    def __init__(self, scope: constructs.Construct, id: builtins.str) -> None:
        '''
        :param scope: -
        :param id: -
        '''
        jsii.create(self.__class__, self, [scope, id])


__all__ = [
    "CdkCloudwatchAutoRetention",
]

publication.publish()
