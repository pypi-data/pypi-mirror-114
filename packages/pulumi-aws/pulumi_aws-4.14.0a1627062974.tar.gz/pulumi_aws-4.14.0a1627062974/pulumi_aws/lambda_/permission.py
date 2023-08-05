# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities

__all__ = ['PermissionArgs', 'Permission']

@pulumi.input_type
class PermissionArgs:
    def __init__(__self__, *,
                 action: pulumi.Input[str],
                 function: pulumi.Input[str],
                 principal: pulumi.Input[str],
                 event_source_token: Optional[pulumi.Input[str]] = None,
                 qualifier: Optional[pulumi.Input[str]] = None,
                 source_account: Optional[pulumi.Input[str]] = None,
                 source_arn: Optional[pulumi.Input[str]] = None,
                 statement_id: Optional[pulumi.Input[str]] = None,
                 statement_id_prefix: Optional[pulumi.Input[str]] = None):
        """
        The set of arguments for constructing a Permission resource.
        :param pulumi.Input[str] action: The AWS Lambda action you want to allow in this statement. (e.g. `lambda:InvokeFunction`)
        :param pulumi.Input[str] function: Name of the Lambda function whose resource policy you are updating
        :param pulumi.Input[str] principal: The principal who is getting this permission. e.g. `s3.amazonaws.com`, an AWS account ID, or any valid AWS service principal such as `events.amazonaws.com` or `sns.amazonaws.com`.
        :param pulumi.Input[str] event_source_token: The Event Source Token to validate.  Used with [Alexa Skills](https://developer.amazon.com/docs/custom-skills/host-a-custom-skill-as-an-aws-lambda-function.html#use-aws-cli).
        :param pulumi.Input[str] qualifier: Query parameter to specify function version or alias name. The permission will then apply to the specific qualified ARN. e.g. `arn:aws:lambda:aws-region:acct-id:function:function-name:2`
        :param pulumi.Input[str] source_account: This parameter is used for S3 and SES. The AWS account ID (without a hyphen) of the source owner.
        :param pulumi.Input[str] source_arn: When the principal is an AWS service, the ARN of the specific resource within that service to grant permission to.
               Without this, any resource from `principal` will be granted permission – even if that resource is from another account.
               For S3, this should be the ARN of the S3 Bucket.
               For CloudWatch Events, this should be the ARN of the CloudWatch Events Rule.
               For API Gateway, this should be the ARN of the API, as described [here](https://docs.aws.amazon.com/apigateway/latest/developerguide/api-gateway-control-access-using-iam-policies-to-invoke-api.html).
        :param pulumi.Input[str] statement_id: A unique statement identifier. By default generated by this provider.
        :param pulumi.Input[str] statement_id_prefix: A statement identifier prefix. This provider will generate a unique suffix. Conflicts with `statement_id`.
        """
        pulumi.set(__self__, "action", action)
        pulumi.set(__self__, "function", function)
        pulumi.set(__self__, "principal", principal)
        if event_source_token is not None:
            pulumi.set(__self__, "event_source_token", event_source_token)
        if qualifier is not None:
            pulumi.set(__self__, "qualifier", qualifier)
        if source_account is not None:
            pulumi.set(__self__, "source_account", source_account)
        if source_arn is not None:
            pulumi.set(__self__, "source_arn", source_arn)
        if statement_id is not None:
            pulumi.set(__self__, "statement_id", statement_id)
        if statement_id_prefix is not None:
            pulumi.set(__self__, "statement_id_prefix", statement_id_prefix)

    @property
    @pulumi.getter
    def action(self) -> pulumi.Input[str]:
        """
        The AWS Lambda action you want to allow in this statement. (e.g. `lambda:InvokeFunction`)
        """
        return pulumi.get(self, "action")

    @action.setter
    def action(self, value: pulumi.Input[str]):
        pulumi.set(self, "action", value)

    @property
    @pulumi.getter
    def function(self) -> pulumi.Input[str]:
        """
        Name of the Lambda function whose resource policy you are updating
        """
        return pulumi.get(self, "function")

    @function.setter
    def function(self, value: pulumi.Input[str]):
        pulumi.set(self, "function", value)

    @property
    @pulumi.getter
    def principal(self) -> pulumi.Input[str]:
        """
        The principal who is getting this permission. e.g. `s3.amazonaws.com`, an AWS account ID, or any valid AWS service principal such as `events.amazonaws.com` or `sns.amazonaws.com`.
        """
        return pulumi.get(self, "principal")

    @principal.setter
    def principal(self, value: pulumi.Input[str]):
        pulumi.set(self, "principal", value)

    @property
    @pulumi.getter(name="eventSourceToken")
    def event_source_token(self) -> Optional[pulumi.Input[str]]:
        """
        The Event Source Token to validate.  Used with [Alexa Skills](https://developer.amazon.com/docs/custom-skills/host-a-custom-skill-as-an-aws-lambda-function.html#use-aws-cli).
        """
        return pulumi.get(self, "event_source_token")

    @event_source_token.setter
    def event_source_token(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "event_source_token", value)

    @property
    @pulumi.getter
    def qualifier(self) -> Optional[pulumi.Input[str]]:
        """
        Query parameter to specify function version or alias name. The permission will then apply to the specific qualified ARN. e.g. `arn:aws:lambda:aws-region:acct-id:function:function-name:2`
        """
        return pulumi.get(self, "qualifier")

    @qualifier.setter
    def qualifier(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "qualifier", value)

    @property
    @pulumi.getter(name="sourceAccount")
    def source_account(self) -> Optional[pulumi.Input[str]]:
        """
        This parameter is used for S3 and SES. The AWS account ID (without a hyphen) of the source owner.
        """
        return pulumi.get(self, "source_account")

    @source_account.setter
    def source_account(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "source_account", value)

    @property
    @pulumi.getter(name="sourceArn")
    def source_arn(self) -> Optional[pulumi.Input[str]]:
        """
        When the principal is an AWS service, the ARN of the specific resource within that service to grant permission to.
        Without this, any resource from `principal` will be granted permission – even if that resource is from another account.
        For S3, this should be the ARN of the S3 Bucket.
        For CloudWatch Events, this should be the ARN of the CloudWatch Events Rule.
        For API Gateway, this should be the ARN of the API, as described [here](https://docs.aws.amazon.com/apigateway/latest/developerguide/api-gateway-control-access-using-iam-policies-to-invoke-api.html).
        """
        return pulumi.get(self, "source_arn")

    @source_arn.setter
    def source_arn(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "source_arn", value)

    @property
    @pulumi.getter(name="statementId")
    def statement_id(self) -> Optional[pulumi.Input[str]]:
        """
        A unique statement identifier. By default generated by this provider.
        """
        return pulumi.get(self, "statement_id")

    @statement_id.setter
    def statement_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "statement_id", value)

    @property
    @pulumi.getter(name="statementIdPrefix")
    def statement_id_prefix(self) -> Optional[pulumi.Input[str]]:
        """
        A statement identifier prefix. This provider will generate a unique suffix. Conflicts with `statement_id`.
        """
        return pulumi.get(self, "statement_id_prefix")

    @statement_id_prefix.setter
    def statement_id_prefix(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "statement_id_prefix", value)


