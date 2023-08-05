# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

from enum import Enum

__all__ = [
    'AppResourceSpecInstanceType',
    'AppType',
    'DataQualityJobDefinitionEndpointInputS3DataDistributionType',
    'DataQualityJobDefinitionEndpointInputS3InputMode',
    'DataQualityJobDefinitionS3OutputS3UploadMode',
    'DomainAppNetworkAccessType',
    'DomainAuthMode',
    'DomainResourceSpecInstanceType',
    'DomainSharingSettingsNotebookOutputOption',
    'FeatureGroupFeatureDefinitionFeatureType',
    'ModelBiasJobDefinitionEndpointInputS3DataDistributionType',
    'ModelBiasJobDefinitionEndpointInputS3InputMode',
    'ModelBiasJobDefinitionS3OutputS3UploadMode',
    'ModelExplainabilityJobDefinitionEndpointInputS3DataDistributionType',
    'ModelExplainabilityJobDefinitionEndpointInputS3InputMode',
    'ModelExplainabilityJobDefinitionS3OutputS3UploadMode',
    'ModelPackageGroupStatus',
    'ModelQualityJobDefinitionEndpointInputS3DataDistributionType',
    'ModelQualityJobDefinitionEndpointInputS3InputMode',
    'ModelQualityJobDefinitionProblemType',
    'ModelQualityJobDefinitionS3OutputS3UploadMode',
    'MonitoringScheduleEndpointInputS3DataDistributionType',
    'MonitoringScheduleEndpointInputS3InputMode',
    'MonitoringScheduleMonitoringExecutionSummaryMonitoringExecutionStatus',
    'MonitoringScheduleMonitoringType',
    'MonitoringScheduleS3OutputS3UploadMode',
    'MonitoringScheduleStatus',
    'ProjectStatus',
    'UserProfileResourceSpecInstanceType',
    'UserProfileSharingSettingsNotebookOutputOption',
]


class AppResourceSpecInstanceType(str, Enum):
    """
    The instance type that the image version runs on.
    """
    SYSTEM = "system"
    ML_T3_MICRO = "ml.t3.micro"
    ML_T3_SMALL = "ml.t3.small"
    ML_T3_MEDIUM = "ml.t3.medium"
    ML_T3_LARGE = "ml.t3.large"
    ML_T3_XLARGE = "ml.t3.xlarge"
    ML_T32XLARGE = "ml.t3.2xlarge"
    ML_M5_LARGE = "ml.m5.large"
    ML_M5_XLARGE = "ml.m5.xlarge"
    ML_M52XLARGE = "ml.m5.2xlarge"
    ML_M54XLARGE = "ml.m5.4xlarge"
    ML_M58XLARGE = "ml.m5.8xlarge"
    ML_M512XLARGE = "ml.m5.12xlarge"
    ML_M516XLARGE = "ml.m5.16xlarge"
    ML_M524XLARGE = "ml.m5.24xlarge"
    ML_C5_LARGE = "ml.c5.large"
    ML_C5_XLARGE = "ml.c5.xlarge"
    ML_C52XLARGE = "ml.c5.2xlarge"
    ML_C54XLARGE = "ml.c5.4xlarge"
    ML_C59XLARGE = "ml.c5.9xlarge"
    ML_C512XLARGE = "ml.c5.12xlarge"
    ML_C518XLARGE = "ml.c5.18xlarge"
    ML_C524XLARGE = "ml.c5.24xlarge"
    ML_P32XLARGE = "ml.p3.2xlarge"
    ML_P38XLARGE = "ml.p3.8xlarge"
    ML_P316XLARGE = "ml.p3.16xlarge"
    ML_G4DN_XLARGE = "ml.g4dn.xlarge"
    ML_G4DN2XLARGE = "ml.g4dn.2xlarge"
    ML_G4DN4XLARGE = "ml.g4dn.4xlarge"
    ML_G4DN8XLARGE = "ml.g4dn.8xlarge"
    ML_G4DN12XLARGE = "ml.g4dn.12xlarge"
    ML_G4DN16XLARGE = "ml.g4dn.16xlarge"


