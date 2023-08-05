# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities

__all__ = ['VPNGatewayRoutePropagationArgs', 'VPNGatewayRoutePropagation']

@pulumi.input_type
class VPNGatewayRoutePropagationArgs:
    def __init__(__self__, *,
                 route_table_ids: pulumi.Input[Sequence[pulumi.Input[str]]],
                 vpn_gateway_id: pulumi.Input[str]):
        """
        The set of arguments for constructing a VPNGatewayRoutePropagation resource.
        """
        pulumi.set(__self__, "route_table_ids", route_table_ids)
        pulumi.set(__self__, "vpn_gateway_id", vpn_gateway_id)

    @property
    @pulumi.getter(name="routeTableIds")
    def route_table_ids(self) -> pulumi.Input[Sequence[pulumi.Input[str]]]:
        return pulumi.get(self, "route_table_ids")

    @route_table_ids.setter
    def route_table_ids(self, value: pulumi.Input[Sequence[pulumi.Input[str]]]):
        pulumi.set(self, "route_table_ids", value)

    @property
    @pulumi.getter(name="vpnGatewayId")
    def vpn_gateway_id(self) -> pulumi.Input[str]:
        return pulumi.get(self, "vpn_gateway_id")

    @vpn_gateway_id.setter
    def vpn_gateway_id(self, value: pulumi.Input[str]):
        pulumi.set(self, "vpn_gateway_id", value)


warnings.warn("""VPNGatewayRoutePropagation is not yet supported by AWS Native, so its creation will currently fail. Please use the classic AWS provider, if possible.""", DeprecationWarning)


class VPNGatewayRoutePropagation(pulumi.CustomResource):
    warnings.warn("""VPNGatewayRoutePropagation is not yet supported by AWS Native, so its creation will currently fail. Please use the classic AWS provider, if possible.""", DeprecationWarning)

    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 route_table_ids: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 vpn_gateway_id: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        Resource Type definition for AWS::EC2::VPNGatewayRoutePropagation

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: VPNGatewayRoutePropagationArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Resource Type definition for AWS::EC2::VPNGatewayRoutePropagation

        :param str resource_name: The name of the resource.
        :param VPNGatewayRoutePropagationArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(VPNGatewayRoutePropagationArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 route_table_ids: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 vpn_gateway_id: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        pulumi.log.warn("""VPNGatewayRoutePropagation is deprecated: VPNGatewayRoutePropagation is not yet supported by AWS Native, so its creation will currently fail. Please use the classic AWS provider, if possible.""")
        if opts is None:
            opts = pulumi.ResourceOptions()
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.version is None:
            opts.version = _utilities.get_version()
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = VPNGatewayRoutePropagationArgs.__new__(VPNGatewayRoutePropagationArgs)

            if route_table_ids is None and not opts.urn:
                raise TypeError("Missing required property 'route_table_ids'")
            __props__.__dict__["route_table_ids"] = route_table_ids
            if vpn_gateway_id is None and not opts.urn:
                raise TypeError("Missing required property 'vpn_gateway_id'")
            __props__.__dict__["vpn_gateway_id"] = vpn_gateway_id
        super(VPNGatewayRoutePropagation, __self__).__init__(
            'aws-native:ec2:VPNGatewayRoutePropagation',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'VPNGatewayRoutePropagation':
        """
        Get an existing VPNGatewayRoutePropagation resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = VPNGatewayRoutePropagationArgs.__new__(VPNGatewayRoutePropagationArgs)

        __props__.__dict__["route_table_ids"] = None
        __props__.__dict__["vpn_gateway_id"] = None
        return VPNGatewayRoutePropagation(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="routeTableIds")
    def route_table_ids(self) -> pulumi.Output[Sequence[str]]:
        return pulumi.get(self, "route_table_ids")

    @property
    @pulumi.getter(name="vpnGatewayId")
    def vpn_gateway_id(self) -> pulumi.Output[str]:
        return pulumi.get(self, "vpn_gateway_id")

