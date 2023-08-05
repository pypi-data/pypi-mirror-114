# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities

__all__ = [
    'DirectoryConnectSettingsArgs',
    'DirectoryVpcSettingsArgs',
]

@pulumi.input_type
class DirectoryConnectSettingsArgs:
    def __init__(__self__, *,
                 customer_dns_ips: pulumi.Input[Sequence[pulumi.Input[str]]],
                 customer_username: pulumi.Input[str],
                 subnet_ids: pulumi.Input[Sequence[pulumi.Input[str]]],
                 vpc_id: pulumi.Input[str],
                 availability_zones: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 connect_ips: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None):
        """
        :param pulumi.Input[Sequence[pulumi.Input[str]]] customer_dns_ips: The DNS IP addresses of the domain to connect to.
        :param pulumi.Input[str] customer_username: The username corresponding to the password provided.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] subnet_ids: The identifiers of the subnets for the directory servers (2 subnets in 2 different AZs).
        :param pulumi.Input[str] vpc_id: The identifier of the VPC that the directory is in.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] connect_ips: The IP addresses of the AD Connector servers.
        """
        pulumi.set(__self__, "customer_dns_ips", customer_dns_ips)
        pulumi.set(__self__, "customer_username", customer_username)
        pulumi.set(__self__, "subnet_ids", subnet_ids)
        pulumi.set(__self__, "vpc_id", vpc_id)
        if availability_zones is not None:
            pulumi.set(__self__, "availability_zones", availability_zones)
        if connect_ips is not None:
            pulumi.set(__self__, "connect_ips", connect_ips)

    @property
    @pulumi.getter(name="customerDnsIps")
    def customer_dns_ips(self) -> pulumi.Input[Sequence[pulumi.Input[str]]]:
        """
        The DNS IP addresses of the domain to connect to.
        """
        return pulumi.get(self, "customer_dns_ips")

    @customer_dns_ips.setter
    def customer_dns_ips(self, value: pulumi.Input[Sequence[pulumi.Input[str]]]):
        pulumi.set(self, "customer_dns_ips", value)

    @property
    @pulumi.getter(name="customerUsername")
    def customer_username(self) -> pulumi.Input[str]:
        """
        The username corresponding to the password provided.
        """
        return pulumi.get(self, "customer_username")

    @customer_username.setter
    def customer_username(self, value: pulumi.Input[str]):
        pulumi.set(self, "customer_username", value)

    @property
    @pulumi.getter(name="subnetIds")
    def subnet_ids(self) -> pulumi.Input[Sequence[pulumi.Input[str]]]:
        """
        The identifiers of the subnets for the directory servers (2 subnets in 2 different AZs).
        """
        return pulumi.get(self, "subnet_ids")

    @subnet_ids.setter
    def subnet_ids(self, value: pulumi.Input[Sequence[pulumi.Input[str]]]):
        pulumi.set(self, "subnet_ids", value)

    @property
    @pulumi.getter(name="vpcId")
    def vpc_id(self) -> pulumi.Input[str]:
        """
        The identifier of the VPC that the directory is in.
        """
        return pulumi.get(self, "vpc_id")

    @vpc_id.setter
    def vpc_id(self, value: pulumi.Input[str]):
        pulumi.set(self, "vpc_id", value)

    @property
    @pulumi.getter(name="availabilityZones")
    def availability_zones(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        return pulumi.get(self, "availability_zones")

    @availability_zones.setter
    def availability_zones(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "availability_zones", value)

    @property
    @pulumi.getter(name="connectIps")
    def connect_ips(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        The IP addresses of the AD Connector servers.
        """
        return pulumi.get(self, "connect_ips")

    @connect_ips.setter
    def connect_ips(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "connect_ips", value)


@pulumi.input_type
class DirectoryVpcSettingsArgs:
    def __init__(__self__, *,
                 subnet_ids: pulumi.Input[Sequence[pulumi.Input[str]]],
                 vpc_id: pulumi.Input[str],
                 availability_zones: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None):
        """
        :param pulumi.Input[Sequence[pulumi.Input[str]]] subnet_ids: The identifiers of the subnets for the directory servers (2 subnets in 2 different AZs).
        :param pulumi.Input[str] vpc_id: The identifier of the VPC that the directory is in.
        """
        pulumi.set(__self__, "subnet_ids", subnet_ids)
        pulumi.set(__self__, "vpc_id", vpc_id)
        if availability_zones is not None:
            pulumi.set(__self__, "availability_zones", availability_zones)

    @property
    @pulumi.getter(name="subnetIds")
    def subnet_ids(self) -> pulumi.Input[Sequence[pulumi.Input[str]]]:
        """
        The identifiers of the subnets for the directory servers (2 subnets in 2 different AZs).
        """
        return pulumi.get(self, "subnet_ids")

    @subnet_ids.setter
    def subnet_ids(self, value: pulumi.Input[Sequence[pulumi.Input[str]]]):
        pulumi.set(self, "subnet_ids", value)

    @property
    @pulumi.getter(name="vpcId")
    def vpc_id(self) -> pulumi.Input[str]:
        """
        The identifier of the VPC that the directory is in.
        """
        return pulumi.get(self, "vpc_id")

    @vpc_id.setter
    def vpc_id(self, value: pulumi.Input[str]):
        pulumi.set(self, "vpc_id", value)

    @property
    @pulumi.getter(name="availabilityZones")
    def availability_zones(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        return pulumi.get(self, "availability_zones")

    @availability_zones.setter
    def availability_zones(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "availability_zones", value)


