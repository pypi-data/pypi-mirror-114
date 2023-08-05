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

__all__ = ['ScalingPlanArgs', 'ScalingPlan']

@pulumi.input_type
class ScalingPlanArgs:
    def __init__(__self__, *,
                 application_source: pulumi.Input['ScalingPlanApplicationSourceArgs'],
                 scaling_instructions: pulumi.Input[Sequence[pulumi.Input['ScalingPlanScalingInstructionArgs']]],
                 name: Optional[pulumi.Input[str]] = None):
        """
        The set of arguments for constructing a ScalingPlan resource.
        :param pulumi.Input['ScalingPlanApplicationSourceArgs'] application_source: A CloudFormation stack or set of tags. You can create one scaling plan per application source.
        :param pulumi.Input[Sequence[pulumi.Input['ScalingPlanScalingInstructionArgs']]] scaling_instructions: The scaling instructions. More details can be found in the [AWS Auto Scaling API Reference](https://docs.aws.amazon.com/autoscaling/plans/APIReference/API_ScalingInstruction.html).
        :param pulumi.Input[str] name: The name of the scaling plan. Names cannot contain vertical bars, colons, or forward slashes.
        """
        pulumi.set(__self__, "application_source", application_source)
        pulumi.set(__self__, "scaling_instructions", scaling_instructions)
        if name is not None:
            pulumi.set(__self__, "name", name)

    @property
    @pulumi.getter(name="applicationSource")
    def application_source(self) -> pulumi.Input['ScalingPlanApplicationSourceArgs']:
        """
        A CloudFormation stack or set of tags. You can create one scaling plan per application source.
        """
        return pulumi.get(self, "application_source")

    @application_source.setter
    def application_source(self, value: pulumi.Input['ScalingPlanApplicationSourceArgs']):
        pulumi.set(self, "application_source", value)

    @property
    @pulumi.getter(name="scalingInstructions")
    def scaling_instructions(self) -> pulumi.Input[Sequence[pulumi.Input['ScalingPlanScalingInstructionArgs']]]:
        """
        The scaling instructions. More details can be found in the [AWS Auto Scaling API Reference](https://docs.aws.amazon.com/autoscaling/plans/APIReference/API_ScalingInstruction.html).
        """
        return pulumi.get(self, "scaling_instructions")

    @scaling_instructions.setter
    def scaling_instructions(self, value: pulumi.Input[Sequence[pulumi.Input['ScalingPlanScalingInstructionArgs']]]):
        pulumi.set(self, "scaling_instructions", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the scaling plan. Names cannot contain vertical bars, colons, or forward slashes.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)


