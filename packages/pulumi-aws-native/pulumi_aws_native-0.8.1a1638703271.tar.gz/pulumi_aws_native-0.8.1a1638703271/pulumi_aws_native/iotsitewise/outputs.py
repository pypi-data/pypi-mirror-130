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

__all__ = [
    'AccessPolicyIamRole',
    'AccessPolicyIamUser',
    'AccessPolicyIdentity',
    'AccessPolicyPortal',
    'AccessPolicyProject',
    'AccessPolicyResource',
    'AccessPolicyUser',
    'AlarmsProperties',
    'AssetHierarchy',
    'AssetModelAttribute',
    'AssetModelCompositeModel',
    'AssetModelExpressionVariable',
    'AssetModelHierarchy',
    'AssetModelMetric',
    'AssetModelMetricWindow',
    'AssetModelProperty',
    'AssetModelPropertyType',
    'AssetModelTag',
    'AssetModelTransform',
    'AssetModelTumblingWindow',
    'AssetModelVariableValue',
    'AssetProperty',
    'AssetTag',
    'DashboardTag',
    'GatewayCapabilitySummary',
    'GatewayGreengrass',
    'GatewayPlatform',
    'GatewayTag',
    'PortalTag',
    'ProjectTag',
]

@pulumi.output_type
class AccessPolicyIamRole(dict):
    """
    Contains information for an IAM role identity in an access policy.
    """
    def __init__(__self__, *,
                 arn: Optional[str] = None):
        """
        Contains information for an IAM role identity in an access policy.
        :param str arn: The ARN of the IAM role.
        """
        if arn is not None:
            pulumi.set(__self__, "arn", arn)

    @property
    @pulumi.getter
    def arn(self) -> Optional[str]:
        """
        The ARN of the IAM role.
        """
        return pulumi.get(self, "arn")


@pulumi.output_type
class AccessPolicyIamUser(dict):
    """
    Contains information for an IAM user identity in an access policy.
    """
    def __init__(__self__, *,
                 arn: Optional[str] = None):
        """
        Contains information for an IAM user identity in an access policy.
        :param str arn: The ARN of the IAM user.
        """
        if arn is not None:
            pulumi.set(__self__, "arn", arn)

    @property
    @pulumi.getter
    def arn(self) -> Optional[str]:
        """
        The ARN of the IAM user.
        """
        return pulumi.get(self, "arn")


@pulumi.output_type
class AccessPolicyIdentity(dict):
    """
    The identity for this access policy. Choose either an SSO user or group or an IAM user or role.
    """
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "iamRole":
            suggest = "iam_role"
        elif key == "iamUser":
            suggest = "iam_user"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in AccessPolicyIdentity. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        AccessPolicyIdentity.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        AccessPolicyIdentity.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 iam_role: Optional['outputs.AccessPolicyIamRole'] = None,
                 iam_user: Optional['outputs.AccessPolicyIamUser'] = None,
                 user: Optional['outputs.AccessPolicyUser'] = None):
        """
        The identity for this access policy. Choose either an SSO user or group or an IAM user or role.
        """
        if iam_role is not None:
            pulumi.set(__self__, "iam_role", iam_role)
        if iam_user is not None:
            pulumi.set(__self__, "iam_user", iam_user)
        if user is not None:
            pulumi.set(__self__, "user", user)

    @property
    @pulumi.getter(name="iamRole")
    def iam_role(self) -> Optional['outputs.AccessPolicyIamRole']:
        return pulumi.get(self, "iam_role")

    @property
    @pulumi.getter(name="iamUser")
    def iam_user(self) -> Optional['outputs.AccessPolicyIamUser']:
        return pulumi.get(self, "iam_user")

    @property
    @pulumi.getter
    def user(self) -> Optional['outputs.AccessPolicyUser']:
        return pulumi.get(self, "user")


@pulumi.output_type
class AccessPolicyPortal(dict):
    """
    A portal resource.
    """
    def __init__(__self__, *,
                 id: Optional[str] = None):
        """
        A portal resource.
        :param str id: The ID of the portal.
        """
        if id is not None:
            pulumi.set(__self__, "id", id)

    @property
    @pulumi.getter
    def id(self) -> Optional[str]:
        """
        The ID of the portal.
        """
        return pulumi.get(self, "id")


