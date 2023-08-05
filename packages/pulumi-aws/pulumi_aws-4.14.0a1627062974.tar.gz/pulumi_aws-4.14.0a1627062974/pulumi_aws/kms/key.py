# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities

__all__ = ['KeyArgs', 'Key']

@pulumi.input_type
class KeyArgs:
    def __init__(__self__, *,
                 customer_master_key_spec: Optional[pulumi.Input[str]] = None,
                 deletion_window_in_days: Optional[pulumi.Input[int]] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 enable_key_rotation: Optional[pulumi.Input[bool]] = None,
                 is_enabled: Optional[pulumi.Input[bool]] = None,
                 key_usage: Optional[pulumi.Input[str]] = None,
                 policy: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 tags_all: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None):
        """
        The set of arguments for constructing a Key resource.
        :param pulumi.Input[str] customer_master_key_spec: Specifies whether the key contains a symmetric key or an asymmetric key pair and the encryption algorithms or signing algorithms that the key supports.
               Valid values: `SYMMETRIC_DEFAULT`,  `RSA_2048`, `RSA_3072`, `RSA_4096`, `ECC_NIST_P256`, `ECC_NIST_P384`, `ECC_NIST_P521`, or `ECC_SECG_P256K1`. Defaults to `SYMMETRIC_DEFAULT`. For help with choosing a key spec, see the [AWS KMS Developer Guide](https://docs.aws.amazon.com/kms/latest/developerguide/symm-asymm-choose.html).
        :param pulumi.Input[int] deletion_window_in_days: Duration in days after which the key is deleted after destruction of the resource, must be between 7 and 30 days. Defaults to 30 days.
        :param pulumi.Input[str] description: The description of the key as viewed in AWS console.
        :param pulumi.Input[bool] enable_key_rotation: Specifies whether [key rotation](http://docs.aws.amazon.com/kms/latest/developerguide/rotate-keys.html) is enabled. Defaults to false.
        :param pulumi.Input[bool] is_enabled: Specifies whether the key is enabled. Defaults to true.
        :param pulumi.Input[str] key_usage: Specifies the intended use of the key. Valid values: `ENCRYPT_DECRYPT` or `SIGN_VERIFY`.
               Defaults to `ENCRYPT_DECRYPT`.
        :param pulumi.Input[str] policy: A valid policy JSON document. Although this is a key policy, not an IAM policy, an `iam.getPolicyDocument`, in the form that designates a principal, can be used.
        """
        if customer_master_key_spec is not None:
            pulumi.set(__self__, "customer_master_key_spec", customer_master_key_spec)
        if deletion_window_in_days is not None:
            pulumi.set(__self__, "deletion_window_in_days", deletion_window_in_days)
        if description is not None:
            pulumi.set(__self__, "description", description)
        if enable_key_rotation is not None:
            pulumi.set(__self__, "enable_key_rotation", enable_key_rotation)
        if is_enabled is not None:
            pulumi.set(__self__, "is_enabled", is_enabled)
        if key_usage is not None:
            pulumi.set(__self__, "key_usage", key_usage)
        if policy is not None:
            pulumi.set(__self__, "policy", policy)
        if tags is not None:
            pulumi.set(__self__, "tags", tags)
        if tags_all is not None:
            pulumi.set(__self__, "tags_all", tags_all)

    @property
    @pulumi.getter(name="customerMasterKeySpec")
    def customer_master_key_spec(self) -> Optional[pulumi.Input[str]]:
        """
        Specifies whether the key contains a symmetric key or an asymmetric key pair and the encryption algorithms or signing algorithms that the key supports.
        Valid values: `SYMMETRIC_DEFAULT`,  `RSA_2048`, `RSA_3072`, `RSA_4096`, `ECC_NIST_P256`, `ECC_NIST_P384`, `ECC_NIST_P521`, or `ECC_SECG_P256K1`. Defaults to `SYMMETRIC_DEFAULT`. For help with choosing a key spec, see the [AWS KMS Developer Guide](https://docs.aws.amazon.com/kms/latest/developerguide/symm-asymm-choose.html).
        """
        return pulumi.get(self, "customer_master_key_spec")

    @customer_master_key_spec.setter
    def customer_master_key_spec(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "customer_master_key_spec", value)

    @property
    @pulumi.getter(name="deletionWindowInDays")
    def deletion_window_in_days(self) -> Optional[pulumi.Input[int]]:
        """
        Duration in days after which the key is deleted after destruction of the resource, must be between 7 and 30 days. Defaults to 30 days.
        """
        return pulumi.get(self, "deletion_window_in_days")

    @deletion_window_in_days.setter
    def deletion_window_in_days(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "deletion_window_in_days", value)

    @property
    @pulumi.getter
    def description(self) -> Optional[pulumi.Input[str]]:
        """
        The description of the key as viewed in AWS console.
        """
        return pulumi.get(self, "description")

    @description.setter
    def description(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "description", value)

    @property
    @pulumi.getter(name="enableKeyRotation")
    def enable_key_rotation(self) -> Optional[pulumi.Input[bool]]:
        """
        Specifies whether [key rotation](http://docs.aws.amazon.com/kms/latest/developerguide/rotate-keys.html) is enabled. Defaults to false.
        """
        return pulumi.get(self, "enable_key_rotation")

    @enable_key_rotation.setter
    def enable_key_rotation(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "enable_key_rotation", value)

    @property
    @pulumi.getter(name="isEnabled")
    def is_enabled(self) -> Optional[pulumi.Input[bool]]:
        """
        Specifies whether the key is enabled. Defaults to true.
        """
        return pulumi.get(self, "is_enabled")

    @is_enabled.setter
    def is_enabled(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "is_enabled", value)

    @property
    @pulumi.getter(name="keyUsage")
    def key_usage(self) -> Optional[pulumi.Input[str]]:
        """
        Specifies the intended use of the key. Valid values: `ENCRYPT_DECRYPT` or `SIGN_VERIFY`.
        Defaults to `ENCRYPT_DECRYPT`.
        """
        return pulumi.get(self, "key_usage")

    @key_usage.setter
    def key_usage(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "key_usage", value)

    @property
    @pulumi.getter
    def policy(self) -> Optional[pulumi.Input[str]]:
        """
        A valid policy JSON document. Although this is a key policy, not an IAM policy, an `iam.getPolicyDocument`, in the form that designates a principal, can be used.
        """
        return pulumi.get(self, "policy")

    @policy.setter
    def policy(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "policy", value)

    @property
    @pulumi.getter
    def tags(self) -> Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]:
        return pulumi.get(self, "tags")

    @tags.setter
    def tags(self, value: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]):
        pulumi.set(self, "tags", value)

    @property
    @pulumi.getter(name="tagsAll")
    def tags_all(self) -> Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]:
        return pulumi.get(self, "tags_all")

    @tags_all.setter
    def tags_all(self, value: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]):
        pulumi.set(self, "tags_all", value)


