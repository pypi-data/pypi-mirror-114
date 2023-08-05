# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities
from . import outputs
from ._inputs import *

__all__ = [
    'GetSecurityGroupsResult',
    'AwaitableGetSecurityGroupsResult',
    'get_security_groups',
]

@pulumi.output_type
class GetSecurityGroupsResult:
    """
    A collection of values returned by getSecurityGroups.
    """
    def __init__(__self__, arns=None, filters=None, id=None, ids=None, tags=None, vpc_ids=None):
        if arns and not isinstance(arns, list):
            raise TypeError("Expected argument 'arns' to be a list")
        pulumi.set(__self__, "arns", arns)
        if filters and not isinstance(filters, list):
            raise TypeError("Expected argument 'filters' to be a list")
        pulumi.set(__self__, "filters", filters)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if ids and not isinstance(ids, list):
            raise TypeError("Expected argument 'ids' to be a list")
        pulumi.set(__self__, "ids", ids)
        if tags and not isinstance(tags, dict):
            raise TypeError("Expected argument 'tags' to be a dict")
        pulumi.set(__self__, "tags", tags)
        if vpc_ids and not isinstance(vpc_ids, list):
            raise TypeError("Expected argument 'vpc_ids' to be a list")
        pulumi.set(__self__, "vpc_ids", vpc_ids)

    @property
    @pulumi.getter
    def arns(self) -> Sequence[str]:
        """
        ARNs of the matched security groups.
        """
        return pulumi.get(self, "arns")

    @property
    @pulumi.getter
    def filters(self) -> Optional[Sequence['outputs.GetSecurityGroupsFilterResult']]:
        return pulumi.get(self, "filters")

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        The provider-assigned unique ID for this managed resource.
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter
    def ids(self) -> Sequence[str]:
        """
        IDs of the matches security groups.
        """
        return pulumi.get(self, "ids")

    @property
    @pulumi.getter
    def tags(self) -> Mapping[str, str]:
        return pulumi.get(self, "tags")

    @property
    @pulumi.getter(name="vpcIds")
    def vpc_ids(self) -> Sequence[str]:
        """
        The VPC IDs of the matched security groups. The data source's tag or filter *will span VPCs* unless the `vpc-id` filter is also used.
        """
        return pulumi.get(self, "vpc_ids")


class AwaitableGetSecurityGroupsResult(GetSecurityGroupsResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetSecurityGroupsResult(
            arns=self.arns,
            filters=self.filters,
            id=self.id,
            ids=self.ids,
            tags=self.tags,
            vpc_ids=self.vpc_ids)


def get_security_groups(filters: Optional[Sequence[pulumi.InputType['GetSecurityGroupsFilterArgs']]] = None,
                        tags: Optional[Mapping[str, str]] = None,
                        opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetSecurityGroupsResult:
    """
    Use this data source to get IDs and VPC membership of Security Groups that are created
    outside of this provider.

    ## Example Usage

    ```python
    import pulumi
    import pulumi_aws as aws

    test = aws.ec2.get_security_groups(tags={
        "Application": "k8s",
        "Environment": "dev",
    })
    ```

    ```python
    import pulumi
    import pulumi_aws as aws

    test = aws.ec2.get_security_groups(filters=[
        aws.ec2.GetSecurityGroupsFilterArgs(
            name="group-name",
            values=["*nodes*"],
        ),
        aws.ec2.GetSecurityGroupsFilterArgs(
            name="vpc-id",
            values=[var["vpc_id"]],
        ),
    ])
    ```


    :param Sequence[pulumi.InputType['GetSecurityGroupsFilterArgs']] filters: One or more name/value pairs to use as filters. There are several valid keys, for a full reference, check out [describe-security-groups in the AWS CLI reference][1].
    :param Mapping[str, str] tags: A map of tags, each pair of which must exactly match for desired security groups.
    """
    __args__ = dict()
    __args__['filters'] = filters
    __args__['tags'] = tags
    if opts is None:
        opts = pulumi.InvokeOptions()
    if opts.version is None:
        opts.version = _utilities.get_version()
    __ret__ = pulumi.runtime.invoke('aws:ec2/getSecurityGroups:getSecurityGroups', __args__, opts=opts, typ=GetSecurityGroupsResult).value

    return AwaitableGetSecurityGroupsResult(
        arns=__ret__.arns,
        filters=__ret__.filters,
        id=__ret__.id,
        ids=__ret__.ids,
        tags=__ret__.tags,
        vpc_ids=__ret__.vpc_ids)
