# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities

__all__ = [
    'CellTagArgs',
    'ReadinessCheckTagArgs',
    'RecoveryGroupTagArgs',
    'ResourceSetDNSTargetResourceArgs',
    'ResourceSetNLBResourceArgs',
    'ResourceSetR53ResourceRecordArgs',
    'ResourceSetResourceArgs',
    'ResourceSetTagArgs',
    'ResourceSetTargetResourceArgs',
]

@pulumi.input_type
class CellTagArgs:
    def __init__(__self__, *,
                 key: pulumi.Input[str],
                 value: pulumi.Input[Sequence[pulumi.Input[str]]]):
        pulumi.set(__self__, "key", key)
        pulumi.set(__self__, "value", value)

    @property
    @pulumi.getter
    def key(self) -> pulumi.Input[str]:
        return pulumi.get(self, "key")

    @key.setter
    def key(self, value: pulumi.Input[str]):
        pulumi.set(self, "key", value)

    @property
    @pulumi.getter
    def value(self) -> pulumi.Input[Sequence[pulumi.Input[str]]]:
        return pulumi.get(self, "value")

    @value.setter
    def value(self, value: pulumi.Input[Sequence[pulumi.Input[str]]]):
        pulumi.set(self, "value", value)


@pulumi.input_type
class ReadinessCheckTagArgs:
    def __init__(__self__, *,
                 key: pulumi.Input[str],
                 value: pulumi.Input[Sequence[pulumi.Input[str]]]):
        pulumi.set(__self__, "key", key)
        pulumi.set(__self__, "value", value)

    @property
    @pulumi.getter
    def key(self) -> pulumi.Input[str]:
        return pulumi.get(self, "key")

    @key.setter
    def key(self, value: pulumi.Input[str]):
        pulumi.set(self, "key", value)

    @property
    @pulumi.getter
    def value(self) -> pulumi.Input[Sequence[pulumi.Input[str]]]:
        return pulumi.get(self, "value")

    @value.setter
    def value(self, value: pulumi.Input[Sequence[pulumi.Input[str]]]):
        pulumi.set(self, "value", value)


@pulumi.input_type
class RecoveryGroupTagArgs:
    def __init__(__self__, *,
                 key: pulumi.Input[str],
                 value: pulumi.Input[Sequence[pulumi.Input[str]]]):
        pulumi.set(__self__, "key", key)
        pulumi.set(__self__, "value", value)

    @property
    @pulumi.getter
    def key(self) -> pulumi.Input[str]:
        return pulumi.get(self, "key")

    @key.setter
    def key(self, value: pulumi.Input[str]):
        pulumi.set(self, "key", value)

    @property
    @pulumi.getter
    def value(self) -> pulumi.Input[Sequence[pulumi.Input[str]]]:
        return pulumi.get(self, "value")

    @value.setter
    def value(self, value: pulumi.Input[Sequence[pulumi.Input[str]]]):
        pulumi.set(self, "value", value)


