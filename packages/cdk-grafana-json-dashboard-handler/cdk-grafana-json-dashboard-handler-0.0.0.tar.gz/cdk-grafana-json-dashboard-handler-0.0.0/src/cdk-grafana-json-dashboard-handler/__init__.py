'''
# cdk-grafana-json-dashboard-handler

A handler Custom Construct for JSON Grafana Dashboards - Deploy to Grafana using AWSCDK.

## How it works

Declare the package as a dependency and import the Construct in your stack. Point it to your local Grafana dashboard file so the Construct can calculate an MD5 hash of it. This is needed as otherwise CloudFormation would not know when to redeploy your dashboard to Grafana when it changes. Upload your dashboard file in your CDK stack (s3assets, see example below), and pass the bucket and s3 file path to the Construct as well. Also, give the Construct a secret to resolve from SecretsManager in order to authenticate to your Grafana installation, in combination with the url where to find it. Finally give it a name so it can name your dashboard accordingly. Deploy!

## Contents of the Custom Construct

The Construct contains a Lambda Singleton function, which gets wrapped by a CloudFormation Custom Resource.

## Before using consider the following

1. This construct is geared towards deploying json dashboards. This construct does not cater towards DSL for creating and developing Grafana Dashboards. The construct assumes you will place this json dashboard somewhere in S3. Consider deploying it using `new s3assets.BucketDeployment` and then pass the object path & bucket name to the construct so it knows where to fetch it.
2. This construct assumes Bearer authorization, in which the value of Bearer is stored in AWS Secretsmanager, either plain or in an object for which you can specify the key, e.g. `'password'` or `{'pass' : 'password'}`
3. This construct currently does NOT support custom KMS encrypted files in s3 (see roadmap below)

## Grafana Handler

Implement as following:

Write your Grafana Dashboard JSON file somewhere to disk.

Use that Dashboard JSON in your stack as follows:

```python
# Example automatically generated from non-compiling source. May contain errors.
# setup the dependencies for the construct, for example like this
bucket = s3.Bucket(self, "pogg",
    auto_delete_objects=True,
    removal_policy=cdk.RemovalPolicy.DESTROY
)

fdp = s3assets.BucketDeployment(self, "pogu",
    sources=[s3assets.Source.asset("test/dashboard")],
    destination_bucket=bucket,
    destination_key_prefix="test/test"
)

secret = sm.Secret.from_secret_partial_arn(self, "smLookup",
    get_required_env_variable("GRAFANA_SECRET_PARTIAL_ARN"))
```

```python
# Example automatically generated from non-compiling source. May contain errors.
dbr = GrafanaHandler(self, "pog",
    dashboard_app_name="cdkConstructTest",
    grafana_pw_secret=secret,
    grafana_url=get_required_env_variable("GRAFANA_URL"),
    bucket_name=bucket.bucket_name,
    object_key="test/test/dashboard/test-dashboard.json",
    local_file_path="test/dashboard/test-dashboard.json"
)
dbr.node.add_dependency(fdp)
```

If your handler needs to live inside your projects networking tier:

```python
# Example automatically generated from non-compiling source. May contain errors.
dbr = GrafanaHandler(self, "pog",
    dashboard_app_name="cdkConstructTest",
    grafana_pw_secret=secret,
    grafana_url=get_required_env_variable("GRAFANA_URL"),
    bucket_name=bucket.bucket_name,
    object_key="test/test/dashboard/test-dashboard.json",
    local_file_path="test/dashboard/test-dashboard.json",
    vpc=testing_vpc,
    vpc_subnets={
        "subnets": [testing_private_subnet_iD1, testing_private_subnet_iD2, testing_private_subnet_iD3
        ]
    }
)
dbr.node.add_dependency(fdp)
```

## More permissions

Whenever your handler needs more permissions use the `addToRolePolicy` on the properties exposed on the construct:

```python
# Example automatically generated from non-compiling source. May contain errors.
dbr = GrafanaHandler(self, "pog",
    dashboard_app_name="cdkConstructTest",
    grafana_pw=process.env.pw,  # pass in a string value. CDK supports resolving to string values from SSM and SecretsManager
    grafana_url=process.env.url,
    path_to_file="../src/test/test-dashboard.json",
    local_file_path="test/dashboard/test-dashboard.json"
)

dbr.grafana_handler_function.add_to_role_policy(
    iam.PolicyStatement(
        actions=["ec2:*"],
        resources=["*"]
    ))
```

## Example deployment

![Design](docs/example.jpeg)

## TODO / Roadmap

1. Add custom KMS key support for the dashboard files in s3.
2. Reduce SecretsManager permissions
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

import aws_cdk.aws_ec2
import aws_cdk.aws_kms
import aws_cdk.aws_lambda
import aws_cdk.aws_secretsmanager
import aws_cdk.core


class GrafanaHandler(
    aws_cdk.core.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-grafana-json-dashboard-handler.GrafanaHandler",
):
    def __init__(
        self,
        scope: aws_cdk.core.Construct,
        id: builtins.str,
        *,
        bucket_name: builtins.str,
        dashboard_app_name: builtins.str,
        grafana_pw_secret: aws_cdk.aws_secretsmanager.ISecret,
        grafana_url: builtins.str,
        local_file_path: builtins.str,
        object_key: builtins.str,
        grafana_pw_secret_key: typing.Optional[builtins.str] = None,
        kms_key: typing.Optional[aws_cdk.aws_kms.IKey] = None,
        timeout: typing.Optional[aws_cdk.core.Duration] = None,
        vpc: typing.Optional[aws_cdk.aws_ec2.IVpc] = None,
        vpc_subnets: typing.Optional[aws_cdk.aws_ec2.SubnetSelection] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param bucket_name: The name of the S3 bucket containing your dashboard file.
        :param dashboard_app_name: A unique identifier to identify this dashboard in Grafana. This identifier is used to set or overwrite the title, id and uid keys in the dashboard json file The identifier should be unique!
        :param grafana_pw_secret: The secret in SecretsManager containing your Grafana password. If needed, specify an optional grafanaPwSecretKey to fetch a value for a specific JSON key in the Secret value.
        :param grafana_url: 
        :param local_file_path: The path to your local dashboard file. Give it in so the Construct can calculate an MD5 hash of it. This is needed as otherwise CloudFormation would not know when to redeploy your dashboard to Grafana when it changes.
        :param object_key: The object key in where you stored your dashboard file under.
        :param grafana_pw_secret_key: The optional key to be looked up from your Grafana password secret in Secretsmanager.
        :param kms_key: 
        :param timeout: 
        :param vpc: 
        :param vpc_subnets: 
        '''
        props = GrafanaHandlerProps(
            bucket_name=bucket_name,
            dashboard_app_name=dashboard_app_name,
            grafana_pw_secret=grafana_pw_secret,
            grafana_url=grafana_url,
            local_file_path=local_file_path,
            object_key=object_key,
            grafana_pw_secret_key=grafana_pw_secret_key,
            kms_key=kms_key,
            timeout=timeout,
            vpc=vpc,
            vpc_subnets=vpc_subnets,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="grafanaFunctionCRHandler")
    def grafana_function_cr_handler(self) -> aws_cdk.core.CustomResource:
        return typing.cast(aws_cdk.core.CustomResource, jsii.get(self, "grafanaFunctionCRHandler"))

    @builtins.property # type: ignore[misc]
    @jsii.member(jsii_name="grafanaHandlerFunction")
    def grafana_handler_function(self) -> aws_cdk.aws_lambda.SingletonFunction:
        return typing.cast(aws_cdk.aws_lambda.SingletonFunction, jsii.get(self, "grafanaHandlerFunction"))