@pulumi.input_type
class _PermissionState:
    def __init__(__self__, *,
                 action: Optional[pulumi.Input[str]] = None,
                 event_source_token: Optional[pulumi.Input[str]] = None,
                 function: Optional[pulumi.Input[str]] = None,
                 principal: Optional[pulumi.Input[str]] = None,
                 qualifier: Optional[pulumi.Input[str]] = None,
                 source_account: Optional[pulumi.Input[str]] = None,
                 source_arn: Optional[pulumi.Input[str]] = None,
                 statement_id: Optional[pulumi.Input[str]] = None,
                 statement_id_prefix: Optional[pulumi.Input[str]] = None):
        """
        Input properties used for looking up and filtering Permission resources.
        :param pulumi.Input[str] action: The AWS Lambda action you want to allow in this statement. (e.g. `lambda:InvokeFunction`)
        :param pulumi.Input[str] event_source_token: The Event Source Token to validate.  Used with [Alexa Skills](https://developer.amazon.com/docs/custom-skills/host-a-custom-skill-as-an-aws-lambda-function.html#use-aws-cli).
        :param pulumi.Input[str] function: Name of the Lambda function whose resource policy you are updating
        :param pulumi.Input[str] principal: The principal who is getting this permission. e.g. `s3.amazonaws.com`, an AWS account ID, or any valid AWS service principal such as `events.amazonaws.com` or `sns.amazonaws.com`.
        :param pulumi.Input[str] qualifier: Query parameter to specify function version or alias name. The permission will then apply to the specific qualified ARN. e.g. `arn:aws:lambda:aws-region:acct-id:function:function-name:2`
        :param pulumi.Input[str] source_account: This parameter is used for S3 and SES. The AWS account ID (without a hyphen) of the source owner.
        :param pulumi.Input[str] source_arn: When the principal is an AWS service, the ARN of the specific resource within that service to grant permission to.
               Without this, any resource from `principal` will be granted permission – even if that resource is from another account.
               For S3, this should be the ARN of the S3 Bucket.
               For CloudWatch Events, this should be the ARN of the CloudWatch Events Rule.
               For API Gateway, this should be the ARN of the API, as described [here](https://docs.aws.amazon.com/apigateway/latest/developerguide/api-gateway-control-access-using-iam-policies-to-invoke-api.html).
        :param pulumi.Input[str] statement_id: A unique statement identifier. By default generated by this provider.
        :param pulumi.Input[str] statement_id_prefix: A statement identifier prefix. This provider will generate a unique suffix. Conflicts with `statement_id`.
        """
        if action is not None:
            pulumi.set(__self__, "action", action)
        if event_source_token is not None:
            pulumi.set(__self__, "event_source_token", event_source_token)
        if function is not None:
            pulumi.set(__self__, "function", function)
        if principal is not None:
            pulumi.set(__self__, "principal", principal)
        if qualifier is not None:
            pulumi.set(__self__, "qualifier", qualifier)
        if source_account is not None:
            pulumi.set(__self__, "source_account", source_account)
        if source_arn is not None:
            pulumi.set(__self__, "source_arn", source_arn)
        if statement_id is not None:
            pulumi.set(__self__, "statement_id", statement_id)
        if statement_id_prefix is not None:
            pulumi.set(__self__, "statement_id_prefix", statement_id_prefix)

    @property
    @pulumi.getter
    def action(self) -> Optional[pulumi.Input[str]]:
        """
        The AWS Lambda action you want to allow in this statement. (e.g. `lambda:InvokeFunction`)
        """
        return pulumi.get(self, "action")

    @action.setter
    def action(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "action", value)

    @property
    @pulumi.getter(name="eventSourceToken")
    def event_source_token(self) -> Optional[pulumi.Input[str]]:
        """
        The Event Source Token to validate.  Used with [Alexa Skills](https://developer.amazon.com/docs/custom-skills/host-a-custom-skill-as-an-aws-lambda-function.html#use-aws-cli).
        """
        return pulumi.get(self, "event_source_token")

    @event_source_token.setter
    def event_source_token(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "event_source_token", value)

    @property
    @pulumi.getter
    def function(self) -> Optional[pulumi.Input[str]]:
        """
        Name of the Lambda function whose resource policy you are updating
        """
        return pulumi.get(self, "function")

    @function.setter
    def function(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "function", value)

    @property
    @pulumi.getter
    def principal(self) -> Optional[pulumi.Input[str]]:
        """
        The principal who is getting this permission. e.g. `s3.amazonaws.com`, an AWS account ID, or any valid AWS service principal such as `events.amazonaws.com` or `sns.amazonaws.com`.
        """
        return pulumi.get(self, "principal")

    @principal.setter
    def principal(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "principal", value)

    @property
    @pulumi.getter
    def qualifier(self) -> Optional[pulumi.Input[str]]:
        """
        Query parameter to specify function version or alias name. The permission will then apply to the specific qualified ARN. e.g. `arn:aws:lambda:aws-region:acct-id:function:function-name:2`
        """
        return pulumi.get(self, "qualifier")

    @qualifier.setter
    def qualifier(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "qualifier", value)

    @property
    @pulumi.getter(name="sourceAccount")
    def source_account(self) -> Optional[pulumi.Input[str]]:
        """
        This parameter is used for S3 and SES. The AWS account ID (without a hyphen) of the source owner.
        """
        return pulumi.get(self, "source_account")

    @source_account.setter
    def source_account(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "source_account", value)

    @property
    @pulumi.getter(name="sourceArn")
    def source_arn(self) -> Optional[pulumi.Input[str]]:
        """
        When the principal is an AWS service, the ARN of the specific resource within that service to grant permission to.
        Without this, any resource from `principal` will be granted permission – even if that resource is from another account.
        For S3, this should be the ARN of the S3 Bucket.
        For CloudWatch Events, this should be the ARN of the CloudWatch Events Rule.
        For API Gateway, this should be the ARN of the API, as described [here](https://docs.aws.amazon.com/apigateway/latest/developerguide/api-gateway-control-access-using-iam-policies-to-invoke-api.html).
        """
        return pulumi.get(self, "source_arn")

    @source_arn.setter
    def source_arn(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "source_arn", value)

    @property
    @pulumi.getter(name="statementId")
    def statement_id(self) -> Optional[pulumi.Input[str]]:
        """
        A unique statement identifier. By default generated by this provider.
        """
        return pulumi.get(self, "statement_id")

    @statement_id.setter
    def statement_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "statement_id", value)

    @property
    @pulumi.getter(name="statementIdPrefix")
    def statement_id_prefix(self) -> Optional[pulumi.Input[str]]:
        """
        A statement identifier prefix. This provider will generate a unique suffix. Conflicts with `statement_id`.
        """
        return pulumi.get(self, "statement_id_prefix")

    @statement_id_prefix.setter
    def statement_id_prefix(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "statement_id_prefix", value)