@pulumi.input_type
class ResourceSetDNSTargetResourceArgs:
    def __init__(__self__, *,
                 domain_name: Optional[pulumi.Input[str]] = None,
                 hosted_zone_arn: Optional[pulumi.Input[str]] = None,
                 record_set_id: Optional[pulumi.Input[str]] = None,
                 record_type: Optional[pulumi.Input[str]] = None,
                 target_resource: Optional[pulumi.Input['ResourceSetTargetResourceArgs']] = None):
        """
        A component for DNS/routing control readiness checks.
        :param pulumi.Input[str] domain_name: The domain name that acts as an ingress point to a portion of the customer application.
        :param pulumi.Input[str] hosted_zone_arn: The hosted zone Amazon Resource Name (ARN) that contains the DNS record with the provided name of the target resource.
        :param pulumi.Input[str] record_set_id: The Route 53 record set ID that will uniquely identify a DNS record, given a name and a type.
        :param pulumi.Input[str] record_type: The type of DNS record of the target resource.
        """
        if domain_name is not None:
            pulumi.set(__self__, "domain_name", domain_name)
        if hosted_zone_arn is not None:
            pulumi.set(__self__, "hosted_zone_arn", hosted_zone_arn)
        if record_set_id is not None:
            pulumi.set(__self__, "record_set_id", record_set_id)
        if record_type is not None:
            pulumi.set(__self__, "record_type", record_type)
        if target_resource is not None:
            pulumi.set(__self__, "target_resource", target_resource)

    @property
    @pulumi.getter(name="domainName")
    def domain_name(self) -> Optional[pulumi.Input[str]]:
        """
        The domain name that acts as an ingress point to a portion of the customer application.
        """
        return pulumi.get(self, "domain_name")

    @domain_name.setter
    def domain_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "domain_name", value)

    @property
    @pulumi.getter(name="hostedZoneArn")
    def hosted_zone_arn(self) -> Optional[pulumi.Input[str]]:
        """
        The hosted zone Amazon Resource Name (ARN) that contains the DNS record with the provided name of the target resource.
        """
        return pulumi.get(self, "hosted_zone_arn")

    @hosted_zone_arn.setter
    def hosted_zone_arn(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "hosted_zone_arn", value)

    @property
    @pulumi.getter(name="recordSetId")
    def record_set_id(self) -> Optional[pulumi.Input[str]]:
        """
        The Route 53 record set ID that will uniquely identify a DNS record, given a name and a type.
        """
        return pulumi.get(self, "record_set_id")

    @record_set_id.setter
    def record_set_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "record_set_id", value)

    @property
    @pulumi.getter(name="recordType")
    def record_type(self) -> Optional[pulumi.Input[str]]:
        """
        The type of DNS record of the target resource.
        """
        return pulumi.get(self, "record_type")

    @record_type.setter
    def record_type(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "record_type", value)

    @property
    @pulumi.getter(name="targetResource")
    def target_resource(self) -> Optional[pulumi.Input['ResourceSetTargetResourceArgs']]:
        return pulumi.get(self, "target_resource")

    @target_resource.setter
    def target_resource(self, value: Optional[pulumi.Input['ResourceSetTargetResourceArgs']]):
        pulumi.set(self, "target_resource", value)


@pulumi.input_type
class ResourceSetNLBResourceArgs:
    def __init__(__self__, *,
                 arn: Optional[pulumi.Input[str]] = None):
        """
        The Network Load Balancer resource that a DNS target resource points to.
        :param pulumi.Input[str] arn: A Network Load Balancer resource Amazon Resource Name (ARN).
        """
        if arn is not None:
            pulumi.set(__self__, "arn", arn)

    @property
    @pulumi.getter
    def arn(self) -> Optional[pulumi.Input[str]]:
        """
        A Network Load Balancer resource Amazon Resource Name (ARN).
        """
        return pulumi.get(self, "arn")

    @arn.setter
    def arn(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "arn", value)


@pulumi.input_type
class ResourceSetR53ResourceRecordArgs:
    def __init__(__self__, *,
                 domain_name: Optional[pulumi.Input[str]] = None,
                 record_set_id: Optional[pulumi.Input[str]] = None):
        """
        The Route 53 resource that a DNS target resource record points to.
        :param pulumi.Input[str] domain_name: The DNS target domain name.
        :param pulumi.Input[str] record_set_id: The Resource Record set id.
        """
        if domain_name is not None:
            pulumi.set(__self__, "domain_name", domain_name)
        if record_set_id is not None:
            pulumi.set(__self__, "record_set_id", record_set_id)

    @property
    @pulumi.getter(name="domainName")
    def domain_name(self) -> Optional[pulumi.Input[str]]:
        """
        The DNS target domain name.
        """
        return pulumi.get(self, "domain_name")

    @domain_name.setter
    def domain_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "domain_name", value)

    @property
    @pulumi.getter(name="recordSetId")
    def record_set_id(self) -> Optional[pulumi.Input[str]]:
        """
        The Resource Record set id.
        """
        return pulumi.get(self, "record_set_id")

    @record_set_id.setter
    def record_set_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "record_set_id", value)


