from typing import List, Optional, Dict

from dataclasses import dataclass, field

from code_loader.contract.enums import DatasetInputType, DatasetMetadataType, DatasetOutputType


@dataclass
class DatasetSubsetInstance:
    name: str
    training_length: int
    validation_length: int
    test_length: Optional[int]


@dataclass
class DatasetBaseSectionInstance:
    name: str
    subset_name: str


@dataclass
class DatasetInputInstance(DatasetBaseSectionInstance):
    shape: List[int]
    type: DatasetInputType


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
class DatasetSetup:
    inputs: List[DatasetInputInstance]
    metadata: List[DatasetMetadataInstance]
    outputs: List[DatasetOutputInstance]
    subsets: List[DatasetSubsetInstance]


@dataclass
class DatasetTestResultPayload:
    name: str
    display: Dict[str, str] = field(default_factory=dict)
    is_passed: bool = True
    shape: Optional[List[int]] = None


@dataclass
class DatasetIntegParseResult:
    payloads: List[DatasetTestResultPayload]
    is_valid: bool
    setup: Optional[DatasetSetup]
    general_error: Optional[str]