@pulumi.output_type
class AccessPolicyProject(dict):
    """
    A project resource.
    """
    def __init__(__self__, *,
                 id: Optional[str] = None):
        """
        A project resource.
        :param str id: The ID of the project.
        """
        if id is not None:
            pulumi.set(__self__, "id", id)

    @property
    @pulumi.getter
    def id(self) -> Optional[str]:
        """
        The ID of the project.
        """
        return pulumi.get(self, "id")


@pulumi.output_type
class AccessPolicyResource(dict):
    """
    The AWS IoT SiteWise Monitor resource for this access policy. Choose either portal or project but not both.
    """
    def __init__(__self__, *,
                 portal: Optional['outputs.AccessPolicyPortal'] = None,
                 project: Optional['outputs.AccessPolicyProject'] = None):
        """
        The AWS IoT SiteWise Monitor resource for this access policy. Choose either portal or project but not both.
        """
        if portal is not None:
            pulumi.set(__self__, "portal", portal)
        if project is not None:
            pulumi.set(__self__, "project", project)

    @property
    @pulumi.getter
    def portal(self) -> Optional['outputs.AccessPolicyPortal']:
        return pulumi.get(self, "portal")

    @property
    @pulumi.getter
    def project(self) -> Optional['outputs.AccessPolicyProject']:
        return pulumi.get(self, "project")


@pulumi.output_type
class AccessPolicyUser(dict):
    """
    Contains information for a user identity in an access policy.
    """
    def __init__(__self__, *,
                 id: Optional[str] = None):
        """
        Contains information for a user identity in an access policy.
        :param str id: The AWS SSO ID of the user.
        """
        if id is not None:
            pulumi.set(__self__, "id", id)

    @property
    @pulumi.getter
    def id(self) -> Optional[str]:
        """
        The AWS SSO ID of the user.
        """
        return pulumi.get(self, "id")


@pulumi.output_type
class AlarmsProperties(dict):
    """
    Contains the configuration information of an alarm created in an AWS IoT SiteWise Monitor portal. You can use the alarm to monitor an asset property and get notified when the asset property value is outside a specified range.
    """
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "alarmRoleArn":
            suggest = "alarm_role_arn"
        elif key == "notificationLambdaArn":
            suggest = "notification_lambda_arn"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in AlarmsProperties. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        AlarmsProperties.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        AlarmsProperties.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 alarm_role_arn: Optional[str] = None,
                 notification_lambda_arn: Optional[str] = None):
        """
        Contains the configuration information of an alarm created in an AWS IoT SiteWise Monitor portal. You can use the alarm to monitor an asset property and get notified when the asset property value is outside a specified range.
        :param str alarm_role_arn: The ARN of the IAM role that allows the alarm to perform actions and access AWS resources and services, such as AWS IoT Events.
        :param str notification_lambda_arn: The ARN of the AWS Lambda function that manages alarm notifications. For more information, see Managing alarm notifications in the AWS IoT Events Developer Guide.
        """
        if alarm_role_arn is not None:
            pulumi.set(__self__, "alarm_role_arn", alarm_role_arn)
        if notification_lambda_arn is not None:
            pulumi.set(__self__, "notification_lambda_arn", notification_lambda_arn)

    @property
    @pulumi.getter(name="alarmRoleArn")
    def alarm_role_arn(self) -> Optional[str]:
        """
        The ARN of the IAM role that allows the alarm to perform actions and access AWS resources and services, such as AWS IoT Events.
        """
        return pulumi.get(self, "alarm_role_arn")

    @property
    @pulumi.getter(name="notificationLambdaArn")
    def notification_lambda_arn(self) -> Optional[str]:
        """
        The ARN of the AWS Lambda function that manages alarm notifications. For more information, see Managing alarm notifications in the AWS IoT Events Developer Guide.
        """
        return pulumi.get(self, "notification_lambda_arn")