@pulumi.input_type
class ResourceSetResourceArgs:
    def __init__(__self__, *,
                 component_id: Optional[pulumi.Input[str]] = None,
                 dns_target_resource: Optional[pulumi.Input['ResourceSetDNSTargetResourceArgs']] = None,
                 readiness_scopes: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 resource_arn: Optional[pulumi.Input[str]] = None):
        """
        The resource element of a ResourceSet
        :param pulumi.Input[str] component_id: The component identifier of the resource, generated when DNS target resource is used.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] readiness_scopes: A list of recovery group Amazon Resource Names (ARNs) and cell ARNs that this resource is contained within.
        :param pulumi.Input[str] resource_arn: The Amazon Resource Name (ARN) of the AWS resource.
        """
        if component_id is not None:
            pulumi.set(__self__, "component_id", component_id)
        if dns_target_resource is not None:
            pulumi.set(__self__, "dns_target_resource", dns_target_resource)
        if readiness_scopes is not None:
            pulumi.set(__self__, "readiness_scopes", readiness_scopes)
        if resource_arn is not None:
            pulumi.set(__self__, "resource_arn", resource_arn)

    @property
    @pulumi.getter(name="componentId")
    def component_id(self) -> Optional[pulumi.Input[str]]:
        """
        The component identifier of the resource, generated when DNS target resource is used.
        """
        return pulumi.get(self, "component_id")

    @component_id.setter
    def component_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "component_id", value)

    @property
    @pulumi.getter(name="dnsTargetResource")
    def dns_target_resource(self) -> Optional[pulumi.Input['ResourceSetDNSTargetResourceArgs']]:
        return pulumi.get(self, "dns_target_resource")

    @dns_target_resource.setter
    def dns_target_resource(self, value: Optional[pulumi.Input['ResourceSetDNSTargetResourceArgs']]):
        pulumi.set(self, "dns_target_resource", value)

    @property
    @pulumi.getter(name="readinessScopes")
    def readiness_scopes(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        A list of recovery group Amazon Resource Names (ARNs) and cell ARNs that this resource is contained within.
        """
        return pulumi.get(self, "readiness_scopes")

    @readiness_scopes.setter
    def readiness_scopes(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "readiness_scopes", value)

    @property
    @pulumi.getter(name="resourceArn")
    def resource_arn(self) -> Optional[pulumi.Input[str]]:
        """
        The Amazon Resource Name (ARN) of the AWS resource.
        """
        return pulumi.get(self, "resource_arn")

    @resource_arn.setter
    def resource_arn(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "resource_arn", value)


@pulumi.input_type
class ResourceSetTagArgs:
    def __init__(__self__, *,
                 key: pulumi.Input[str],
                 value: pulumi.Input[Sequence[pulumi.Input[str]]]):
        pulumi.set(__self__, "key", key)
        pulumi.set(__self__, "value", value)

    @property
    @pulumi.getter
    def key(self) -> pulumi.Input[str]:
        return pulumi.get(self, "key")

    @key.setter
    def key(self, value: pulumi.Input[str]):
        pulumi.set(self, "key", value)

    @property
    @pulumi.getter
    def value(self) -> pulumi.Input[Sequence[pulumi.Input[str]]]:
        return pulumi.get(self, "value")

    @value.setter
    def value(self, value: pulumi.Input[Sequence[pulumi.Input[str]]]):
        pulumi.set(self, "value", value)


@pulumi.input_type
class ResourceSetTargetResourceArgs:
    def __init__(__self__, *,
                 n_lb_resource: Optional[pulumi.Input['ResourceSetNLBResourceArgs']] = None,
                 r53_resource: Optional[pulumi.Input['ResourceSetR53ResourceRecordArgs']] = None):
        """
        The target resource that the Route 53 record points to.
        """
        if n_lb_resource is not None:
            pulumi.set(__self__, "n_lb_resource", n_lb_resource)
        if r53_resource is not None:
            pulumi.set(__self__, "r53_resource", r53_resource)

    @property
    @pulumi.getter(name="nLBResource")
    def n_lb_resource(self) -> Optional[pulumi.Input['ResourceSetNLBResourceArgs']]:
        return pulumi.get(self, "n_lb_resource")

    @n_lb_resource.setter
    def n_lb_resource(self, value: Optional[pulumi.Input['ResourceSetNLBResourceArgs']]):
        pulumi.set(self, "n_lb_resource", value)

    @property
    @pulumi.getter(name="r53Resource")
    def r53_resource(self) -> Optional[pulumi.Input['ResourceSetR53ResourceRecordArgs']]:
        return pulumi.get(self, "r53_resource")

    @r53_resource.setter
    def r53_resource(self, value: Optional[pulumi.Input['ResourceSetR53ResourceRecordArgs']]):
        pulumi.set(self, "r53_resource", value)