class Permission(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 action: Optional[pulumi.Input[str]] = None,
                 event_source_token: Optional[pulumi.Input[str]] = None,
                 function: Optional[pulumi.Input[str]] = None,
                 principal: Optional[pulumi.Input[str]] = None,
                 qualifier: Optional[pulumi.Input[str]] = None,
                 source_account: Optional[pulumi.Input[str]] = None,
                 source_arn: Optional[pulumi.Input[str]] = None,
                 statement_id: Optional[pulumi.Input[str]] = None,
                 statement_id_prefix: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        Gives an external source (like a CloudWatch Event Rule, SNS, or S3) permission to access the Lambda function.

        ## Example Usage
        ### Basic Example

        ```python
        import pulumi
        import json
        import pulumi_aws as aws

        iam_for_lambda = aws.iam.Role("iamForLambda", assume_role_policy=json.dumps({
            "Version": "2012-10-17",
            "Statement": [{
                "Action": "sts:AssumeRole",
                "Effect": "Allow",
                "Sid": "",
                "Principal": {
                    "Service": "lambda.amazonaws.com",
                },
            }],
        }))
        test_lambda = aws.lambda_.Function("testLambda",
            code=pulumi.FileArchive("lambdatest.zip"),
            role=iam_for_lambda.arn,
            handler="exports.handler",
            runtime="nodejs12.x")
        test_alias = aws.lambda_.Alias("testAlias",
            description="a sample description",
            function_name=test_lambda.name,
            function_version="$LATEST")
        allow_cloudwatch = aws.lambda_.Permission("allowCloudwatch",
            action="lambda:InvokeFunction",
            function=test_lambda.name,
            principal="events.amazonaws.com",
            source_arn="arn:aws:events:eu-west-1:111122223333:rule/RunDaily",
            qualifier=test_alias.name)
        ```
        ### Usage with SNS

        ```python
        import pulumi
        import json
        import pulumi_aws as aws

        default_topic = aws.sns.Topic("defaultTopic")
        default_role = aws.iam.Role("defaultRole", assume_role_policy=json.dumps({
            "Version": "2012-10-17",
            "Statement": [{
                "Action": "sts:AssumeRole",
                "Effect": "Allow",
                "Sid": "",
                "Principal": {
                    "Service": "lambda.amazonaws.com",
                },
            }],
        }))
        func = aws.lambda_.Function("func",
            code=pulumi.FileArchive("lambdatest.zip"),
            role=default_role.arn,
            handler="exports.handler",
            runtime="python2.7")
        with_sns = aws.lambda_.Permission("withSns",
            action="lambda:InvokeFunction",
            function=func.name,
            principal="sns.amazonaws.com",
            source_arn=default_topic.arn)
        lambda_ = aws.sns.TopicSubscription("lambda",
            topic=default_topic.arn,
            protocol="lambda",
            endpoint=func.arn)
        ```
        ### Specify Lambda permissions for API Gateway REST API

        ```python
        import pulumi
        import pulumi_aws as aws

        my_demo_api = aws.apigateway.RestApi("myDemoAPI", description="This is my API for demonstration purposes")
        lambda_permission = aws.lambda_.Permission("lambdaPermission",
            action="lambda:InvokeFunction",
            function="MyDemoFunction",
            principal="apigateway.amazonaws.com",
            source_arn=my_demo_api.execution_arn.apply(lambda execution_arn: f"{execution_arn}/*/*/*"))
        ```
        ## Usage with CloudWatch log group

        ```python
        import pulumi
        import pulumi_aws as aws

        default_log_group = aws.cloudwatch.LogGroup("defaultLogGroup")
        default_role = aws.iam.Role("defaultRole", assume_role_policy=\"\"\"{
          "Version": "2012-10-17",
          "Statement": [
            {
              "Action": "sts:AssumeRole",
              "Principal": {
                "Service": "lambda.amazonaws.com"
              },
              "Effect": "Allow",
              "Sid": ""
            }
          ]
        }
        \"\"\")
        logging_function = aws.lambda_.Function("loggingFunction",
            code=pulumi.FileArchive("lamba_logging.zip"),
            handler="exports.handler",
            role=default_role.arn,
            runtime="python2.7")
        logging_permission = aws.lambda_.Permission("loggingPermission",
            action="lambda:InvokeFunction",
            function=logging_function.name,
            principal="logs.eu-west-1.amazonaws.com",
            source_arn=default_log_group.arn.apply(lambda arn: f"{arn}:*"))
        logging_log_subscription_filter = aws.cloudwatch.LogSubscriptionFilter("loggingLogSubscriptionFilter",
            destination_arn=logging_function.arn,
            filter_pattern="",
            log_group=default_log_group.name,
            opts=pulumi.ResourceOptions(depends_on=[logging_permission]))
        ```

        ## Import

        Lambda permission statements can be imported using function_name/statement_id, with an optional qualifier, e.g.

        ```sh
         $ pulumi import aws:lambda/permission:Permission test_lambda_permission my_test_lambda_function/AllowExecutionFromCloudWatch
        ```

        ```sh
         $ pulumi import aws:lambda/permission:Permission test_lambda_permission my_test_lambda_function:qualifier_name/AllowExecutionFromCloudWatch
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] action: The AWS Lambda action you want to allow in this statement. (e.g. `lambda:InvokeFunction`)
        :param pulumi.Input[str] event_source_token: The Event Source Token to validate.  Used with [Alexa Skills](https://developer.amazon.com/docs/custom-skills/host-a-custom-skill-as-an-aws-lambda-function.html#use-aws-cli).
        :param pulumi.Input[str] function: Name of the Lambda function whose resource policy you are updating
        :param pulumi.Input[str] principal: The principal who is getting this permission. e.g. `s3.amazonaws.com`, an AWS account ID, or any valid AWS service principal such as `events.amazonaws.com` or `sns.amazonaws.com`.
        :param pulumi.Input[str] qualifier: Query parameter to specify function version or alias name. The permission will then apply to the specific qualified ARN. e.g. `arn:aws:lambda:aws-region:acct-id:function:function-name:2`
        :param pulumi.Input[str] source_account: This parameter is used for S3 and SES. The AWS account ID (without a hyphen) of the source owner.
        :param pulumi.Input[str] source_arn: When the principal is an AWS service, the ARN of the specific resource within that service to grant permission to.
               Without this, any resource from `principal` will be granted permission – even if that resource is from another account.
               For S3, this should be the ARN of the S3 Bucket.
               For CloudWatch Events, this should be the ARN of the CloudWatch Events Rule.
               For API Gateway, this should be the ARN of the API, as described [here](https://docs.aws.amazon.com/apigateway/latest/developerguide/api-gateway-control-access-using-iam-policies-to-invoke-api.html).
        :param pulumi.Input[str] statement_id: A unique statement identifier. By default generated by this provider.
        :param pulumi.Input[str] statement_id_prefix: A statement identifier prefix. This provider will generate a unique suffix. Conflicts with `statement_id`.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: PermissionArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Gives an external source (like a CloudWatch Event Rule, SNS, or S3) permission to access the Lambda function.

        ## Example Usage
        ### Basic Example

        ```python
        import pulumi
        import json
        import pulumi_aws as aws

        iam_for_lambda = aws.iam.Role("iamForLambda", assume_role_policy=json.dumps({
            "Version": "2012-10-17",
            "Statement": [{
                "Action": "sts:AssumeRole",
                "Effect": "Allow",
                "Sid": "",
                "Principal": {
                    "Service": "lambda.amazonaws.com",
                },
            }],
        }))
        test_lambda = aws.lambda_.Function("testLambda",
            code=pulumi.FileArchive("lambdatest.zip"),
            role=iam_for_lambda.arn,
            handler="exports.handler",
            runtime="nodejs12.x")
        test_alias = aws.lambda_.Alias("testAlias",
            description="a sample description",
            function_name=test_lambda.name,
            function_version="$LATEST")
        allow_cloudwatch = aws.lambda_.Permission("allowCloudwatch",
            action="lambda:InvokeFunction",
            function=test_lambda.name,
            principal="events.amazonaws.com",
            source_arn="arn:aws:events:eu-west-1:111122223333:rule/RunDaily",
            qualifier=test_alias.name)
        ```
        ### Usage with SNS

        ```python
        import pulumi
        import json
        import pulumi_aws as aws

        default_topic = aws.sns.Topic("defaultTopic")
        default_role = aws.iam.Role("defaultRole", assume_role_policy=json.dumps({
            "Version": "2012-10-17",
            "Statement": [{
                "Action": "sts:AssumeRole",
                "Effect": "Allow",
                "Sid": "",
                "Principal": {
                    "Service": "lambda.amazonaws.com",
                },
            }],
        }))
        func = aws.lambda_.Function("func",
            code=pulumi.FileArchive("lambdatest.zip"),
            role=default_role.arn,
            handler="exports.handler",
            runtime="python2.7")
        with_sns = aws.lambda_.Permission("withSns",
            action="lambda:InvokeFunction",
            function=func.name,
            principal="sns.amazonaws.com",
            source_arn=default_topic.arn)
        lambda_ = aws.sns.TopicSubscription("lambda",
            topic=default_topic.arn,
            protocol="lambda",
            endpoint=func.arn)
        ```
        ### Specify Lambda permissions for API Gateway REST API

        ```python
        import pulumi
        import pulumi_aws as aws

        my_demo_api = aws.apigateway.RestApi("myDemoAPI", description="This is my API for demonstration purposes")
        lambda_permission = aws.lambda_.Permission("lambdaPermission",
            action="lambda:InvokeFunction",
            function="MyDemoFunction",
            principal="apigateway.amazonaws.com",
            source_arn=my_demo_api.execution_arn.apply(lambda execution_arn: f"{execution_arn}/*/*/*"))
        ```
        ## Usage with CloudWatch log group

        ```python
        import pulumi
        import pulumi_aws as aws

        default_log_group = aws.cloudwatch.LogGroup("defaultLogGroup")
        default_role = aws.iam.Role("defaultRole", assume_role_policy=\"\"\"{
          "Version": "2012-10-17",
          "Statement": [
            {
              "Action": "sts:AssumeRole",
              "Principal": {
                "Service": "lambda.amazonaws.com"
              },
              "Effect": "Allow",
              "Sid": ""
            }
          ]
        }
        \"\"\")
        logging_function = aws.lambda_.Function("loggingFunction",
            code=pulumi.FileArchive("lamba_logging.zip"),
            handler="exports.handler",
            role=default_role.arn,
            runtime="python2.7")
        logging_permission = aws.lambda_.Permission("loggingPermission",
            action="lambda:InvokeFunction",
            function=logging_function.name,
            principal="logs.eu-west-1.amazonaws.com",
            source_arn=default_log_group.arn.apply(lambda arn: f"{arn}:*"))
        logging_log_subscription_filter = aws.cloudwatch.LogSubscriptionFilter("loggingLogSubscriptionFilter",
            destination_arn=logging_function.arn,
            filter_pattern="",
            log_group=default_log_group.name,
            opts=pulumi.ResourceOptions(depends_on=[logging_permission]))
        ```

        ## Import

        Lambda permission statements can be imported using function_name/statement_id, with an optional qualifier, e.g.

        ```sh
         $ pulumi import aws:lambda/permission:Permission test_lambda_permission my_test_lambda_function/AllowExecutionFromCloudWatch
        ```

        ```sh
         $ pulumi import aws:lambda/permission:Permission test_lambda_permission my_test_lambda_function:qualifier_name/AllowExecutionFromCloudWatch
        ```

        :param str resource_name: The name of the resource.
        :param PermissionArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(PermissionArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 action: Optional[pulumi.Input[str]] = None,
                 event_source_token: Optional[pulumi.Input[str]] = None,
                 function: Optional[pulumi.Input[str]] = None,
                 principal: Optional[pulumi.Input[str]] = None,
                 qualifier: Optional[pulumi.Input[str]] = None,
                 source_account: Optional[pulumi.Input[str]] = None,
                 source_arn: Optional[pulumi.Input[str]] = None,
                 statement_id: Optional[pulumi.Input[str]] = None,
                 statement_id_prefix: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        if opts is None:
            opts = pulumi.ResourceOptions()
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.version is None:
            opts.version = _utilities.get_version()
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = PermissionArgs.__new__(PermissionArgs)

            if action is None and not opts.urn:
                raise TypeError("Missing required property 'action'")
            __props__.__dict__["action"] = action
            __props__.__dict__["event_source_token"] = event_source_token
            if function is None and not opts.urn:
                raise TypeError("Missing required property 'function'")
            __props__.__dict__["function"] = function
            if principal is None and not opts.urn:
                raise TypeError("Missing required property 'principal'")
            __props__.__dict__["principal"] = principal
            __props__.__dict__["qualifier"] = qualifier
            __props__.__dict__["source_account"] = source_account
            __props__.__dict__["source_arn"] = source_arn
            __props__.__dict__["statement_id"] = statement_id
            __props__.__dict__["statement_id_prefix"] = statement_id_prefix
        super(Permission, __self__).__init__(
            'aws:lambda/permission:Permission',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            action: Optional[pulumi.Input[str]] = None,
            event_source_token: Optional[pulumi.Input[str]] = None,
            function: Optional[pulumi.Input[str]] = None,
            principal: Optional[pulumi.Input[str]] = None,
            qualifier: Optional[pulumi.Input[str]] = None,
            source_account: Optional[pulumi.Input[str]] = None,
            source_arn: Optional[pulumi.Input[str]] = None,
            statement_id: Optional[pulumi.Input[str]] = None,
            statement_id_prefix: Optional[pulumi.Input[str]] = None) -> 'Permission':
        """
        Get an existing Permission resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] action: The AWS Lambda action you want to allow in this statement. (e.g. `lambda:InvokeFunction`)
        :param pulumi.Input[str] event_source_token: The Event Source Token to validate.  Used with [Alexa Skills](https://developer.amazon.com/docs/custom-skills/host-a-custom-skill-as-an-aws-lambda-function.html#use-aws-cli).
        :param pulumi.Input[str] function: Name of the Lambda function whose resource policy you are updating
        :param pulumi.Input[str] principal: The principal who is getting this permission. e.g. `s3.amazonaws.com`, an AWS account ID, or any valid AWS service principal such as `events.amazonaws.com` or `sns.amazonaws.com`.
        :param pulumi.Input[str] qualifier: Query parameter to specify function version or alias name. The permission will then apply to the specific qualified ARN. e.g. `arn:aws:lambda:aws-region:acct-id:function:function-name:2`
        :param pulumi.Input[str] source_account: This parameter is used for S3 and SES. The AWS account ID (without a hyphen) of the source owner.
        :param pulumi.Input[str] source_arn: When the principal is an AWS service, the ARN of the specific resource within that service to grant permission to.
               Without this, any resource from `principal` will be granted permission – even if that resource is from another account.
               For S3, this should be the ARN of the S3 Bucket.
               For CloudWatch Events, this should be the ARN of the CloudWatch Events Rule.
               For API Gateway, this should be the ARN of the API, as described [here](https://docs.aws.amazon.com/apigateway/latest/developerguide/api-gateway-control-access-using-iam-policies-to-invoke-api.html).
        :param pulumi.Input[str] statement_id: A unique statement identifier. By default generated by this provider.
        :param pulumi.Input[str] statement_id_prefix: A statement identifier prefix. This provider will generate a unique suffix. Conflicts with `statement_id`.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _PermissionState.__new__(_PermissionState)

        __props__.__dict__["action"] = action
        __props__.__dict__["event_source_token"] = event_source_token
        __props__.__dict__["function"] = function
        __props__.__dict__["principal"] = principal
        __props__.__dict__["qualifier"] = qualifier
        __props__.__dict__["source_account"] = source_account
        __props__.__dict__["source_arn"] = source_arn
        __props__.__dict__["statement_id"] = statement_id
        __props__.__dict__["statement_id_prefix"] = statement_id_prefix
        return Permission(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def action(self) -> pulumi.Output[str]:
        """
        The AWS Lambda action you want to allow in this statement. (e.g. `lambda:InvokeFunction`)
        """
        return pulumi.get(self, "action")

    @property
    @pulumi.getter(name="eventSourceToken")
    def event_source_token(self) -> pulumi.Output[Optional[str]]:
        """
        The Event Source Token to validate.  Used with [Alexa Skills](https://developer.amazon.com/docs/custom-skills/host-a-custom-skill-as-an-aws-lambda-function.html#use-aws-cli).
        """
        return pulumi.get(self, "event_source_token")

    @property
    @pulumi.getter
    def function(self) -> pulumi.Output[str]:
        """
        Name of the Lambda function whose resource policy you are updating
        """
        return pulumi.get(self, "function")

    @property
    @pulumi.getter
    def principal(self) -> pulumi.Output[str]:
        """
        The principal who is getting this permission. e.g. `s3.amazonaws.com`, an AWS account ID, or any valid AWS service principal such as `events.amazonaws.com` or `sns.amazonaws.com`.
        """
        return pulumi.get(self, "principal")

    @property
    @pulumi.getter
    def qualifier(self) -> pulumi.Output[Optional[str]]:
        """
        Query parameter to specify function version or alias name. The permission will then apply to the specific qualified ARN. e.g. `arn:aws:lambda:aws-region:acct-id:function:function-name:2`
        """
        return pulumi.get(self, "qualifier")

    @property
    @pulumi.getter(name="sourceAccount")
    def source_account(self) -> pulumi.Output[Optional[str]]:
        """
        This parameter is used for S3 and SES. The AWS account ID (without a hyphen) of the source owner.
        """
        return pulumi.get(self, "source_account")

    @property
    @pulumi.getter(name="sourceArn")
    def source_arn(self) -> pulumi.Output[Optional[str]]:
        """
        When the principal is an AWS service, the ARN of the specific resource within that service to grant permission to.
        Without this, any resource from `principal` will be granted permission – even if that resource is from another account.
        For S3, this should be the ARN of the S3 Bucket.
        For CloudWatch Events, this should be the ARN of the CloudWatch Events Rule.
        For API Gateway, this should be the ARN of the API, as described [here](https://docs.aws.amazon.com/apigateway/latest/developerguide/api-gateway-control-access-using-iam-policies-to-invoke-api.html).
        """
        return pulumi.get(self, "source_arn")

    @property
    @pulumi.getter(name="statementId")
    def statement_id(self) -> pulumi.Output[str]:
        """
        A unique statement identifier. By default generated by this provider.
        """
        return pulumi.get(self, "statement_id")

    @property
    @pulumi.getter(name="statementIdPrefix")
    def statement_id_prefix(self) -> pulumi.Output[Optional[str]]:
        """
        A statement identifier prefix. This provider will generate a unique suffix. Conflicts with `statement_id`.
        """
        return pulumi.get(self, "statement_id_prefix")