@pulumi.output_type
class AssetHierarchy(dict):
    """
    A hierarchy specifies allowed parent/child asset relationships.
    """
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "childAssetId":
            suggest = "child_asset_id"
        elif key == "logicalId":
            suggest = "logical_id"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in AssetHierarchy. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        AssetHierarchy.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        AssetHierarchy.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 child_asset_id: str,
                 logical_id: str):
        """
        A hierarchy specifies allowed parent/child asset relationships.
        :param str child_asset_id: The ID of the child asset to be associated.
        :param str logical_id: The LogicalID of a hierarchy in the parent asset's model.
        """
        pulumi.set(__self__, "child_asset_id", child_asset_id)
        pulumi.set(__self__, "logical_id", logical_id)

    @property
    @pulumi.getter(name="childAssetId")
    def child_asset_id(self) -> str:
        """
        The ID of the child asset to be associated.
        """
        return pulumi.get(self, "child_asset_id")

    @property
    @pulumi.getter(name="logicalId")
    def logical_id(self) -> str:
        """
        The LogicalID of a hierarchy in the parent asset's model.
        """
        return pulumi.get(self, "logical_id")


@pulumi.output_type
class AssetModelAttribute(dict):
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "defaultValue":
            suggest = "default_value"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in AssetModelAttribute. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        AssetModelAttribute.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        AssetModelAttribute.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 default_value: Optional[str] = None):
        if default_value is not None:
            pulumi.set(__self__, "default_value", default_value)

    @property
    @pulumi.getter(name="defaultValue")
    def default_value(self) -> Optional[str]:
        return pulumi.get(self, "default_value")


@pulumi.output_type
class AssetModelCompositeModel(dict):
    """
    Contains a composite model definition in an asset model. This composite model definition is applied to all assets created from the asset model.
    """
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "compositeModelProperties":
            suggest = "composite_model_properties"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in AssetModelCompositeModel. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        AssetModelCompositeModel.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        AssetModelCompositeModel.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 name: str,
                 type: str,
                 composite_model_properties: Optional[Sequence['outputs.AssetModelProperty']] = None,
                 description: Optional[str] = None):
        """
        Contains a composite model definition in an asset model. This composite model definition is applied to all assets created from the asset model.
        :param str name: A unique, friendly name for the asset composite model.
        :param str type: The type of the composite model. For alarm composite models, this type is AWS/ALARM
        :param Sequence['AssetModelProperty'] composite_model_properties: The property definitions of the asset model. You can specify up to 200 properties per asset model.
        :param str description: A description for the asset composite model.
        """
        pulumi.set(__self__, "name", name)
        pulumi.set(__self__, "type", type)
        if composite_model_properties is not None:
            pulumi.set(__self__, "composite_model_properties", composite_model_properties)
        if description is not None:
            pulumi.set(__self__, "description", description)

    @property
    @pulumi.getter
    def name(self) -> str:
        """
        A unique, friendly name for the asset composite model.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def type(self) -> str:
        """
        The type of the composite model. For alarm composite models, this type is AWS/ALARM
        """
        return pulumi.get(self, "type")

    @property
    @pulumi.getter(name="compositeModelProperties")
    def composite_model_properties(self) -> Optional[Sequence['outputs.AssetModelProperty']]:
        """
        The property definitions of the asset model. You can specify up to 200 properties per asset model.
        """
        return pulumi.get(self, "composite_model_properties")

    @property
    @pulumi.getter
    def description(self) -> Optional[str]:
        """
        A description for the asset composite model.
        """
        return pulumi.get(self, "description")


@pulumi.output_type
class AssetModelExpressionVariable(dict):
    def __init__(__self__, *,
                 name: str,
                 value: 'outputs.AssetModelVariableValue'):
        """
        :param str name: The friendly name of the variable to be used in the expression.
        :param 'AssetModelVariableValue' value: The variable that identifies an asset property from which to use values.
        """
        pulumi.set(__self__, "name", name)
        pulumi.set(__self__, "value", value)

    @property
    @pulumi.getter
    def name(self) -> str:
        """
        The friendly name of the variable to be used in the expression.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def value(self) -> 'outputs.AssetModelVariableValue':
        """
        The variable that identifies an asset property from which to use values.
        """
        return pulumi.get(self, "value")


