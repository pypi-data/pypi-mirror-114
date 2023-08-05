# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities

__all__ = [
    'GetOrderableDbInstanceResult',
    'AwaitableGetOrderableDbInstanceResult',
    'get_orderable_db_instance',
]

@pulumi.output_type
class GetOrderableDbInstanceResult:
    """
    A collection of values returned by getOrderableDbInstance.
    """
    def __init__(__self__, availability_zones=None, engine=None, engine_version=None, id=None, instance_class=None, license_model=None, preferred_instance_classes=None, vpc=None):
        if availability_zones and not isinstance(availability_zones, list):
            raise TypeError("Expected argument 'availability_zones' to be a list")
        pulumi.set(__self__, "availability_zones", availability_zones)
        if engine and not isinstance(engine, str):
            raise TypeError("Expected argument 'engine' to be a str")
        pulumi.set(__self__, "engine", engine)
        if engine_version and not isinstance(engine_version, str):
            raise TypeError("Expected argument 'engine_version' to be a str")
        pulumi.set(__self__, "engine_version", engine_version)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if instance_class and not isinstance(instance_class, str):
            raise TypeError("Expected argument 'instance_class' to be a str")
        pulumi.set(__self__, "instance_class", instance_class)
        if license_model and not isinstance(license_model, str):
            raise TypeError("Expected argument 'license_model' to be a str")
        pulumi.set(__self__, "license_model", license_model)
        if preferred_instance_classes and not isinstance(preferred_instance_classes, list):
            raise TypeError("Expected argument 'preferred_instance_classes' to be a list")
        pulumi.set(__self__, "preferred_instance_classes", preferred_instance_classes)
        if vpc and not isinstance(vpc, bool):
            raise TypeError("Expected argument 'vpc' to be a bool")
        pulumi.set(__self__, "vpc", vpc)

    @property
    @pulumi.getter(name="availabilityZones")
    def availability_zones(self) -> Sequence[str]:
        """
        Availability zones where the instance is available.
        """
        return pulumi.get(self, "availability_zones")

    @property
    @pulumi.getter
    def engine(self) -> Optional[str]:
        return pulumi.get(self, "engine")

    @property
    @pulumi.getter(name="engineVersion")
    def engine_version(self) -> str:
        return pulumi.get(self, "engine_version")

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        The provider-assigned unique ID for this managed resource.
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter(name="instanceClass")
    def instance_class(self) -> str:
        return pulumi.get(self, "instance_class")

    @property
    @pulumi.getter(name="licenseModel")
    def license_model(self) -> Optional[str]:
        return pulumi.get(self, "license_model")

    @property
    @pulumi.getter(name="preferredInstanceClasses")
    def preferred_instance_classes(self) -> Optional[Sequence[str]]:
        return pulumi.get(self, "preferred_instance_classes")

    @property
    @pulumi.getter
    def vpc(self) -> bool:
        return pulumi.get(self, "vpc")


class AwaitableGetOrderableDbInstanceResult(GetOrderableDbInstanceResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetOrderableDbInstanceResult(
            availability_zones=self.availability_zones,
            engine=self.engine,
            engine_version=self.engine_version,
            id=self.id,
            instance_class=self.instance_class,
            license_model=self.license_model,
            preferred_instance_classes=self.preferred_instance_classes,
            vpc=self.vpc)


def get_orderable_db_instance(engine: Optional[str] = None,
                              engine_version: Optional[str] = None,
                              instance_class: Optional[str] = None,
                              license_model: Optional[str] = None,
                              preferred_instance_classes: Optional[Sequence[str]] = None,
                              vpc: Optional[bool] = None,
                              opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetOrderableDbInstanceResult:
    """
    Information about DocumentDB orderable DB instances.

    ## Example Usage

    ```python
    import pulumi
    import pulumi_aws as aws

    test = aws.docdb.get_orderable_db_instance(engine="docdb",
        engine_version="3.6.0",
        license_model="na",
        preferred_instance_classes=[
            "db.r5.large",
            "db.r4.large",
            "db.t3.medium",
        ])
    ```


    :param str engine: DB engine. Default: `docdb`
    :param str engine_version: Version of the DB engine.
    :param str instance_class: DB instance class. Examples of classes are `db.r5.12xlarge`, `db.r5.24xlarge`, `db.r5.2xlarge`, `db.r5.4xlarge`, `db.r5.large`, `db.r5.xlarge`, and `db.t3.medium`. (Conflicts with `preferred_instance_classes`.)
    :param str license_model: License model. Default: `na`
    :param Sequence[str] preferred_instance_classes: Ordered list of preferred DocumentDB DB instance classes. The first match in this list will be returned. If no preferred matches are found and the original search returned more than one result, an error is returned. (Conflicts with `instance_class`.)
    :param bool vpc: Enable to show only VPC.
    """
    __args__ = dict()
    __args__['engine'] = engine
    __args__['engineVersion'] = engine_version
    __args__['instanceClass'] = instance_class
    __args__['licenseModel'] = license_model
    __args__['preferredInstanceClasses'] = preferred_instance_classes
    __args__['vpc'] = vpc
    if opts is None:
        opts = pulumi.InvokeOptions()
    if opts.version is None:
        opts.version = _utilities.get_version()
    __ret__ = pulumi.runtime.invoke('aws:docdb/getOrderableDbInstance:getOrderableDbInstance', __args__, opts=opts, typ=GetOrderableDbInstanceResult).value

    return AwaitableGetOrderableDbInstanceResult(
        availability_zones=__ret__.availability_zones,
        engine=__ret__.engine,
        engine_version=__ret__.engine_version,
        id=__ret__.id,
        instance_class=__ret__.instance_class,
        license_model=__ret__.license_model,
        preferred_instance_classes=__ret__.preferred_instance_classes,
        vpc=__ret__.vpc)