class AppType(str, Enum):
    """
    The type of app.
    """
    JUPYTER_SERVER = "JupyterServer"
    KERNEL_GATEWAY = "KernelGateway"


class DataQualityJobDefinitionEndpointInputS3DataDistributionType(str, Enum):
    """
    Whether input data distributed in Amazon S3 is fully replicated or sharded by an S3 key. Defauts to FullyReplicated
    """
    FULLY_REPLICATED = "FullyReplicated"
    SHARDED_BY_S3_KEY = "ShardedByS3Key"


class DataQualityJobDefinitionEndpointInputS3InputMode(str, Enum):
    """
    Whether the Pipe or File is used as the input mode for transfering data for the monitoring job. Pipe mode is recommended for large datasets. File mode is useful for small files that fit in memory. Defaults to File.
    """
    PIPE = "Pipe"
    FILE = "File"


class DataQualityJobDefinitionS3OutputS3UploadMode(str, Enum):
    """
    Whether to upload the results of the monitoring job continuously or after the job completes.
    """
    CONTINUOUS = "Continuous"
    END_OF_JOB = "EndOfJob"


class DomainAppNetworkAccessType(str, Enum):
    """
    Specifies the VPC used for non-EFS traffic. The default value is PublicInternetOnly.
    """
    PUBLIC_INTERNET_ONLY = "PublicInternetOnly"
    VPC_ONLY = "VpcOnly"


class DomainAuthMode(str, Enum):
    """
    The mode of authentication that members use to access the domain.
    """
    SSO = "SSO"
    IAM = "IAM"


class DomainResourceSpecInstanceType(str, Enum):
    """
    The instance type that the image version runs on.
    """
    SYSTEM = "system"
    ML_T3_MICRO = "ml.t3.micro"
    ML_T3_SMALL = "ml.t3.small"
    ML_T3_MEDIUM = "ml.t3.medium"
    ML_T3_LARGE = "ml.t3.large"
    ML_T3_XLARGE = "ml.t3.xlarge"
    ML_T32XLARGE = "ml.t3.2xlarge"
    ML_M5_LARGE = "ml.m5.large"
    ML_M5_XLARGE = "ml.m5.xlarge"
    ML_M52XLARGE = "ml.m5.2xlarge"
    ML_M54XLARGE = "ml.m5.4xlarge"
    ML_M58XLARGE = "ml.m5.8xlarge"
    ML_M512XLARGE = "ml.m5.12xlarge"
    ML_M516XLARGE = "ml.m5.16xlarge"
    ML_M524XLARGE = "ml.m5.24xlarge"
    ML_C5_LARGE = "ml.c5.large"
    ML_C5_XLARGE = "ml.c5.xlarge"
    ML_C52XLARGE = "ml.c5.2xlarge"
    ML_C54XLARGE = "ml.c5.4xlarge"
    ML_C59XLARGE = "ml.c5.9xlarge"
    ML_C512XLARGE = "ml.c5.12xlarge"
    ML_C518XLARGE = "ml.c5.18xlarge"
    ML_C524XLARGE = "ml.c5.24xlarge"
    ML_P32XLARGE = "ml.p3.2xlarge"
    ML_P38XLARGE = "ml.p3.8xlarge"
    ML_P316XLARGE = "ml.p3.16xlarge"
    ML_G4DN_XLARGE = "ml.g4dn.xlarge"
    ML_G4DN2XLARGE = "ml.g4dn.2xlarge"
    ML_G4DN4XLARGE = "ml.g4dn.4xlarge"
    ML_G4DN8XLARGE = "ml.g4dn.8xlarge"
    ML_G4DN12XLARGE = "ml.g4dn.12xlarge"
    ML_G4DN16XLARGE = "ml.g4dn.16xlarge"


class DomainSharingSettingsNotebookOutputOption(str, Enum):
    """
    Whether to include the notebook cell output when sharing the notebook. The default is Disabled.
    """
    ALLOWED = "Allowed"
    DISABLED = "Disabled"


class FeatureGroupFeatureDefinitionFeatureType(str, Enum):
    INTEGRAL = "Integral"
    FRACTIONAL = "Fractional"
    STRING = "String"


