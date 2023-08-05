<!--
Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
SPDX-License-Identifier: Apache-2.0
-->

# cdk-nag

| Language   | cdk-nag                                                                                   | monocdk-nag                                                                                       |
| ---------- | ----------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------- |
| Python     | [![PyPI version](https://badge.fury.io/py/cdk-nag.svg)](https://badge.fury.io/py/cdk-nag) | [![PyPI version](https://badge.fury.io/py/monocdk-nag.svg)](https://badge.fury.io/py/monocdk-nag) |
| TypeScript | [![npm version](https://badge.fury.io/js/cdk-nag.svg)](https://badge.fury.io/js/cdk-nag)  | [![npm version](https://badge.fury.io/js/monocdk-nag.svg)](https://badge.fury.io/js/monocdk-nag)  |

Check CDK applications for best practices using a combination of available rule packs. Inspired by [cfn_nag](https://github.com/stelligent/cfn_nag)

![](cdk_nag.gif)

## Available Packs

See [RULES](./RULES.md) for more information on all the available packs.

1. [AWS Solutions](./RULES.md#awssolutions)
2. [NIST 800-53](./RULES.md#nist-800-53) (In Progress)

## Usage

### cdk

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
from aws_cdk.core import App, Aspects
from ...lib.cdk_test_stack import CdkTestStack
from cdk_nag import AwsSolutionsChecks

app = App()
CdkTestStack(app, "CdkNagDemo")
# Simple rule informational messages
Aspects.of(app).add(AwsSolutionsChecks())
```

### monocdk

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
from monocdk import App, Aspects
from monocdk_nag import AwsSolutionsChecks
from ...lib.my_stack import MyStack

app = App()
CdkTestStack(app, "CdkNagDemo")
# Simple rule informational messages
Aspects.of(app).add(AwsSolutionsChecks())
```

## Suppressing a Rule

<details>
  <summary>Example 1) Default Construct</summary>

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
test = SecurityGroup(self, "test",
    vpc=Vpc(self, "vpc")
)
test.add_ingress_rule(Peer.any_ipv4(), Port.all_traffic())
test_cfn = test.node.default_child
test_cfn.add_metadata("cdk_nag",
    rules_to_suppress=[{"id": "AwsSolutions-EC23", "reason": "at least 10 characters"}
    ]
)
```

</details><details>
  <summary>Example 2) Dependent Constructs</summary>

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
user = User(self, "rUser")
user.add_to_policy(
    PolicyStatement(
        actions=["s3:PutObject"],
        resources=[Bucket(self, "rBucket").arn_for_objects("*")]
    ))
cfn_user = user.node.children
for child in cfn_user:
    resource = child.node.default_child
    if resource != undefined && resource.cfn_resource_type == "AWS::IAM::Policy":
        resource.add_metadata("cdk_nag",
            rules_to_suppress=[{
                "id": "AwsSolutions-IAM5",
                "reason": "The user is allowed to put objects on all prefixes in the specified bucket."
            }
            ]
        )
```

</details>

## Rules and Property Overrides

In some cases L2 Constructs do not have a native option to remediate an issue and must be fixed via [Raw Overrides](https://docs.aws.amazon.com/cdk/latest/guide/cfn_layer.html#cfn_layer_raw). Since raw overrides take place after template synthesis these fixes are not caught by the cdk_nag. In this case you should remediate the issue and suppress the issue like in the following example.

<details>
  <summary>Example) Property Overrides</summary>

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
instance = Instance(stack, "rInstance",
    vpc=Vpc(stack, "rVpc"),
    instance_type=InstanceType(InstanceClass.T3),
    machine_image=MachineImage.latest_amazon_linux()
)
cfn_ins = instance.node.default_child
cfn_ins.add_property_override("DisableApiTermination", True)
cfn_ins.add_metadata("cdk_nag",
    rules_to_suppress=[{
        "id": "AwsSolutions-EC29",
        "reason": "Remediated through property override "
    }
    ]
)
```

</details>

## Contributing

See [CONTRIBUTING](./CONTRIBUTING.md) for more information.

## License

This project is licensed under the Apache-2.0 License.
