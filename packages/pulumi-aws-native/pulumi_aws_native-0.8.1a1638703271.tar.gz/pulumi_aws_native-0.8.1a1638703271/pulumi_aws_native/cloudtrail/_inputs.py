# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities
from ._enums import *

__all__ = [
    'TrailDataResourceArgs',
    'TrailEventSelectorArgs',
    'TrailInsightSelectorArgs',
    'TrailTagArgs',
]

@pulumi.input_type
class TrailDataResourceArgs:
    def __init__(__self__, *,
                 type: pulumi.Input[str],
                 values: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None):
        """
        CloudTrail supports data event logging for Amazon S3 objects and AWS Lambda functions. You can specify up to 250 resources for an individual event selector, but the total number of data resources cannot exceed 250 across all event selectors in a trail. This limit does not apply if you configure resource logging for all data events.
        :param pulumi.Input[str] type: The resource type in which you want to log data events. You can specify AWS::S3::Object or AWS::Lambda::Function resources.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] values: An array of Amazon Resource Name (ARN) strings or partial ARN strings for the specified objects.
        """
        pulumi.set(__self__, "type", type)
        if values is not None:
            pulumi.set(__self__, "values", values)

    @property
    @pulumi.getter
    def type(self) -> pulumi.Input[str]:
        """
        The resource type in which you want to log data events. You can specify AWS::S3::Object or AWS::Lambda::Function resources.
        """
        return pulumi.get(self, "type")

    @type.setter
    def type(self, value: pulumi.Input[str]):
        pulumi.set(self, "type", value)

    @property
    @pulumi.getter
    def values(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        An array of Amazon Resource Name (ARN) strings or partial ARN strings for the specified objects.
        """
        return pulumi.get(self, "values")

    @values.setter
    def values(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "values", value)


@pulumi.input_type
class TrailEventSelectorArgs:
    def __init__(__self__, *,
                 data_resources: Optional[pulumi.Input[Sequence[pulumi.Input['TrailDataResourceArgs']]]] = None,
                 exclude_management_event_sources: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 include_management_events: Optional[pulumi.Input[bool]] = None,
                 read_write_type: Optional[pulumi.Input['TrailEventSelectorReadWriteType']] = None):
        """
        The type of email sending events to publish to the event destination.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] exclude_management_event_sources: An optional list of service event sources from which you do not want management events to be logged on your trail. In this release, the list can be empty (disables the filter), or it can filter out AWS Key Management Service events by containing "kms.amazonaws.com". By default, ExcludeManagementEventSources is empty, and AWS KMS events are included in events that are logged to your trail.
        :param pulumi.Input[bool] include_management_events: Specify if you want your event selector to include management events for your trail.
        :param pulumi.Input['TrailEventSelectorReadWriteType'] read_write_type: Specify if you want your trail to log read-only events, write-only events, or all. For example, the EC2 GetConsoleOutput is a read-only API operation and RunInstances is a write-only API operation.
        """
        if data_resources is not None:
            pulumi.set(__self__, "data_resources", data_resources)
        if exclude_management_event_sources is not None:
            pulumi.set(__self__, "exclude_management_event_sources", exclude_management_event_sources)
        if include_management_events is not None:
            pulumi.set(__self__, "include_management_events", include_management_events)
        if read_write_type is not None:
            pulumi.set(__self__, "read_write_type", read_write_type)

    @property
    @pulumi.getter(name="dataResources")
    def data_resources(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['TrailDataResourceArgs']]]]:
        return pulumi.get(self, "data_resources")

    @data_resources.setter
    def data_resources(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['TrailDataResourceArgs']]]]):
        pulumi.set(self, "data_resources", value)

    @property
    @pulumi.getter(name="excludeManagementEventSources")
    def exclude_management_event_sources(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        An optional list of service event sources from which you do not want management events to be logged on your trail. In this release, the list can be empty (disables the filter), or it can filter out AWS Key Management Service events by containing "kms.amazonaws.com". By default, ExcludeManagementEventSources is empty, and AWS KMS events are included in events that are logged to your trail.
        """
        return pulumi.get(self, "exclude_management_event_sources")

    @exclude_management_event_sources.setter
    def exclude_management_event_sources(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "exclude_management_event_sources", value)

    @property
    @pulumi.getter(name="includeManagementEvents")
    def include_management_events(self) -> Optional[pulumi.Input[bool]]:
        """
        Specify if you want your event selector to include management events for your trail.
        """
        return pulumi.get(self, "include_management_events")

    @include_management_events.setter
    def include_management_events(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "include_management_events", value)

    @property
    @pulumi.getter(name="readWriteType")
    def read_write_type(self) -> Optional[pulumi.Input['TrailEventSelectorReadWriteType']]:
        """
        Specify if you want your trail to log read-only events, write-only events, or all. For example, the EC2 GetConsoleOutput is a read-only API operation and RunInstances is a write-only API operation.
        """
        return pulumi.get(self, "read_write_type")

    @read_write_type.setter
    def read_write_type(self, value: Optional[pulumi.Input['TrailEventSelectorReadWriteType']]):
        pulumi.set(self, "read_write_type", value)


@pulumi.input_type
class TrailInsightSelectorArgs:
    def __init__(__self__, *,
                 insight_type: Optional[pulumi.Input[str]] = None):
        """
        A string that contains insight types that are logged on a trail.
        :param pulumi.Input[str] insight_type: The type of insight to log on a trail.
        """
        if insight_type is not None:
            pulumi.set(__self__, "insight_type", insight_type)

    @property
    @pulumi.getter(name="insightType")
    def insight_type(self) -> Optional[pulumi.Input[str]]:
        """
        The type of insight to log on a trail.
        """
        return pulumi.get(self, "insight_type")

    @insight_type.setter
    def insight_type(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "insight_type", value)


@pulumi.input_type
class TrailTagArgs:
    def __init__(__self__, *,
                 key: pulumi.Input[str],
                 value: pulumi.Input[str]):
        """
        An arbitrary set of tags (key-value pairs) for this trail.
        :param pulumi.Input[str] key: The key name of the tag. You can specify a value that is 1 to 127 Unicode characters in length and cannot be prefixed with aws:. You can use any of the following characters: the set of Unicode letters, digits, whitespace, _, ., /, =, +, and -.
        :param pulumi.Input[str] value: The value for the tag. You can specify a value that is 1 to 255 Unicode characters in length and cannot be prefixed with aws:. You can use any of the following characters: the set of Unicode letters, digits, whitespace, _, ., /, =, +, and -.
        """
        pulumi.set(__self__, "key", key)
        pulumi.set(__self__, "value", value)

    @property
    @pulumi.getter
    def key(self) -> pulumi.Input[str]:
        """
        The key name of the tag. You can specify a value that is 1 to 127 Unicode characters in length and cannot be prefixed with aws:. You can use any of the following characters: the set of Unicode letters, digits, whitespace, _, ., /, =, +, and -.
        """
        return pulumi.get(self, "key")

    @key.setter
    def key(self, value: pulumi.Input[str]):
        pulumi.set(self, "key", value)

    @property
    @pulumi.getter
    def value(self) -> pulumi.Input[str]:
        """
        The value for the tag. You can specify a value that is 1 to 255 Unicode characters in length and cannot be prefixed with aws:. You can use any of the following characters: the set of Unicode letters, digits, whitespace, _, ., /, =, +, and -.
        """
        return pulumi.get(self, "value")

    @value.setter
    def value(self, value: pulumi.Input[str]):
        pulumi.set(self, "value", value)