@jsii.data_type(
    jsii_type="cdk-grafana-json-dashboard-handler.GrafanaHandlerProps",
    jsii_struct_bases=[],
    name_mapping={
        "bucket_name": "bucketName",
        "dashboard_app_name": "dashboardAppName",
        "grafana_pw_secret": "grafanaPwSecret",
        "grafana_url": "grafanaUrl",
        "local_file_path": "localFilePath",
        "object_key": "objectKey",
        "grafana_pw_secret_key": "grafanaPwSecretKey",
        "kms_key": "kmsKey",
        "timeout": "timeout",
        "vpc": "vpc",
        "vpc_subnets": "vpcSubnets",
    },
)
class GrafanaHandlerProps:
    def __init__(
        self,
        *,
        bucket_name: builtins.str,
        dashboard_app_name: builtins.str,
        grafana_pw_secret: aws_cdk.aws_secretsmanager.ISecret,
        grafana_url: builtins.str,
        local_file_path: builtins.str,
        object_key: builtins.str,
        grafana_pw_secret_key: typing.Optional[builtins.str] = None,
        kms_key: typing.Optional[aws_cdk.aws_kms.IKey] = None,
        timeout: typing.Optional[aws_cdk.core.Duration] = None,
        vpc: typing.Optional[aws_cdk.aws_ec2.IVpc] = None,
        vpc_subnets: typing.Optional[aws_cdk.aws_ec2.SubnetSelection] = None,
    ) -> None:
        '''Properties for a newly created Grafana Handler Construct.

        A valid Grafana dashboard JSON has an uid, id and title key in the root of the object.
        We generate these based on input so static JSON files are not a problem when wanting to deploy more dynamic
        but the end result is still deterministic. This is all derived from the dashboardAppName property

        :param bucket_name: The name of the S3 bucket containing your dashboard file.
        :param dashboard_app_name: A unique identifier to identify this dashboard in Grafana. This identifier is used to set or overwrite the title, id and uid keys in the dashboard json file The identifier should be unique!
        :param grafana_pw_secret: The secret in SecretsManager containing your Grafana password. If needed, specify an optional grafanaPwSecretKey to fetch a value for a specific JSON key in the Secret value.
        :param grafana_url: 
        :param local_file_path: The path to your local dashboard file. Give it in so the Construct can calculate an MD5 hash of it. This is needed as otherwise CloudFormation would not know when to redeploy your dashboard to Grafana when it changes.
        :param object_key: The object key in where you stored your dashboard file under.
        :param grafana_pw_secret_key: The optional key to be looked up from your Grafana password secret in Secretsmanager.
        :param kms_key: 
        :param timeout: 
        :param vpc: 
        :param vpc_subnets: 
        '''
        if isinstance(vpc_subnets, dict):
            vpc_subnets = aws_cdk.aws_ec2.SubnetSelection(**vpc_subnets)
        self._values: typing.Dict[str, typing.Any] = {
            "bucket_name": bucket_name,
            "dashboard_app_name": dashboard_app_name,
            "grafana_pw_secret": grafana_pw_secret,
            "grafana_url": grafana_url,
            "local_file_path": local_file_path,
            "object_key": object_key,
        }
        if grafana_pw_secret_key is not None:
            self._values["grafana_pw_secret_key"] = grafana_pw_secret_key
        if kms_key is not None:
            self._values["kms_key"] = kms_key
        if timeout is not None:
            self._values["timeout"] = timeout
        if vpc is not None:
            self._values["vpc"] = vpc
        if vpc_subnets is not None:
            self._values["vpc_subnets"] = vpc_subnets

    @builtins.property
    def bucket_name(self) -> builtins.str:
        '''The name of the S3 bucket containing your dashboard file.'''
        result = self._values.get("bucket_name")
        assert result is not None, "Required property 'bucket_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def dashboard_app_name(self) -> builtins.str:
        '''A unique identifier to identify this dashboard in Grafana.

        This identifier is used to set or overwrite the title, id and uid keys in the dashboard json file
        The identifier should be unique!
        '''
        result = self._values.get("dashboard_app_name")
        assert result is not None, "Required property 'dashboard_app_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def grafana_pw_secret(self) -> aws_cdk.aws_secretsmanager.ISecret:
        '''The secret in SecretsManager containing your Grafana password.

        If needed, specify an optional grafanaPwSecretKey to fetch a value for a specific JSON key in the Secret value.
        '''
        result = self._values.get("grafana_pw_secret")
        assert result is not None, "Required property 'grafana_pw_secret' is missing"
        return typing.cast(aws_cdk.aws_secretsmanager.ISecret, result)

    @builtins.property
    def grafana_url(self) -> builtins.str:
        result = self._values.get("grafana_url")
        assert result is not None, "Required property 'grafana_url' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def local_file_path(self) -> builtins.str:
        '''The path to your local dashboard file.

        Give it in so the Construct can calculate an MD5 hash of it. This is needed as otherwise CloudFormation would not know when to redeploy your dashboard to Grafana when it changes.
        '''
        result = self._values.get("local_file_path")
        assert result is not None, "Required property 'local_file_path' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def object_key(self) -> builtins.str:
        '''The object key in where you stored your dashboard file under.'''
        result = self._values.get("object_key")
        assert result is not None, "Required property 'object_key' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def grafana_pw_secret_key(self) -> typing.Optional[builtins.str]:
        '''The optional key to be looked up from your Grafana password secret in Secretsmanager.'''
        result = self._values.get("grafana_pw_secret_key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def kms_key(self) -> typing.Optional[aws_cdk.aws_kms.IKey]:
        result = self._values.get("kms_key")
        return typing.cast(typing.Optional[aws_cdk.aws_kms.IKey], result)

    @builtins.property
    def timeout(self) -> typing.Optional[aws_cdk.core.Duration]:
        result = self._values.get("timeout")
        return typing.cast(typing.Optional[aws_cdk.core.Duration], result)

    @builtins.property
    def vpc(self) -> typing.Optional[aws_cdk.aws_ec2.IVpc]:
        result = self._values.get("vpc")
        return typing.cast(typing.Optional[aws_cdk.aws_ec2.IVpc], result)

    @builtins.property
    def vpc_subnets(self) -> typing.Optional[aws_cdk.aws_ec2.SubnetSelection]:
        result = self._values.get("vpc_subnets")
        return typing.cast(typing.Optional[aws_cdk.aws_ec2.SubnetSelection], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GrafanaHandlerProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "GrafanaHandler",
    "GrafanaHandlerProps",
]

publication.publish()