class ModelBiasJobDefinitionEndpointInputS3DataDistributionType(str, Enum):
    """
    Whether input data distributed in Amazon S3 is fully replicated or sharded by an S3 key. Defauts to FullyReplicated
    """
    FULLY_REPLICATED = "FullyReplicated"
    SHARDED_BY_S3_KEY = "ShardedByS3Key"


class ModelBiasJobDefinitionEndpointInputS3InputMode(str, Enum):
    """
    Whether the Pipe or File is used as the input mode for transfering data for the monitoring job. Pipe mode is recommended for large datasets. File mode is useful for small files that fit in memory. Defaults to File.
    """
    PIPE = "Pipe"
    FILE = "File"


class ModelBiasJobDefinitionS3OutputS3UploadMode(str, Enum):
    """
    Whether to upload the results of the monitoring job continuously or after the job completes.
    """
    CONTINUOUS = "Continuous"
    END_OF_JOB = "EndOfJob"


class ModelExplainabilityJobDefinitionEndpointInputS3DataDistributionType(str, Enum):
    """
    Whether input data distributed in Amazon S3 is fully replicated or sharded by an S3 key. Defauts to FullyReplicated
    """
    FULLY_REPLICATED = "FullyReplicated"
    SHARDED_BY_S3_KEY = "ShardedByS3Key"


class ModelExplainabilityJobDefinitionEndpointInputS3InputMode(str, Enum):
    """
    Whether the Pipe or File is used as the input mode for transfering data for the monitoring job. Pipe mode is recommended for large datasets. File mode is useful for small files that fit in memory. Defaults to File.
    """
    PIPE = "Pipe"
    FILE = "File"


class ModelExplainabilityJobDefinitionS3OutputS3UploadMode(str, Enum):
    """
    Whether to upload the results of the monitoring job continuously or after the job completes.
    """
    CONTINUOUS = "Continuous"
    END_OF_JOB = "EndOfJob"


class ModelPackageGroupStatus(str, Enum):
    """
    The status of a modelpackage group job.
    """
    PENDING = "Pending"
    IN_PROGRESS = "InProgress"
    COMPLETED = "Completed"
    FAILED = "Failed"
    DELETING = "Deleting"
    DELETE_FAILED = "DeleteFailed"


class ModelQualityJobDefinitionEndpointInputS3DataDistributionType(str, Enum):
    """
    Whether input data distributed in Amazon S3 is fully replicated or sharded by an S3 key. Defauts to FullyReplicated
    """
    FULLY_REPLICATED = "FullyReplicated"
    SHARDED_BY_S3_KEY = "ShardedByS3Key"


class ModelQualityJobDefinitionEndpointInputS3InputMode(str, Enum):
    """
    Whether the Pipe or File is used as the input mode for transfering data for the monitoring job. Pipe mode is recommended for large datasets. File mode is useful for small files that fit in memory. Defaults to File.
    """
    PIPE = "Pipe"
    FILE = "File"


class ModelQualityJobDefinitionProblemType(str, Enum):
    """
    The status of the monitoring job.
    """
    BINARY_CLASSIFICATION = "BinaryClassification"
    MULTICLASS_CLASSIFICATION = "MulticlassClassification"
    REGRESSION = "Regression"


class ModelQualityJobDefinitionS3OutputS3UploadMode(str, Enum):
    """
    Whether to upload the results of the monitoring job continuously or after the job completes.
    """
    CONTINUOUS = "Continuous"
    END_OF_JOB = "EndOfJob"


class MonitoringScheduleEndpointInputS3DataDistributionType(str, Enum):
    """
    Whether input data distributed in Amazon S3 is fully replicated or sharded by an S3 key. Defauts to FullyReplicated
    """
    FULLY_REPLICATED = "FullyReplicated"
    SHARDED_BY_S3_KEY = "ShardedByS3Key"


class MonitoringScheduleEndpointInputS3InputMode(str, Enum):
    """
    Whether the Pipe or File is used as the input mode for transfering data for the monitoring job. Pipe mode is recommended for large datasets. File mode is useful for small files that fit in memory. Defaults to File.
    """
    PIPE = "Pipe"
    FILE = "File"


