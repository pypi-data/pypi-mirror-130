from dataclasses import dataclass, field

from typing import Any, Callable, List, Optional
import numpy as np

from leapcli.dataset.contract import DatasetInputType, DatasetOutputType, DatasetMetadataType


@dataclass
class SubsetResponse:
    length: int
    data: Any


SectionCallableInterface = Callable[[int, SubsetResponse], np.ndarray]


@dataclass
class SubsetHandler:
    ratio: float
    function: Callable[[], List[SubsetResponse]]
    name: str


@dataclass
class DatasetBaseHandler:
    name: str
    function: SectionCallableInterface
    subset: str


@dataclass
class InputHandler(DatasetBaseHandler):
    type: DatasetInputType
    shape: Optional[List[int]]


@dataclass
class GroundTruthHandler(DatasetBaseHandler):
    type: DatasetOutputType
    labels: List[str]
    masked_input: Optional[str]
    shape: Optional[List[int]]


@dataclass
class MetadataHandler(DatasetBaseHandler):
    type: DatasetMetadataType


@dataclass
class  DatasetIntegrationSetup:
    subsets: List[SubsetHandler] = field(default_factory=list)
    inputs: List[InputHandler] = field(default_factory=list)
    ground_truths: List[GroundTruthHandler] = field(default_factory=list)
    metadata: List[MetadataHandler] = field(default_factory=list)


class DatasetBinder:

    def __init__(self):
        self._container = DatasetIntegrationSetup()

    def set_subset(self, ratio: float, function: Callable[[None], List[SubsetResponse]], name: str) -> None:
        self._container.subsets.append(SubsetHandler(ratio, function, name))

    def set_input(self, function: SectionCallableInterface, subset: str,
                  input_type: DatasetInputType, name: str) -> None:
        self._container.inputs.append(InputHandler(name, function, subset, input_type, []))

    def set_ground_truth(self, function: SectionCallableInterface, subset: str,
                         ground_truth_type: DatasetOutputType, name: str, labels: List[str],
                         masked_input: Optional[str]) -> None:
        self._container.ground_truths.append(GroundTruthHandler(name, function, subset,
                                                                ground_truth_type, labels, masked_input, []))

    def set_metadata(self, function: SectionCallableInterface, subset: str,
                     metadata_type: DatasetMetadataType, name: str) -> None:
        self._container.metadata.append(MetadataHandler(name, function, subset, metadata_type))