@pulumi.output_type
class AssetModelHierarchy(dict):
    """
    Contains information about an asset model hierarchy.
    """
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "childAssetModelId":
            suggest = "child_asset_model_id"
        elif key == "logicalId":
            suggest = "logical_id"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in AssetModelHierarchy. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        AssetModelHierarchy.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        AssetModelHierarchy.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 child_asset_model_id: str,
                 logical_id: str,
                 name: str):
        """
        Contains information about an asset model hierarchy.
        :param str child_asset_model_id: The ID of the asset model. All assets in this hierarchy must be instances of the child AssetModelId asset model.
        :param str logical_id: Customer provided ID for hierarchy.
        :param str name: The name of the asset model hierarchy.
        """
        pulumi.set(__self__, "child_asset_model_id", child_asset_model_id)
        pulumi.set(__self__, "logical_id", logical_id)
        pulumi.set(__self__, "name", name)

    @property
    @pulumi.getter(name="childAssetModelId")
    def child_asset_model_id(self) -> str:
        """
        The ID of the asset model. All assets in this hierarchy must be instances of the child AssetModelId asset model.
        """
        return pulumi.get(self, "child_asset_model_id")

    @property
    @pulumi.getter(name="logicalId")
    def logical_id(self) -> str:
        """
        Customer provided ID for hierarchy.
        """
        return pulumi.get(self, "logical_id")

    @property
    @pulumi.getter
    def name(self) -> str:
        """
        The name of the asset model hierarchy.
        """
        return pulumi.get(self, "name")


@pulumi.output_type
class AssetModelMetric(dict):
    def __init__(__self__, *,
                 expression: str,
                 variables: Sequence['outputs.AssetModelExpressionVariable'],
                 window: 'outputs.AssetModelMetricWindow'):
        """
        :param str expression: The mathematical expression that defines the metric aggregation function. You can specify up to 10 functions per expression.
        :param Sequence['AssetModelExpressionVariable'] variables: The list of variables used in the expression.
        :param 'AssetModelMetricWindow' window: The window (time interval) over which AWS IoT SiteWise computes the metric's aggregation expression
        """
        pulumi.set(__self__, "expression", expression)
        pulumi.set(__self__, "variables", variables)
        pulumi.set(__self__, "window", window)

    @property
    @pulumi.getter
    def expression(self) -> str:
        """
        The mathematical expression that defines the metric aggregation function. You can specify up to 10 functions per expression.
        """
        return pulumi.get(self, "expression")

    @property
    @pulumi.getter
    def variables(self) -> Sequence['outputs.AssetModelExpressionVariable']:
        """
        The list of variables used in the expression.
        """
        return pulumi.get(self, "variables")

    @property
    @pulumi.getter
    def window(self) -> 'outputs.AssetModelMetricWindow':
        """
        The window (time interval) over which AWS IoT SiteWise computes the metric's aggregation expression
        """
        return pulumi.get(self, "window")


@pulumi.output_type
class AssetModelMetricWindow(dict):
    """
    Contains a time interval window used for data aggregate computations (for example, average, sum, count, and so on).
    """
    def __init__(__self__, *,
                 tumbling: Optional['outputs.AssetModelTumblingWindow'] = None):
        """
        Contains a time interval window used for data aggregate computations (for example, average, sum, count, and so on).
        """
        if tumbling is not None:
            pulumi.set(__self__, "tumbling", tumbling)

    @property
    @pulumi.getter
    def tumbling(self) -> Optional['outputs.AssetModelTumblingWindow']:
        return pulumi.get(self, "tumbling")


