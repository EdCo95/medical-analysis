from enum import Enum
from typing import Dict, List, Tuple, Union

from assess.utils import serialize


class CriteriaKey(Enum):
    DESCRIPTION = "description"
    CRITERIA = "criteria"


class AssessmentCriteria:
    """Class providing access to the data stored in an assessment TOML."""

    def __init__(self, critera: Dict[str, Union[str, Dict[str, str]]]):
        self.critera = critera

    def get_sections(self) -> List[Tuple[str, str]]:
        """Returns the section titles and their descriptions."""
        result = []
        for key, val in self.critera.items():
            if isinstance(val, str):
                continue
            result.append((key, val[CriteriaKey.CRITERIA.value]))
        return result

    def get_description(self) -> str:
        return self.critera[CriteriaKey.DESCRIPTION.value]

    @classmethod
    def from_spec(cls, spec_name: str) -> "AssessmentCriteria":
        raw_data = serialize.load_assesment_criteria(spec_name)
        return cls(critera=raw_data)
