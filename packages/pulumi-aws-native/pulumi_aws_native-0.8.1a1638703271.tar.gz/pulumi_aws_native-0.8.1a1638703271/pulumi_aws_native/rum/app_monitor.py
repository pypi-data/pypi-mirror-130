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

__all__ = ['AppMonitorArgs', 'AppMonitor']

@pulumi.input_type
class AppMonitorArgs:
    def __init__(__self__, *,
                 app_monitor_configuration: Optional[pulumi.Input['AppMonitorConfigurationArgs']] = None,
                 cw_log_enabled: Optional[pulumi.Input[bool]] = None,
                 domain: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Sequence[pulumi.Input['AppMonitorTagArgs']]]] = None):
        """
        The set of arguments for constructing a AppMonitor resource.
        :param pulumi.Input[bool] cw_log_enabled: Data collected by RUM is kept by RUM for 30 days and then deleted. This parameter specifies whether RUM sends a copy of this telemetry data to CWLlong in your account. This enables you to keep the telemetry data for more than 30 days, but it does incur CWLlong charges. If you omit this parameter, the default is false
        :param pulumi.Input[str] domain: The top-level internet domain name for which your application has administrative authority.
        :param pulumi.Input[str] name: A name for the app monitor
        """
        if app_monitor_configuration is not None:
            pulumi.set(__self__, "app_monitor_configuration", app_monitor_configuration)
        if cw_log_enabled is not None:
            pulumi.set(__self__, "cw_log_enabled", cw_log_enabled)
        if domain is not None:
            pulumi.set(__self__, "domain", domain)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if tags is not None:
            pulumi.set(__self__, "tags", tags)

    @property
    @pulumi.getter(name="appMonitorConfiguration")
    def app_monitor_configuration(self) -> Optional[pulumi.Input['AppMonitorConfigurationArgs']]:
        return pulumi.get(self, "app_monitor_configuration")

    @app_monitor_configuration.setter
    def app_monitor_configuration(self, value: Optional[pulumi.Input['AppMonitorConfigurationArgs']]):
        pulumi.set(self, "app_monitor_configuration", value)

    @property
    @pulumi.getter(name="cwLogEnabled")
    def cw_log_enabled(self) -> Optional[pulumi.Input[bool]]:
        """
        Data collected by RUM is kept by RUM for 30 days and then deleted. This parameter specifies whether RUM sends a copy of this telemetry data to CWLlong in your account. This enables you to keep the telemetry data for more than 30 days, but it does incur CWLlong charges. If you omit this parameter, the default is false
        """
        return pulumi.get(self, "cw_log_enabled")

    @cw_log_enabled.setter
    def cw_log_enabled(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "cw_log_enabled", value)

    @property
    @pulumi.getter
    def domain(self) -> Optional[pulumi.Input[str]]:
        """
        The top-level internet domain name for which your application has administrative authority.
        """
        return pulumi.get(self, "domain")

    @domain.setter
    def domain(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "domain", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        A name for the app monitor
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter
    def tags(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['AppMonitorTagArgs']]]]:
        return pulumi.get(self, "tags")

    @tags.setter
    def tags(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['AppMonitorTagArgs']]]]):
        pulumi.set(self, "tags", value)


class AppMonitor(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 app_monitor_configuration: Optional[pulumi.Input[pulumi.InputType['AppMonitorConfigurationArgs']]] = None,
                 cw_log_enabled: Optional[pulumi.Input[bool]] = None,
                 domain: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['AppMonitorTagArgs']]]]] = None,
                 __props__=None):
        """
        Resource Type definition for AWS::RUM::AppMonitor

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[bool] cw_log_enabled: Data collected by RUM is kept by RUM for 30 days and then deleted. This parameter specifies whether RUM sends a copy of this telemetry data to CWLlong in your account. This enables you to keep the telemetry data for more than 30 days, but it does incur CWLlong charges. If you omit this parameter, the default is false
        :param pulumi.Input[str] domain: The top-level internet domain name for which your application has administrative authority.
        :param pulumi.Input[str] name: A name for the app monitor
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: Optional[AppMonitorArgs] = None,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Resource Type definition for AWS::RUM::AppMonitor

        :param str resource_name: The name of the resource.
        :param AppMonitorArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(AppMonitorArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 app_monitor_configuration: Optional[pulumi.Input[pulumi.InputType['AppMonitorConfigurationArgs']]] = None,
                 cw_log_enabled: Optional[pulumi.Input[bool]] = None,
                 domain: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['AppMonitorTagArgs']]]]] = None,
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
            __props__ = AppMonitorArgs.__new__(AppMonitorArgs)

            __props__.__dict__["app_monitor_configuration"] = app_monitor_configuration
            __props__.__dict__["cw_log_enabled"] = cw_log_enabled
            __props__.__dict__["domain"] = domain
            __props__.__dict__["name"] = name
            __props__.__dict__["tags"] = tags
        super(AppMonitor, __self__).__init__(
            'aws-native:rum:AppMonitor',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None) -> 'AppMonitor':
        """
        Get an existing AppMonitor resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = AppMonitorArgs.__new__(AppMonitorArgs)

        __props__.__dict__["app_monitor_configuration"] = None
        __props__.__dict__["cw_log_enabled"] = None
        __props__.__dict__["domain"] = None
        __props__.__dict__["name"] = None
        __props__.__dict__["tags"] = None
        return AppMonitor(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="appMonitorConfiguration")
    def app_monitor_configuration(self) -> pulumi.Output[Optional['outputs.AppMonitorConfiguration']]:
        return pulumi.get(self, "app_monitor_configuration")

    @property
    @pulumi.getter(name="cwLogEnabled")
    def cw_log_enabled(self) -> pulumi.Output[Optional[bool]]:
        """
        Data collected by RUM is kept by RUM for 30 days and then deleted. This parameter specifies whether RUM sends a copy of this telemetry data to CWLlong in your account. This enables you to keep the telemetry data for more than 30 days, but it does incur CWLlong charges. If you omit this parameter, the default is false
        """
        return pulumi.get(self, "cw_log_enabled")

    @property
    @pulumi.getter
    def domain(self) -> pulumi.Output[Optional[str]]:
        """
        The top-level internet domain name for which your application has administrative authority.
        """
        return pulumi.get(self, "domain")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[Optional[str]]:
        """
        A name for the app monitor
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def tags(self) -> pulumi.Output[Optional[Sequence['outputs.AppMonitorTag']]]:
        return pulumi.get(self, "tags")