@pulumi.output_type
class AssetModelProperty(dict):
    """
    Contains information about an asset model property.
    """
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "dataType":
            suggest = "data_type"
        elif key == "logicalId":
            suggest = "logical_id"
        elif key == "dataTypeSpec":
            suggest = "data_type_spec"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in AssetModelProperty. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        AssetModelProperty.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        AssetModelProperty.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 data_type: 'AssetModelDataType',
                 logical_id: str,
                 name: str,
                 type: 'outputs.AssetModelPropertyType',
                 data_type_spec: Optional['AssetModelDataTypeSpec'] = None,
                 unit: Optional[str] = None):
        """
        Contains information about an asset model property.
        :param 'AssetModelDataType' data_type: The data type of the asset model property.
        :param str logical_id: Customer provided ID for property.
        :param str name: The name of the asset model property.
        :param 'AssetModelPropertyType' type: The property type
        :param 'AssetModelDataTypeSpec' data_type_spec: The data type of the structure for this property.
        :param str unit: The unit of the asset model property, such as Newtons or RPM.
        """
        pulumi.set(__self__, "data_type", data_type)
        pulumi.set(__self__, "logical_id", logical_id)
        pulumi.set(__self__, "name", name)
        pulumi.set(__self__, "type", type)
        if data_type_spec is not None:
            pulumi.set(__self__, "data_type_spec", data_type_spec)
        if unit is not None:
            pulumi.set(__self__, "unit", unit)

    @property
    @pulumi.getter(name="dataType")
    def data_type(self) -> 'AssetModelDataType':
        """
        The data type of the asset model property.
        """
        return pulumi.get(self, "data_type")

    @property
    @pulumi.getter(name="logicalId")
    def logical_id(self) -> str:
        """
        Customer provided ID for property.
        """
        return pulumi.get(self, "logical_id")

    @property
    @pulumi.getter
    def name(self) -> str:
        """
        The name of the asset model property.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def type(self) -> 'outputs.AssetModelPropertyType':
        """
        The property type
        """
        return pulumi.get(self, "type")

    @property
    @pulumi.getter(name="dataTypeSpec")
    def data_type_spec(self) -> Optional['AssetModelDataTypeSpec']:
        """
        The data type of the structure for this property.
        """
        return pulumi.get(self, "data_type_spec")

    @property
    @pulumi.getter
    def unit(self) -> Optional[str]:
        """
        The unit of the asset model property, such as Newtons or RPM.
        """
        return pulumi.get(self, "unit")


@pulumi.output_type
class AssetModelPropertyType(dict):
    """
    Contains a property type, which can be one of attribute, measurement, metric, or transform.
    """
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "typeName":
            suggest = "type_name"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in AssetModelPropertyType. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        AssetModelPropertyType.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        AssetModelPropertyType.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 type_name: 'AssetModelTypeName',
                 attribute: Optional['outputs.AssetModelAttribute'] = None,
                 metric: Optional['outputs.AssetModelMetric'] = None,
                 transform: Optional['outputs.AssetModelTransform'] = None):
        """
        Contains a property type, which can be one of attribute, measurement, metric, or transform.
        """
        pulumi.set(__self__, "type_name", type_name)
        if attribute is not None:
            pulumi.set(__self__, "attribute", attribute)
        if metric is not None:
            pulumi.set(__self__, "metric", metric)
        if transform is not None:
            pulumi.set(__self__, "transform", transform)

    @property
    @pulumi.getter(name="typeName")
    def type_name(self) -> 'AssetModelTypeName':
        return pulumi.get(self, "type_name")

    @property
    @pulumi.getter
    def attribute(self) -> Optional['outputs.AssetModelAttribute']:
        return pulumi.get(self, "attribute")

    @property
    @pulumi.getter
    def metric(self) -> Optional['outputs.AssetModelMetric']:
        return pulumi.get(self, "metric")

    @property
    @pulumi.getter
    def transform(self) -> Optional['outputs.AssetModelTransform']:
        return pulumi.get(self, "transform")


@pulumi.output_type
class AssetModelTag(dict):
    def __init__(__self__, *,
                 key: str,
                 value: str):
        pulumi.set(__self__, "key", key)
        pulumi.set(__self__, "value", value)

    @property
    @pulumi.getter
    def key(self) -> str:
        return pulumi.get(self, "key")

    @property
    @pulumi.getter
    def value(self) -> str:
        return pulumi.get(self, "value")


@pulumi.output_type
class AssetModelTransform(dict):
    def __init__(__self__, *,
                 expression: str,
                 variables: Sequence['outputs.AssetModelExpressionVariable']):
        """
        :param str expression: The mathematical expression that defines the transformation function. You can specify up to 10 functions per expression.
        :param Sequence['AssetModelExpressionVariable'] variables: The list of variables used in the expression.
        """
        pulumi.set(__self__, "expression", expression)
        pulumi.set(__self__, "variables", variables)

    @property
    @pulumi.getter
    def expression(self) -> str:
        """
        The mathematical expression that defines the transformation function. You can specify up to 10 functions per expression.
        """
        return pulumi.get(self, "expression")

    @property
    @pulumi.getter
    def variables(self) -> Sequence['outputs.AssetModelExpressionVariable']:
        """
        The list of variables used in the expression.
        """
        return pulumi.get(self, "variables")


@pulumi.output_type
class AssetModelTumblingWindow(dict):
    """
    Contains a tumbling window, which is a repeating fixed-sized, non-overlapping, and contiguous time interval. This window is used in metric and aggregation computations.
    """
    def __init__(__self__, *,
                 interval: str,
                 offset: Optional[str] = None):
        """
        Contains a tumbling window, which is a repeating fixed-sized, non-overlapping, and contiguous time interval. This window is used in metric and aggregation computations.
        """
        pulumi.set(__self__, "interval", interval)
        if offset is not None:
            pulumi.set(__self__, "offset", offset)

    @property
    @pulumi.getter
    def interval(self) -> str:
        return pulumi.get(self, "interval")

    @property
    @pulumi.getter
    def offset(self) -> Optional[str]:
        return pulumi.get(self, "offset")


@pulumi.output_type
class AssetModelVariableValue(dict):
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "propertyLogicalId":
            suggest = "property_logical_id"
        elif key == "hierarchyLogicalId":
            suggest = "hierarchy_logical_id"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in AssetModelVariableValue. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        AssetModelVariableValue.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        AssetModelVariableValue.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 property_logical_id: str,
                 hierarchy_logical_id: Optional[str] = None):
        pulumi.set(__self__, "property_logical_id", property_logical_id)
        if hierarchy_logical_id is not None:
            pulumi.set(__self__, "hierarchy_logical_id", hierarchy_logical_id)

    @property
    @pulumi.getter(name="propertyLogicalId")
    def property_logical_id(self) -> str:
        return pulumi.get(self, "property_logical_id")

    @property
    @pulumi.getter(name="hierarchyLogicalId")
    def hierarchy_logical_id(self) -> Optional[str]:
        return pulumi.get(self, "hierarchy_logical_id")


@pulumi.output_type
class AssetProperty(dict):
    """
    The asset property's definition, alias, and notification state.
    """
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "logicalId":
            suggest = "logical_id"
        elif key == "notificationState":
            suggest = "notification_state"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in AssetProperty. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        AssetProperty.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        AssetProperty.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 logical_id: str,
                 alias: Optional[str] = None,
                 notification_state: Optional['AssetPropertyNotificationState'] = None):
        """
        The asset property's definition, alias, and notification state.
        :param str logical_id: Customer provided ID for property.
        :param str alias: The property alias that identifies the property.
        :param 'AssetPropertyNotificationState' notification_state: The MQTT notification state (ENABLED or DISABLED) for this asset property.
        """
        pulumi.set(__self__, "logical_id", logical_id)
        if alias is not None:
            pulumi.set(__self__, "alias", alias)
        if notification_state is not None:
            pulumi.set(__self__, "notification_state", notification_state)

    @property
    @pulumi.getter(name="logicalId")
    def logical_id(self) -> str:
        """
        Customer provided ID for property.
        """
        return pulumi.get(self, "logical_id")

    @property
    @pulumi.getter
    def alias(self) -> Optional[str]:
        """
        The property alias that identifies the property.
        """
        return pulumi.get(self, "alias")

    @property
    @pulumi.getter(name="notificationState")
    def notification_state(self) -> Optional['AssetPropertyNotificationState']:
        """
        The MQTT notification state (ENABLED or DISABLED) for this asset property.
        """
        return pulumi.get(self, "notification_state")


@pulumi.output_type
class AssetTag(dict):
    def __init__(__self__, *,
                 key: str,
                 value: str):
        pulumi.set(__self__, "key", key)
        pulumi.set(__self__, "value", value)

    @property
    @pulumi.getter
    def key(self) -> str:
        return pulumi.get(self, "key")

    @property
    @pulumi.getter
    def value(self) -> str:
        return pulumi.get(self, "value")


@pulumi.output_type
class DashboardTag(dict):
    """
    To add or update tag, provide both key and value. To delete tag, provide only tag key to be deleted
    """
    def __init__(__self__, *,
                 key: str,
                 value: str):
        """
        To add or update tag, provide both key and value. To delete tag, provide only tag key to be deleted
        """
        pulumi.set(__self__, "key", key)
        pulumi.set(__self__, "value", value)

    @property
    @pulumi.getter
    def key(self) -> str:
        return pulumi.get(self, "key")

    @property
    @pulumi.getter
    def value(self) -> str:
        return pulumi.get(self, "value")


@pulumi.output_type
class GatewayCapabilitySummary(dict):
    """
    Contains a summary of a gateway capability configuration.
    """
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "capabilityNamespace":
            suggest = "capability_namespace"
        elif key == "capabilityConfiguration":
            suggest = "capability_configuration"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in GatewayCapabilitySummary. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        GatewayCapabilitySummary.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        GatewayCapabilitySummary.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 capability_namespace: str,
                 capability_configuration: Optional[str] = None):
        """
        Contains a summary of a gateway capability configuration.
        """
        pulumi.set(__self__, "capability_namespace", capability_namespace)
        if capability_configuration is not None:
            pulumi.set(__self__, "capability_configuration", capability_configuration)

    @property
    @pulumi.getter(name="capabilityNamespace")
    def capability_namespace(self) -> str:
        return pulumi.get(self, "capability_namespace")

    @property
    @pulumi.getter(name="capabilityConfiguration")
    def capability_configuration(self) -> Optional[str]:
        return pulumi.get(self, "capability_configuration")


@pulumi.output_type
class GatewayGreengrass(dict):
    """
    Contains the ARN of AWS IoT Greengrass Group that the gateway runs on.
    """
    @staticmethod
    def __key_warning(key: str):
        suggest = None
        if key == "groupArn":
            suggest = "group_arn"

        if suggest:
            pulumi.log.warn(f"Key '{key}' not found in GatewayGreengrass. Access the value via the '{suggest}' property getter instead.")

    def __getitem__(self, key: str) -> Any:
        GatewayGreengrass.__key_warning(key)
        return super().__getitem__(key)

    def get(self, key: str, default = None) -> Any:
        GatewayGreengrass.__key_warning(key)
        return super().get(key, default)

    def __init__(__self__, *,
                 group_arn: str):
        """
        Contains the ARN of AWS IoT Greengrass Group that the gateway runs on.
        :param str group_arn: The ARN of the Greengrass group.
        """
        pulumi.set(__self__, "group_arn", group_arn)

    @property
    @pulumi.getter(name="groupArn")
    def group_arn(self) -> str:
        """
        The ARN of the Greengrass group.
        """
        return pulumi.get(self, "group_arn")


@pulumi.output_type
class GatewayPlatform(dict):
    """
    Contains a gateway's platform information.
    """
    def __init__(__self__, *,
                 greengrass: 'outputs.GatewayGreengrass'):
        """
        Contains a gateway's platform information.
        :param 'GatewayGreengrass' greengrass: A gateway that runs on AWS IoT Greengrass.
        """
        pulumi.set(__self__, "greengrass", greengrass)

    @property
    @pulumi.getter
    def greengrass(self) -> 'outputs.GatewayGreengrass':
        """
        A gateway that runs on AWS IoT Greengrass.
        """
        return pulumi.get(self, "greengrass")


@pulumi.output_type
class GatewayTag(dict):
    """
    To add or update tag, provide both key and value. To delete tag, provide only tag key to be deleted
    """
    def __init__(__self__, *,
                 key: str,
                 value: str):
        """
        To add or update tag, provide both key and value. To delete tag, provide only tag key to be deleted
        """
        pulumi.set(__self__, "key", key)
        pulumi.set(__self__, "value", value)

    @property
    @pulumi.getter
    def key(self) -> str:
        return pulumi.get(self, "key")

    @property
    @pulumi.getter
    def value(self) -> str:
        return pulumi.get(self, "value")


@pulumi.output_type
class PortalTag(dict):
    """
    To add or update tag, provide both key and value. To delete tag, provide only tag key to be deleted.
    """
    def __init__(__self__, *,
                 key: str,
                 value: str):
        """
        To add or update tag, provide both key and value. To delete tag, provide only tag key to be deleted.
        """
        pulumi.set(__self__, "key", key)
        pulumi.set(__self__, "value", value)

    @property
    @pulumi.getter
    def key(self) -> str:
        return pulumi.get(self, "key")

    @property
    @pulumi.getter
    def value(self) -> str:
        return pulumi.get(self, "value")


@pulumi.output_type
class ProjectTag(dict):
    """
    To add or update tag, provide both key and value. To delete tag, provide only tag key to be deleted
    """
    def __init__(__self__, *,
                 key: str,
                 value: str):
        """
        To add or update tag, provide both key and value. To delete tag, provide only tag key to be deleted
        """
        pulumi.set(__self__, "key", key)
        pulumi.set(__self__, "value", value)

    @property
    @pulumi.getter
    def key(self) -> str:
        return pulumi.get(self, "key")

    @property
    @pulumi.getter
    def value(self) -> str:
        return pulumi.get(self, "value")