@pulumi.input_type
class _ScalingPlanState:
    def __init__(__self__, *,
                 application_source: Optional[pulumi.Input['ScalingPlanApplicationSourceArgs']] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 scaling_instructions: Optional[pulumi.Input[Sequence[pulumi.Input['ScalingPlanScalingInstructionArgs']]]] = None,
                 scaling_plan_version: Optional[pulumi.Input[int]] = None):
        """
        Input properties used for looking up and filtering ScalingPlan resources.
        :param pulumi.Input['ScalingPlanApplicationSourceArgs'] application_source: A CloudFormation stack or set of tags. You can create one scaling plan per application source.
        :param pulumi.Input[str] name: The name of the scaling plan. Names cannot contain vertical bars, colons, or forward slashes.
        :param pulumi.Input[Sequence[pulumi.Input['ScalingPlanScalingInstructionArgs']]] scaling_instructions: The scaling instructions. More details can be found in the [AWS Auto Scaling API Reference](https://docs.aws.amazon.com/autoscaling/plans/APIReference/API_ScalingInstruction.html).
        :param pulumi.Input[int] scaling_plan_version: The version number of the scaling plan. This value is always 1.
        """
        if application_source is not None:
            pulumi.set(__self__, "application_source", application_source)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if scaling_instructions is not None:
            pulumi.set(__self__, "scaling_instructions", scaling_instructions)
        if scaling_plan_version is not None:
            pulumi.set(__self__, "scaling_plan_version", scaling_plan_version)

    @property
    @pulumi.getter(name="applicationSource")
    def application_source(self) -> Optional[pulumi.Input['ScalingPlanApplicationSourceArgs']]:
        """
        A CloudFormation stack or set of tags. You can create one scaling plan per application source.
        """
        return pulumi.get(self, "application_source")

    @application_source.setter
    def application_source(self, value: Optional[pulumi.Input['ScalingPlanApplicationSourceArgs']]):
        pulumi.set(self, "application_source", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the scaling plan. Names cannot contain vertical bars, colons, or forward slashes.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter(name="scalingInstructions")
    def scaling_instructions(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['ScalingPlanScalingInstructionArgs']]]]:
        """
        The scaling instructions. More details can be found in the [AWS Auto Scaling API Reference](https://docs.aws.amazon.com/autoscaling/plans/APIReference/API_ScalingInstruction.html).
        """
        return pulumi.get(self, "scaling_instructions")

    @scaling_instructions.setter
    def scaling_instructions(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['ScalingPlanScalingInstructionArgs']]]]):
        pulumi.set(self, "scaling_instructions", value)

    @property
    @pulumi.getter(name="scalingPlanVersion")
    def scaling_plan_version(self) -> Optional[pulumi.Input[int]]:
        """
        The version number of the scaling plan. This value is always 1.
        """
        return pulumi.get(self, "scaling_plan_version")

    @scaling_plan_version.setter
    def scaling_plan_version(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "scaling_plan_version", value)


