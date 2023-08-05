# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities
from . import outputs

__all__ = [
    'GetMeshResult',
    'AwaitableGetMeshResult',
    'get_mesh',
]

@pulumi.output_type
class GetMeshResult:
    """
    A collection of values returned by getMesh.
    """
    def __init__(__self__, arn=None, created_date=None, id=None, last_updated_date=None, mesh_owner=None, name=None, resource_owner=None, specs=None, tags=None):
        if arn and not isinstance(arn, str):
            raise TypeError("Expected argument 'arn' to be a str")
        pulumi.set(__self__, "arn", arn)
        if created_date and not isinstance(created_date, str):
            raise TypeError("Expected argument 'created_date' to be a str")
        pulumi.set(__self__, "created_date", created_date)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if last_updated_date and not isinstance(last_updated_date, str):
            raise TypeError("Expected argument 'last_updated_date' to be a str")
        pulumi.set(__self__, "last_updated_date", last_updated_date)
        if mesh_owner and not isinstance(mesh_owner, str):
            raise TypeError("Expected argument 'mesh_owner' to be a str")
        pulumi.set(__self__, "mesh_owner", mesh_owner)
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)
        if resource_owner and not isinstance(resource_owner, str):
            raise TypeError("Expected argument 'resource_owner' to be a str")
        pulumi.set(__self__, "resource_owner", resource_owner)
        if specs and not isinstance(specs, list):
            raise TypeError("Expected argument 'specs' to be a list")
        pulumi.set(__self__, "specs", specs)
        if tags and not isinstance(tags, dict):
            raise TypeError("Expected argument 'tags' to be a dict")
        pulumi.set(__self__, "tags", tags)

    @property
    @pulumi.getter
    def arn(self) -> str:
        """
        The ARN of the service mesh.
        """
        return pulumi.get(self, "arn")

    @property
    @pulumi.getter(name="createdDate")
    def created_date(self) -> str:
        """
        The creation date of the service mesh.
        """
        return pulumi.get(self, "created_date")

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        The provider-assigned unique ID for this managed resource.
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter(name="lastUpdatedDate")
    def last_updated_date(self) -> str:
        """
        The last update date of the service mesh.
        """
        return pulumi.get(self, "last_updated_date")

    @property
    @pulumi.getter(name="meshOwner")
    def mesh_owner(self) -> str:
        return pulumi.get(self, "mesh_owner")

    @property
    @pulumi.getter
    def name(self) -> str:
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="resourceOwner")
    def resource_owner(self) -> str:
        """
        The resource owner's AWS account ID.
        """
        return pulumi.get(self, "resource_owner")

    @property
    @pulumi.getter
    def specs(self) -> Sequence['outputs.GetMeshSpecResult']:
        """
        The service mesh specification.
        """
        return pulumi.get(self, "specs")

    @property
    @pulumi.getter
    def tags(self) -> Mapping[str, str]:
        """
        A map of tags.
        """
        return pulumi.get(self, "tags")


class AwaitableGetMeshResult(GetMeshResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetMeshResult(
            arn=self.arn,
            created_date=self.created_date,
            id=self.id,
            last_updated_date=self.last_updated_date,
            mesh_owner=self.mesh_owner,
            name=self.name,
            resource_owner=self.resource_owner,
            specs=self.specs,
            tags=self.tags)


def get_mesh(mesh_owner: Optional[str] = None,
             name: Optional[str] = None,
             tags: Optional[Mapping[str, str]] = None,
             opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetMeshResult:
    """
    The App Mesh Mesh data source allows details of an App Mesh Mesh to be retrieved by its name and optionally the mesh_owner.

    ## Example Usage

    ```python
    import pulumi
    import pulumi_aws as aws

    simple = aws.appmesh.get_mesh(name="simpleapp")
    ```

    ```python
    import pulumi
    import pulumi_aws as aws

    current = aws.get_caller_identity()
    simple = aws.appmesh.get_mesh(name="simpleapp",
        mesh_owner=current.account_id)
    ```


    :param str mesh_owner: The AWS account ID of the service mesh's owner.
    :param str name: The name of the service mesh.
    :param Mapping[str, str] tags: A map of tags.
    """
    __args__ = dict()
    __args__['meshOwner'] = mesh_owner
    __args__['name'] = name
    __args__['tags'] = tags
    if opts is None:
        opts = pulumi.InvokeOptions()
    if opts.version is None:
        opts.version = _utilities.get_version()
    __ret__ = pulumi.runtime.invoke('aws:appmesh/getMesh:getMesh', __args__, opts=opts, typ=GetMeshResult).value

    return AwaitableGetMeshResult(
        arn=__ret__.arn,
        created_date=__ret__.created_date,
        id=__ret__.id,
        last_updated_date=__ret__.last_updated_date,
        mesh_owner=__ret__.mesh_owner,
        name=__ret__.name,
        resource_owner=__ret__.resource_owner,
        specs=__ret__.specs,
        tags=__ret__.tags)
