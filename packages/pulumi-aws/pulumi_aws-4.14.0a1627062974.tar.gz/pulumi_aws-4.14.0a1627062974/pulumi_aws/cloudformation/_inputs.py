# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities

__all__ = [
    'CloudFormationTypeLoggingConfigArgs',
    'StackSetAutoDeploymentArgs',
]

@pulumi.input_type
class CloudFormationTypeLoggingConfigArgs:
    def __init__(__self__, *,
                 log_group_name: pulumi.Input[str],
                 log_role_arn: pulumi.Input[str]):
        """
        :param pulumi.Input[str] log_group_name: Name of the CloudWatch Log Group where CloudFormation sends error logging information when invoking the type's handlers.
        :param pulumi.Input[str] log_role_arn: Amazon Resource Name (ARN) of the IAM Role CloudFormation assumes when sending error logging information to CloudWatch Logs.
        """
        pulumi.set(__self__, "log_group_name", log_group_name)
        pulumi.set(__self__, "log_role_arn", log_role_arn)

    @property
    @pulumi.getter(name="logGroupName")
    def log_group_name(self) -> pulumi.Input[str]:
        """
        Name of the CloudWatch Log Group where CloudFormation sends error logging information when invoking the type's handlers.
        """
        return pulumi.get(self, "log_group_name")

    @log_group_name.setter
    def log_group_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "log_group_name", value)

    @property
    @pulumi.getter(name="logRoleArn")
    def log_role_arn(self) -> pulumi.Input[str]:
        """
        Amazon Resource Name (ARN) of the IAM Role CloudFormation assumes when sending error logging information to CloudWatch Logs.
        """
        return pulumi.get(self, "log_role_arn")

    @log_role_arn.setter
    def log_role_arn(self, value: pulumi.Input[str]):
        pulumi.set(self, "log_role_arn", value)


@pulumi.input_type
class StackSetAutoDeploymentArgs:
    def __init__(__self__, *,
                 enabled: Optional[pulumi.Input[bool]] = None,
                 retain_stacks_on_account_removal: Optional[pulumi.Input[bool]] = None):
        """
        :param pulumi.Input[bool] enabled: Whether or not auto-deployment is enabled.
        :param pulumi.Input[bool] retain_stacks_on_account_removal: Whether or not to retain stacks when the account is removed.
        """
        if enabled is not None:
            pulumi.set(__self__, "enabled", enabled)
        if retain_stacks_on_account_removal is not None:
            pulumi.set(__self__, "retain_stacks_on_account_removal", retain_stacks_on_account_removal)

    @property
    @pulumi.getter
    def enabled(self) -> Optional[pulumi.Input[bool]]:
        """
        Whether or not auto-deployment is enabled.
        """
        return pulumi.get(self, "enabled")

    @enabled.setter
    def enabled(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "enabled", value)

    @property
    @pulumi.getter(name="retainStacksOnAccountRemoval")
    def retain_stacks_on_account_removal(self) -> Optional[pulumi.Input[bool]]:
        """
        Whether or not to retain stacks when the account is removed.
        """
        return pulumi.get(self, "retain_stacks_on_account_removal")

    @retain_stacks_on_account_removal.setter
    def retain_stacks_on_account_removal(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "retain_stacks_on_account_removal", value)