class ScalingPlan(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 application_source: Optional[pulumi.Input[pulumi.InputType['ScalingPlanApplicationSourceArgs']]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 scaling_instructions: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['ScalingPlanScalingInstructionArgs']]]]] = None,
                 __props__=None):
        """
        Manages an AWS Auto Scaling scaling plan.
        More information can be found in the [AWS Auto Scaling User Guide](https://docs.aws.amazon.com/autoscaling/plans/userguide/what-is-aws-auto-scaling.html).

        > **NOTE:** The AWS Auto Scaling service uses an AWS IAM service-linked role to manage predictive scaling of Amazon EC2 Auto Scaling groups. The service attempts to automatically create this role the first time a scaling plan with predictive scaling enabled is created.
        An `iam.ServiceLinkedRole` resource can be used to manually manage this role.
        See the [AWS documentation](https://docs.aws.amazon.com/autoscaling/plans/userguide/aws-auto-scaling-service-linked-roles.html#create-service-linked-role-manual) for more details.

        ## Example Usage

        ## Import

        Auto Scaling scaling plans can be imported using the `name`, e.g.

        ```sh
         $ pulumi import aws:autoscalingplans/scalingPlan:ScalingPlan example MyScale1
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[pulumi.InputType['ScalingPlanApplicationSourceArgs']] application_source: A CloudFormation stack or set of tags. You can create one scaling plan per application source.
        :param pulumi.Input[str] name: The name of the scaling plan. Names cannot contain vertical bars, colons, or forward slashes.
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['ScalingPlanScalingInstructionArgs']]]] scaling_instructions: The scaling instructions. More details can be found in the [AWS Auto Scaling API Reference](https://docs.aws.amazon.com/autoscaling/plans/APIReference/API_ScalingInstruction.html).
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: ScalingPlanArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Manages an AWS Auto Scaling scaling plan.
        More information can be found in the [AWS Auto Scaling User Guide](https://docs.aws.amazon.com/autoscaling/plans/userguide/what-is-aws-auto-scaling.html).

        > **NOTE:** The AWS Auto Scaling service uses an AWS IAM service-linked role to manage predictive scaling of Amazon EC2 Auto Scaling groups. The service attempts to automatically create this role the first time a scaling plan with predictive scaling enabled is created.
        An `iam.ServiceLinkedRole` resource can be used to manually manage this role.
        See the [AWS documentation](https://docs.aws.amazon.com/autoscaling/plans/userguide/aws-auto-scaling-service-linked-roles.html#create-service-linked-role-manual) for more details.

        ## Example Usage

        ## Import

        Auto Scaling scaling plans can be imported using the `name`, e.g.

        ```sh
         $ pulumi import aws:autoscalingplans/scalingPlan:ScalingPlan example MyScale1
        ```

        :param str resource_name: The name of the resource.
        :param ScalingPlanArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(ScalingPlanArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 application_source: Optional[pulumi.Input[pulumi.InputType['ScalingPlanApplicationSourceArgs']]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 scaling_instructions: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['ScalingPlanScalingInstructionArgs']]]]] = None,
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
            __props__ = ScalingPlanArgs.__new__(ScalingPlanArgs)

            if application_source is None and not opts.urn:
                raise TypeError("Missing required property 'application_source'")
            __props__.__dict__["application_source"] = application_source
            __props__.__dict__["name"] = name
            if scaling_instructions is None and not opts.urn:
                raise TypeError("Missing required property 'scaling_instructions'")
            __props__.__dict__["scaling_instructions"] = scaling_instructions
            __props__.__dict__["scaling_plan_version"] = None
        super(ScalingPlan, __self__).__init__(
            'aws:autoscalingplans/scalingPlan:ScalingPlan',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            application_source: Optional[pulumi.Input[pulumi.InputType['ScalingPlanApplicationSourceArgs']]] = None,
            name: Optional[pulumi.Input[str]] = None,
            scaling_instructions: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['ScalingPlanScalingInstructionArgs']]]]] = None,
            scaling_plan_version: Optional[pulumi.Input[int]] = None) -> 'ScalingPlan':
        """
        Get an existing ScalingPlan resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[pulumi.InputType['ScalingPlanApplicationSourceArgs']] application_source: A CloudFormation stack or set of tags. You can create one scaling plan per application source.
        :param pulumi.Input[str] name: The name of the scaling plan. Names cannot contain vertical bars, colons, or forward slashes.
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['ScalingPlanScalingInstructionArgs']]]] scaling_instructions: The scaling instructions. More details can be found in the [AWS Auto Scaling API Reference](https://docs.aws.amazon.com/autoscaling/plans/APIReference/API_ScalingInstruction.html).
        :param pulumi.Input[int] scaling_plan_version: The version number of the scaling plan. This value is always 1.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _ScalingPlanState.__new__(_ScalingPlanState)

        __props__.__dict__["application_source"] = application_source
        __props__.__dict__["name"] = name
        __props__.__dict__["scaling_instructions"] = scaling_instructions
        __props__.__dict__["scaling_plan_version"] = scaling_plan_version
        return ScalingPlan(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="applicationSource")
    def application_source(self) -> pulumi.Output['outputs.ScalingPlanApplicationSource']:
        """
        A CloudFormation stack or set of tags. You can create one scaling plan per application source.
        """
        return pulumi.get(self, "application_source")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        The name of the scaling plan. Names cannot contain vertical bars, colons, or forward slashes.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="scalingInstructions")
    def scaling_instructions(self) -> pulumi.Output[Sequence['outputs.ScalingPlanScalingInstruction']]:
        """
        The scaling instructions. More details can be found in the [AWS Auto Scaling API Reference](https://docs.aws.amazon.com/autoscaling/plans/APIReference/API_ScalingInstruction.html).
        """
        return pulumi.get(self, "scaling_instructions")

    @property
    @pulumi.getter(name="scalingPlanVersion")
    def scaling_plan_version(self) -> pulumi.Output[int]:
        """
        The version number of the scaling plan. This value is always 1.
        """
        return pulumi.get(self, "scaling_plan_version")