@pulumi.input_type
class _KeyState:
    def __init__(__self__, *,
                 arn: Optional[pulumi.Input[str]] = None,
                 customer_master_key_spec: Optional[pulumi.Input[str]] = None,
                 deletion_window_in_days: Optional[pulumi.Input[int]] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 enable_key_rotation: Optional[pulumi.Input[bool]] = None,
                 is_enabled: Optional[pulumi.Input[bool]] = None,
                 key_id: Optional[pulumi.Input[str]] = None,
                 key_usage: Optional[pulumi.Input[str]] = None,
                 policy: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 tags_all: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None):
        """
        Input properties used for looking up and filtering Key resources.
        :param pulumi.Input[str] arn: The Amazon Resource Name (ARN) of the key.
        :param pulumi.Input[str] customer_master_key_spec: Specifies whether the key contains a symmetric key or an asymmetric key pair and the encryption algorithms or signing algorithms that the key supports.
               Valid values: `SYMMETRIC_DEFAULT`,  `RSA_2048`, `RSA_3072`, `RSA_4096`, `ECC_NIST_P256`, `ECC_NIST_P384`, `ECC_NIST_P521`, or `ECC_SECG_P256K1`. Defaults to `SYMMETRIC_DEFAULT`. For help with choosing a key spec, see the [AWS KMS Developer Guide](https://docs.aws.amazon.com/kms/latest/developerguide/symm-asymm-choose.html).
        :param pulumi.Input[int] deletion_window_in_days: Duration in days after which the key is deleted after destruction of the resource, must be between 7 and 30 days. Defaults to 30 days.
        :param pulumi.Input[str] description: The description of the key as viewed in AWS console.
        :param pulumi.Input[bool] enable_key_rotation: Specifies whether [key rotation](http://docs.aws.amazon.com/kms/latest/developerguide/rotate-keys.html) is enabled. Defaults to false.
        :param pulumi.Input[bool] is_enabled: Specifies whether the key is enabled. Defaults to true.
        :param pulumi.Input[str] key_id: The globally unique identifier for the key.
        :param pulumi.Input[str] key_usage: Specifies the intended use of the key. Valid values: `ENCRYPT_DECRYPT` or `SIGN_VERIFY`.
               Defaults to `ENCRYPT_DECRYPT`.
        :param pulumi.Input[str] policy: A valid policy JSON document. Although this is a key policy, not an IAM policy, an `iam.getPolicyDocument`, in the form that designates a principal, can be used.
        """
        if arn is not None:
            pulumi.set(__self__, "arn", arn)
        if customer_master_key_spec is not None:
            pulumi.set(__self__, "customer_master_key_spec", customer_master_key_spec)
        if deletion_window_in_days is not None:
            pulumi.set(__self__, "deletion_window_in_days", deletion_window_in_days)
        if description is not None:
            pulumi.set(__self__, "description", description)
        if enable_key_rotation is not None:
            pulumi.set(__self__, "enable_key_rotation", enable_key_rotation)
        if is_enabled is not None:
            pulumi.set(__self__, "is_enabled", is_enabled)
        if key_id is not None:
            pulumi.set(__self__, "key_id", key_id)
        if key_usage is not None:
            pulumi.set(__self__, "key_usage", key_usage)
        if policy is not None:
            pulumi.set(__self__, "policy", policy)
        if tags is not None:
            pulumi.set(__self__, "tags", tags)
        if tags_all is not None:
            pulumi.set(__self__, "tags_all", tags_all)

    @property
    @pulumi.getter
    def arn(self) -> Optional[pulumi.Input[str]]:
        """
        The Amazon Resource Name (ARN) of the key.
        """
        return pulumi.get(self, "arn")

    @arn.setter
    def arn(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "arn", value)

    @property
    @pulumi.getter(name="customerMasterKeySpec")
    def customer_master_key_spec(self) -> Optional[pulumi.Input[str]]:
        """
        Specifies whether the key contains a symmetric key or an asymmetric key pair and the encryption algorithms or signing algorithms that the key supports.
        Valid values: `SYMMETRIC_DEFAULT`,  `RSA_2048`, `RSA_3072`, `RSA_4096`, `ECC_NIST_P256`, `ECC_NIST_P384`, `ECC_NIST_P521`, or `ECC_SECG_P256K1`. Defaults to `SYMMETRIC_DEFAULT`. For help with choosing a key spec, see the [AWS KMS Developer Guide](https://docs.aws.amazon.com/kms/latest/developerguide/symm-asymm-choose.html).
        """
        return pulumi.get(self, "customer_master_key_spec")

    @customer_master_key_spec.setter
    def customer_master_key_spec(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "customer_master_key_spec", value)

    @property
    @pulumi.getter(name="deletionWindowInDays")
    def deletion_window_in_days(self) -> Optional[pulumi.Input[int]]:
        """
        Duration in days after which the key is deleted after destruction of the resource, must be between 7 and 30 days. Defaults to 30 days.
        """
        return pulumi.get(self, "deletion_window_in_days")

    @deletion_window_in_days.setter
    def deletion_window_in_days(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "deletion_window_in_days", value)

    @property
    @pulumi.getter
    def description(self) -> Optional[pulumi.Input[str]]:
        """
        The description of the key as viewed in AWS console.
        """
        return pulumi.get(self, "description")

    @description.setter
    def description(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "description", value)

    @property
    @pulumi.getter(name="enableKeyRotation")
    def enable_key_rotation(self) -> Optional[pulumi.Input[bool]]:
        """
        Specifies whether [key rotation](http://docs.aws.amazon.com/kms/latest/developerguide/rotate-keys.html) is enabled. Defaults to false.
        """
        return pulumi.get(self, "enable_key_rotation")

    @enable_key_rotation.setter
    def enable_key_rotation(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "enable_key_rotation", value)

    @property
    @pulumi.getter(name="isEnabled")
    def is_enabled(self) -> Optional[pulumi.Input[bool]]:
        """
        Specifies whether the key is enabled. Defaults to true.
        """
        return pulumi.get(self, "is_enabled")

    @is_enabled.setter
    def is_enabled(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "is_enabled", value)

    @property
    @pulumi.getter(name="keyId")
    def key_id(self) -> Optional[pulumi.Input[str]]:
        """
        The globally unique identifier for the key.
        """
        return pulumi.get(self, "key_id")

    @key_id.setter
    def key_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "key_id", value)

    @property
    @pulumi.getter(name="keyUsage")
    def key_usage(self) -> Optional[pulumi.Input[str]]:
        """
        Specifies the intended use of the key. Valid values: `ENCRYPT_DECRYPT` or `SIGN_VERIFY`.
        Defaults to `ENCRYPT_DECRYPT`.
        """
        return pulumi.get(self, "key_usage")

    @key_usage.setter
    def key_usage(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "key_usage", value)

    @property
    @pulumi.getter
    def policy(self) -> Optional[pulumi.Input[str]]:
        """
        A valid policy JSON document. Although this is a key policy, not an IAM policy, an `iam.getPolicyDocument`, in the form that designates a principal, can be used.
        """
        return pulumi.get(self, "policy")

    @policy.setter
    def policy(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "policy", value)

    @property
    @pulumi.getter
    def tags(self) -> Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]:
        return pulumi.get(self, "tags")

    @tags.setter
    def tags(self, value: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]):
        pulumi.set(self, "tags", value)

    @property
    @pulumi.getter(name="tagsAll")
    def tags_all(self) -> Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]:
        return pulumi.get(self, "tags_all")

    @tags_all.setter
    def tags_all(self, value: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]):
        pulumi.set(self, "tags_all", value)


