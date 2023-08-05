# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities

__all__ = [
    'TableRetentionProperties',
]

@pulumi.output_type
class TableRetentionProperties(dict):
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "magneticStoreRetentionPeriodInDays":
            suggest = "magnetic_store_retention_period_in_days"
        elif key == "memoryStoreRetentionPeriodInHours":
            suggest = "memory_store_retention_period_in_hours"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in TableRetentionProperties. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        TableRetentionProperties.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        TableRetentionProperties.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 magnetic_store_retention_period_in_days: int,
                 memory_store_retention_period_in_hours: int):
        """
        :param int magnetic_store_retention_period_in_days: The duration for which data must be stored in the magnetic store. Minimum value of 1. Maximum value of 73000.
        :param int memory_store_retention_period_in_hours: The duration for which data must be stored in the memory store. Minimum value of 1. Maximum value of 8766.
        """
        pulumi.set(__self__, "magnetic_store_retention_period_in_days", magnetic_store_retention_period_in_days)
        pulumi.set(__self__, "memory_store_retention_period_in_hours", memory_store_retention_period_in_hours)

    @property
    @pulumi.getter(name="magneticStoreRetentionPeriodInDays")
    def magnetic_store_retention_period_in_days(self) -> int:
        """
        The duration for which data must be stored in the magnetic store. Minimum value of 1. Maximum value of 73000.
        """
        return pulumi.get(self, "magnetic_store_retention_period_in_days")

    @property
    @pulumi.getter(name="memoryStoreRetentionPeriodInHours")
    def memory_store_retention_period_in_hours(self) -> int:
        """
        The duration for which data must be stored in the memory store. Minimum value of 1. Maximum value of 8766.
        """
        return pulumi.get(self, "memory_store_retention_period_in_hours")


