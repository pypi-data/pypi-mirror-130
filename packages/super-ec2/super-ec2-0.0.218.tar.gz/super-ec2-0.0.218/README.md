[![NPM version](https://badge.fury.io/js/%40cdk-constructs-zone%2Fsuper-ec2.svg)](https://badge.fury.io/js/%40cdk-constructs-zone%2Fsuper-ec2)
[![PyPI version](https://badge.fury.io/py/super-ec2.svg)](https://badge.fury.io/py/super-ec2)
![Release](https://github.com/cdk-constructs-zone/super-ec2/workflows/release/badge.svg)

![Downloads](https://img.shields.io/badge/-DOWNLOADS:-brightgreen?color=gray)
![npm](https://img.shields.io/npm/dt/@cdk-constructs-zone/super-ec2?label=npm&color=orange)
![PyPI](https://img.shields.io/pypi/dm/super-ec2?label=pypi&color=blue)

![](https://img.shields.io/badge/jenkins-ec2-green=?style=plastic&logo=appveyor)

# Welcome to `@cdk-constructs-zone/super-ec2`

This repository template helps you create EC2 .

## Sample

### Jenkins

* Simplest deployment: It would creat a VPC and ALB by default.

```python
# Example automatically generated from non-compiling source. May contain errors.
import aws_cdk.core as cdk
from cdk_constructs_zone.super_ec2 import JenkinsEC2, ELBtype

app = cdk.App()

stack = cdk.Stack(app, "demo")

jks = JenkinsEC2(stack, "superJks")

cdk.CfnOutput(stack, "loadbalancerDNS",
    value=jks.loadbalancer.load_balancer_dns_name
)
cdk.CfnOutput(stack, "connect-to-instance",
    value=f"aws ssm start-session --target {jks.instance.instanceId}"
)
```

* Deploy Jenkins with self-defined VPC and NLB

```python
# Example automatically generated from non-compiling source. May contain errors.
jks = JenkinsEC2(stack, "superJks",
    vpc=Vpc.from_lookup(stack, "defaultVPC", is_default=True),
    loadbalancer_type=ELBtype.NLB
)
```

* Deploy Jenkins with R53 records: If `acm` is not given, it would create a certificate validated from DNS by default.

```python
# Example automatically generated from non-compiling source. May contain errors.
jks = JenkinsEC2(stack, "superJks",
    vpc=Vpc.from_lookup(stack, "defaultVPC", is_default=True),
    loadbalancer_type=ELBtype.NLB,
    domain={
        "acm": Certificate.from_certificate_arn(stack, "cert", "arn:aws:xxx"),
        "hosted_zone_id": "xxx",
        "zone_name": "bbb.ccc",
        "record_name": "aaa"
    }
)
```

Note: Jenkins initial admin password has been written to `/home/ec2-user/jenkins-data/secrets/initialAdminPassword`. You can access EC2 instance using [ssm tool](https://docs.aws.amazon.com/systems-manager/latest/userguide/session-manager-working-with-sessions-start.html).

```
aws ssm start-session --target instance-id
```