class Key(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 customer_master_key_spec: Optional[pulumi.Input[str]] = None,
                 deletion_window_in_days: Optional[pulumi.Input[int]] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 enable_key_rotation: Optional[pulumi.Input[bool]] = None,
                 is_enabled: Optional[pulumi.Input[bool]] = None,
                 key_usage: Optional[pulumi.Input[str]] = None,
                 policy: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 tags_all: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 __props__=None):
        """
        Provides a KMS single-Region customer master key (CMK).

        ## Example Usage

        ```python
        import pulumi
        import pulumi_aws as aws

        key = aws.kms.Key("key",
            deletion_window_in_days=10,
            description="KMS key 1")
        ```

        ## Import

        KMS Keys can be imported using the `id`, e.g.

        ```sh
         $ pulumi import aws:kms/key:Key a 1234abcd-12ab-34cd-56ef-1234567890ab
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] customer_master_key_spec: Specifies whether the key contains a symmetric key or an asymmetric key pair and the encryption algorithms or signing algorithms that the key supports.
               Valid values: `SYMMETRIC_DEFAULT`,  `RSA_2048`, `RSA_3072`, `RSA_4096`, `ECC_NIST_P256`, `ECC_NIST_P384`, `ECC_NIST_P521`, or `ECC_SECG_P256K1`. Defaults to `SYMMETRIC_DEFAULT`. For help with choosing a key spec, see the [AWS KMS Developer Guide](https://docs.aws.amazon.com/kms/latest/developerguide/symm-asymm-choose.html).
        :param pulumi.Input[int] deletion_window_in_days: Duration in days after which the key is deleted after destruction of the resource, must be between 7 and 30 days. Defaults to 30 days.
        :param pulumi.Input[str] description: The description of the key as viewed in AWS console.
        :param pulumi.Input[bool] enable_key_rotation: Specifies whether [key rotation](http://docs.aws.amazon.com/kms/latest/developerguide/rotate-keys.html) is enabled. Defaults to false.
        :param pulumi.Input[bool] is_enabled: Specifies whether the key is enabled. Defaults to true.
        :param pulumi.Input[str] key_usage: Specifies the intended use of the key. Valid values: `ENCRYPT_DECRYPT` or `SIGN_VERIFY`.
               Defaults to `ENCRYPT_DECRYPT`.
        :param pulumi.Input[str] policy: A valid policy JSON document. Although this is a key policy, not an IAM policy, an `iam.getPolicyDocument`, in the form that designates a principal, can be used.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: Optional[KeyArgs] = None,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Provides a KMS single-Region customer master key (CMK).

        ## Example Usage

        ```python
        import pulumi
        import pulumi_aws as aws

        key = aws.kms.Key("key",
            deletion_window_in_days=10,
            description="KMS key 1")
        ```

        ## Import

        KMS Keys can be imported using the `id`, e.g.

        ```sh
         $ pulumi import aws:kms/key:Key a 1234abcd-12ab-34cd-56ef-1234567890ab
        ```

        :param str resource_name: The name of the resource.
        :param KeyArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(KeyArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 customer_master_key_spec: Optional[pulumi.Input[str]] = None,
                 deletion_window_in_days: Optional[pulumi.Input[int]] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 enable_key_rotation: Optional[pulumi.Input[bool]] = None,
                 is_enabled: Optional[pulumi.Input[bool]] = None,
                 key_usage: Optional[pulumi.Input[str]] = None,
                 policy: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 tags_all: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
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
            __props__ = KeyArgs.__new__(KeyArgs)

            __props__.__dict__["customer_master_key_spec"] = customer_master_key_spec
            __props__.__dict__["deletion_window_in_days"] = deletion_window_in_days
            __props__.__dict__["description"] = description
            __props__.__dict__["enable_key_rotation"] = enable_key_rotation
            __props__.__dict__["is_enabled"] = is_enabled
            __props__.__dict__["key_usage"] = key_usage
            __props__.__dict__["policy"] = policy
            __props__.__dict__["tags"] = tags
            __props__.__dict__["tags_all"] = tags_all
            __props__.__dict__["arn"] = None
            __props__.__dict__["key_id"] = None
        super(Key, __self__).__init__(
            'aws:kms/key:Key',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            arn: Optional[pulumi.Input[str]] = None,
            customer_master_key_spec: Optional[pulumi.Input[str]] = None,
            deletion_window_in_days: Optional[pulumi.Input[int]] = None,
            description: Optional[pulumi.Input[str]] = None,
            enable_key_rotation: Optional[pulumi.Input[bool]] = None,
            is_enabled: Optional[pulumi.Input[bool]] = None,
            key_id: Optional[pulumi.Input[str]] = None,
            key_usage: Optional[pulumi.Input[str]] = None,
            policy: Optional[pulumi.Input[str]] = None,
            tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
            tags_all: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None) -> 'Key':
        """
        Get an existing Key resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] arn: The Amazon Resource Name (ARN) of the key.
        :param pulumi.Input[str] customer_master_key_spec: Specifies whether the key contains a symmetric key or an asymmetric key pair and the encryption algorithms or signing algorithms that the key supports.
               Valid values: `SYMMETRIC_DEFAULT`,  `RSA_2048`, `RSA_3072`, `RSA_4096`, `ECC_NIST_P256`, `ECC_NIST_P384`, `ECC_NIST_P521`, or `ECC_SECG_P256K1`. Defaults to `SYMMETRIC_DEFAULT`. For help with choosing a key spec, see the [AWS KMS Developer Guide](https://docs.aws.amazon.com/kms/latest/developerguide/symm-asymm-choose.html).
        :param pulumi.Input[int] deletion_window_in_days: Duration in days after which the key is deleted after destruction of the resource, must be between 7 and 30 days. Defaults to 30 days.
        :param pulumi.Input[str] description: The description of the key as viewed in AWS console.
        :param pulumi.Input[bool] enable_key_rotation: Specifies whether [key rotation](http://docs.aws.amazon.com/kms/latest/developerguide/rotate-keys.html) is enabled. Defaults to false.
        :param pulumi.Input[bool] is_enabled: Specifies whether the key is enabled. Defaults to true.
        :param pulumi.Input[str] key_id: The globally unique identifier for the key.
        :param pulumi.Input[str] key_usage: Specifies the intended use of the key. Valid values: `ENCRYPT_DECRYPT` or `SIGN_VERIFY`.
               Defaults to `ENCRYPT_DECRYPT`.
        :param pulumi.Input[str] policy: A valid policy JSON document. Although this is a key policy, not an IAM policy, an `iam.getPolicyDocument`, in the form that designates a principal, can be used.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _KeyState.__new__(_KeyState)

        __props__.__dict__["arn"] = arn
        __props__.__dict__["customer_master_key_spec"] = customer_master_key_spec
        __props__.__dict__["deletion_window_in_days"] = deletion_window_in_days
        __props__.__dict__["description"] = description
        __props__.__dict__["enable_key_rotation"] = enable_key_rotation
        __props__.__dict__["is_enabled"] = is_enabled
        __props__.__dict__["key_id"] = key_id
        __props__.__dict__["key_usage"] = key_usage
        __props__.__dict__["policy"] = policy
        __props__.__dict__["tags"] = tags
        __props__.__dict__["tags_all"] = tags_all
        return Key(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def arn(self) -> pulumi.Output[str]:
        """
        The Amazon Resource Name (ARN) of the key.
        """
        return pulumi.get(self, "arn")

    @property
    @pulumi.getter(name="customerMasterKeySpec")
    def customer_master_key_spec(self) -> pulumi.Output[Optional[str]]:
        """
        Specifies whether the key contains a symmetric key or an asymmetric key pair and the encryption algorithms or signing algorithms that the key supports.
        Valid values: `SYMMETRIC_DEFAULT`,  `RSA_2048`, `RSA_3072`, `RSA_4096`, `ECC_NIST_P256`, `ECC_NIST_P384`, `ECC_NIST_P521`, or `ECC_SECG_P256K1`. Defaults to `SYMMETRIC_DEFAULT`. For help with choosing a key spec, see the [AWS KMS Developer Guide](https://docs.aws.amazon.com/kms/latest/developerguide/symm-asymm-choose.html).
        """
        return pulumi.get(self, "customer_master_key_spec")

    @property
    @pulumi.getter(name="deletionWindowInDays")
    def deletion_window_in_days(self) -> pulumi.Output[Optional[int]]:
        """
        Duration in days after which the key is deleted after destruction of the resource, must be between 7 and 30 days. Defaults to 30 days.
        """
        return pulumi.get(self, "deletion_window_in_days")

    @property
    @pulumi.getter
    def description(self) -> pulumi.Output[str]:
        """
        The description of the key as viewed in AWS console.
        """
        return pulumi.get(self, "description")

    @property
    @pulumi.getter(name="enableKeyRotation")
    def enable_key_rotation(self) -> pulumi.Output[Optional[bool]]:
        """
        Specifies whether [key rotation](http://docs.aws.amazon.com/kms/latest/developerguide/rotate-keys.html) is enabled. Defaults to false.
        """
        return pulumi.get(self, "enable_key_rotation")

    @property
    @pulumi.getter(name="isEnabled")
    def is_enabled(self) -> pulumi.Output[Optional[bool]]:
        """
        Specifies whether the key is enabled. Defaults to true.
        """
        return pulumi.get(self, "is_enabled")

    @property
    @pulumi.getter(name="keyId")
    def key_id(self) -> pulumi.Output[str]:
        """
        The globally unique identifier for the key.
        """
        return pulumi.get(self, "key_id")

    @property
    @pulumi.getter(name="keyUsage")
    def key_usage(self) -> pulumi.Output[Optional[str]]:
        """
        Specifies the intended use of the key. Valid values: `ENCRYPT_DECRYPT` or `SIGN_VERIFY`.
        Defaults to `ENCRYPT_DECRYPT`.
        """
        return pulumi.get(self, "key_usage")

    @property
    @pulumi.getter
    def policy(self) -> pulumi.Output[str]:
        """
        A valid policy JSON document. Although this is a key policy, not an IAM policy, an `iam.getPolicyDocument`, in the form that designates a principal, can be used.
        """
        return pulumi.get(self, "policy")

    @property
    @pulumi.getter
    def tags(self) -> pulumi.Output[Optional[Mapping[str, str]]]:
        return pulumi.get(self, "tags")

    @property
    @pulumi.getter(name="tagsAll")
    def tags_all(self) -> pulumi.Output[Mapping[str, str]]:
        return pulumi.get(self, "tags_all")

