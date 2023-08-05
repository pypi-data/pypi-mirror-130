# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities
from . import outputs
from ._enums import *
from ._inputs import *

__all__ = ['StreamArgs', 'Stream']

@pulumi.input_type
class StreamArgs:
    def __init__(__self__, *,
                 shard_count: pulumi.Input[int],
                 name: Optional[pulumi.Input[str]] = None,
                 retention_period_hours: Optional[pulumi.Input[int]] = None,
                 stream_encryption: Optional[pulumi.Input['StreamEncryptionArgs']] = None,
                 tags: Optional[pulumi.Input[Sequence[pulumi.Input['StreamTagArgs']]]] = None):
        """
        The set of arguments for constructing a Stream resource.
        :param pulumi.Input[int] shard_count: The number of shards that the stream uses.
        :param pulumi.Input[str] name: The name of the Kinesis stream.
        :param pulumi.Input[int] retention_period_hours: The number of hours for the data records that are stored in shards to remain accessible.
        :param pulumi.Input['StreamEncryptionArgs'] stream_encryption: When specified, enables or updates server-side encryption using an AWS KMS key for a specified stream.
        :param pulumi.Input[Sequence[pulumi.Input['StreamTagArgs']]] tags: An arbitrary set of tags (key–value pairs) to associate with the Kinesis stream.
        """
        pulumi.set(__self__, "shard_count", shard_count)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if retention_period_hours is not None:
            pulumi.set(__self__, "retention_period_hours", retention_period_hours)
        if stream_encryption is not None:
            pulumi.set(__self__, "stream_encryption", stream_encryption)
        if tags is not None:
            pulumi.set(__self__, "tags", tags)

    @property
    @pulumi.getter(name="shardCount")
    def shard_count(self) -> pulumi.Input[int]:
        """
        The number of shards that the stream uses.
        """
        return pulumi.get(self, "shard_count")

    @shard_count.setter
    def shard_count(self, value: pulumi.Input[int]):
        pulumi.set(self, "shard_count", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the Kinesis stream.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter(name="retentionPeriodHours")
    def retention_period_hours(self) -> Optional[pulumi.Input[int]]:
        """
        The number of hours for the data records that are stored in shards to remain accessible.
        """
        return pulumi.get(self, "retention_period_hours")

    @retention_period_hours.setter
    def retention_period_hours(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "retention_period_hours", value)

    @property
    @pulumi.getter(name="streamEncryption")
    def stream_encryption(self) -> Optional[pulumi.Input['StreamEncryptionArgs']]:
        """
        When specified, enables or updates server-side encryption using an AWS KMS key for a specified stream.
        """
        return pulumi.get(self, "stream_encryption")

    @stream_encryption.setter
    def stream_encryption(self, value: Optional[pulumi.Input['StreamEncryptionArgs']]):
        pulumi.set(self, "stream_encryption", value)

    @property
    @pulumi.getter
    def tags(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['StreamTagArgs']]]]:
        """
        An arbitrary set of tags (key–value pairs) to associate with the Kinesis stream.
        """
        return pulumi.get(self, "tags")

    @tags.setter
    def tags(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['StreamTagArgs']]]]):
        pulumi.set(self, "tags", value)


class Stream(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 retention_period_hours: Optional[pulumi.Input[int]] = None,
                 shard_count: Optional[pulumi.Input[int]] = None,
                 stream_encryption: Optional[pulumi.Input[pulumi.InputType['StreamEncryptionArgs']]] = None,
                 tags: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['StreamTagArgs']]]]] = None,
                 __props__=None):
        """
        Resource Type definition for AWS::Kinesis::Stream

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] name: The name of the Kinesis stream.
        :param pulumi.Input[int] retention_period_hours: The number of hours for the data records that are stored in shards to remain accessible.
        :param pulumi.Input[int] shard_count: The number of shards that the stream uses.
        :param pulumi.Input[pulumi.InputType['StreamEncryptionArgs']] stream_encryption: When specified, enables or updates server-side encryption using an AWS KMS key for a specified stream.
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['StreamTagArgs']]]] tags: An arbitrary set of tags (key–value pairs) to associate with the Kinesis stream.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: StreamArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Resource Type definition for AWS::Kinesis::Stream

        :param str resource_name: The name of the resource.
        :param StreamArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(StreamArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 retention_period_hours: Optional[pulumi.Input[int]] = None,
                 shard_count: Optional[pulumi.Input[int]] = None,
                 stream_encryption: Optional[pulumi.Input[pulumi.InputType['StreamEncryptionArgs']]] = None,
                 tags: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['StreamTagArgs']]]]] = None,
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
            __props__ = StreamArgs.__new__(StreamArgs)

            __props__.__dict__["name"] = name
            __props__.__dict__["retention_period_hours"] = retention_period_hours
            if shard_count is None and not opts.urn:
                raise TypeError("Missing required property 'shard_count'")
            __props__.__dict__["shard_count"] = shard_count
            __props__.__dict__["stream_encryption"] = stream_encryption
            __props__.__dict__["tags"] = tags
            __props__.__dict__["arn"] = None
        super(Stream, __self__).__init__(
            'aws-native:kinesis:Stream',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'Stream':
        """
        Get an existing Stream resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = StreamArgs.__new__(StreamArgs)

        __props__.__dict__["arn"] = None
        __props__.__dict__["name"] = None
        __props__.__dict__["retention_period_hours"] = None
        __props__.__dict__["shard_count"] = None
        __props__.__dict__["stream_encryption"] = None
        __props__.__dict__["tags"] = None
        return Stream(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def arn(self) -> pulumi.Output[str]:
        """
        The Amazon resource name (ARN) of the Kinesis stream
        """
        return pulumi.get(self, "arn")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[Optional[str]]:
        """
        The name of the Kinesis stream.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="retentionPeriodHours")
    def retention_period_hours(self) -> pulumi.Output[Optional[int]]:
        """
        The number of hours for the data records that are stored in shards to remain accessible.
        """
        return pulumi.get(self, "retention_period_hours")

    @property
    @pulumi.getter(name="shardCount")
    def shard_count(self) -> pulumi.Output[int]:
        """
        The number of shards that the stream uses.
        """
        return pulumi.get(self, "shard_count")

    @property
    @pulumi.getter(name="streamEncryption")
    def stream_encryption(self) -> pulumi.Output[Optional['outputs.StreamEncryption']]:
        """
        When specified, enables or updates server-side encryption using an AWS KMS key for a specified stream.
        """
        return pulumi.get(self, "stream_encryption")

    @property
    @pulumi.getter
    def tags(self) -> pulumi.Output[Optional[Sequence['outputs.StreamTag']]]:
        """
        An arbitrary set of tags (key–value pairs) to associate with the Kinesis stream.
        """
        return pulumi.get(self, "tags")