class MonitoringScheduleMonitoringExecutionSummaryMonitoringExecutionStatus(str, Enum):
    """
    The status of the monitoring job.
    """
    PENDING = "Pending"
    COMPLETED = "Completed"
    COMPLETED_WITH_VIOLATIONS = "CompletedWithViolations"
    IN_PROGRESS = "InProgress"
    FAILED = "Failed"
    STOPPING = "Stopping"
    STOPPED = "Stopped"


class MonitoringScheduleMonitoringType(str, Enum):
    """
    The type of monitoring job.
    """
    DATA_QUALITY = "DataQuality"
    MODEL_QUALITY = "ModelQuality"
    MODEL_BIAS = "ModelBias"
    MODEL_EXPLAINABILITY = "ModelExplainability"


class MonitoringScheduleS3OutputS3UploadMode(str, Enum):
    """
    Whether to upload the results of the monitoring job continuously or after the job completes.
    """
    CONTINUOUS = "Continuous"
    END_OF_JOB = "EndOfJob"


class MonitoringScheduleStatus(str, Enum):
    """
    The status of a schedule job.
    """
    PENDING = "Pending"
    FAILED = "Failed"
    SCHEDULED = "Scheduled"
    STOPPED = "Stopped"


class ProjectStatus(str, Enum):
    """
    The status of a project.
    """
    PENDING = "Pending"
    CREATE_IN_PROGRESS = "CreateInProgress"
    CREATE_COMPLETED = "CreateCompleted"
    CREATE_FAILED = "CreateFailed"
    DELETE_IN_PROGRESS = "DeleteInProgress"
    DELETE_FAILED = "DeleteFailed"
    DELETE_COMPLETED = "DeleteCompleted"


class UserProfileResourceSpecInstanceType(str, Enum):
    """
    The instance type that the image version runs on.
    """
    SYSTEM = "system"
    ML_T3_MICRO = "ml.t3.micro"
    ML_T3_SMALL = "ml.t3.small"
    ML_T3_MEDIUM = "ml.t3.medium"
    ML_T3_LARGE = "ml.t3.large"
    ML_T3_XLARGE = "ml.t3.xlarge"
    ML_T32XLARGE = "ml.t3.2xlarge"
    ML_M5_LARGE = "ml.m5.large"
    ML_M5_XLARGE = "ml.m5.xlarge"
    ML_M52XLARGE = "ml.m5.2xlarge"
    ML_M54XLARGE = "ml.m5.4xlarge"
    ML_M58XLARGE = "ml.m5.8xlarge"
    ML_M512XLARGE = "ml.m5.12xlarge"
    ML_M516XLARGE = "ml.m5.16xlarge"
    ML_M524XLARGE = "ml.m5.24xlarge"
    ML_C5_LARGE = "ml.c5.large"
    ML_C5_XLARGE = "ml.c5.xlarge"
    ML_C52XLARGE = "ml.c5.2xlarge"
    ML_C54XLARGE = "ml.c5.4xlarge"
    ML_C59XLARGE = "ml.c5.9xlarge"
    ML_C512XLARGE = "ml.c5.12xlarge"
    ML_C518XLARGE = "ml.c5.18xlarge"
    ML_C524XLARGE = "ml.c5.24xlarge"
    ML_P32XLARGE = "ml.p3.2xlarge"
    ML_P38XLARGE = "ml.p3.8xlarge"
    ML_P316XLARGE = "ml.p3.16xlarge"
    ML_G4DN_XLARGE = "ml.g4dn.xlarge"
    ML_G4DN2XLARGE = "ml.g4dn.2xlarge"
    ML_G4DN4XLARGE = "ml.g4dn.4xlarge"
    ML_G4DN8XLARGE = "ml.g4dn.8xlarge"
    ML_G4DN12XLARGE = "ml.g4dn.12xlarge"
    ML_G4DN16XLARGE = "ml.g4dn.16xlarge"


class UserProfileSharingSettingsNotebookOutputOption(str, Enum):
    """
    Whether to include the notebook cell output when sharing the notebook. The default is Disabled.
    """
    ALLOWED = "Allowed"
    DISABLED = "Disabled"
