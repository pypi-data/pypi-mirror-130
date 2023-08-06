from enum import Enum
from typing import List, Dict, Optional

from dataclasses import dataclass


class DatasetOutputType(Enum):
    Numeric = "Numeric"
    Classes = "Classes"
    Mask = "Mask"


class DatasetInputType(Enum):
    Image = "Image"
    Text = "Text"
    Word = "Word"
    Numeric = "Numeric"
    Time_series = "Time_series"


class DatasetParameterType(Enum):
    Number = "Number"
    Select = "Select"
    String = "String"
    MultiSelect = "MultiSelect"


class DatasetMetadataType(Enum):
    float = "float"
    string = "string"
    int = "int"
    boolean = "boolean"


@dataclass
class DatasetSubsetInstance:
    id: str
    name: str
    ratio: float
    script: str


@dataclass
class DatasetBaseSectionInstance:
    id: str
    name: str
    script: str
    subset: str


@dataclass
class DatasetInputInstance(DatasetBaseSectionInstance):
    shape: List[int]
    type: DatasetInputType


@dataclass
class DatasetLibInstance:
    as_: str
    from_: str
    id: str
    import_: str


@dataclass
class DatasetMetadataInstance(DatasetBaseSectionInstance):
    type: DatasetMetadataType


@dataclass
class DatasetOutputInstance(DatasetBaseSectionInstance):
    shape: List[int]
    type: DatasetOutputType
    masked_input: Optional[str] = None
    labels: Optional[List[str]] = None


@dataclass
class DatasetParameterInstance:
    id: str
    name: str
    default_value: str
    type: DatasetParameterType


@dataclass
class DatasetSetup:
    inputs: List[DatasetInputInstance]
    libs: List[DatasetLibInstance]
    metadata: List[DatasetMetadataInstance]
    outputs: List[DatasetOutputInstance]
    parameters: List[DatasetParameterInstance]
    subsets: List[DatasetSubsetInstance]


class CloudProviderEnum(Enum):
    aws = "aws"
    gcloud = "gcloud"


@dataclass
class Secret:
    name: str
    cloud_provider: CloudProviderEnum
    auth_file_path: str


@dataclass
class BucketConfig:
    bucket: str
    secret: Secret


@dataclass
class DatasetRequest:
    name: str
    setup: DatasetSetup
    input_shape: Dict[str, List[int]]
    bucket_config: Optional[BucketConfig] = None
