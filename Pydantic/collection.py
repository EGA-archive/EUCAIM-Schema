import re
import argparse
from dateutil.parser import parse
from pydantic import (
    BaseModel,
    ValidationError,
    field_validator,
    PrivateAttr
)

from typing import Optional, Union, List

class OntologyTerm(BaseModel, extra='forbid'):
    id: str
    label: Optional[str]=None
    @field_validator('id')
    @classmethod
    def id_must_be_CURIE(cls, v: str) -> str:
        if re.match("[A-Za-z0-9]+:[A-Za-z0-9]", v):
            pass
        else:
            raise ValueError('id must be CURIE, e.g. NCIT:C42331')
        return v

class AgeRange(BaseModel, extra='forbid'):
    min: float
    max: float

class Collection(BaseModel, extra='forbid'):
    def __init__(self, **data) -> None:
        for private_key in self.__class__.__private_attributes__.keys():
            try:
                value = data.pop(private_key)
            except KeyError:
                pass

        super().__init__(**data)
    _id: Optional[str] = PrivateAttr()
    name: str
    id: str
    description: Optional[str] = None
    ageRange:AgeRange
    modalities: List
    bodyParts: List
    gender: List
    @field_validator('modalities')
    @classmethod
    def check_modalities(cls, v):
        for modality in v:
            OntologyTerm(**modality)
    @field_validator('bodyParts')
    @classmethod
    def check_bodyParts(cls, v):
        for body_part in v:
            OntologyTerm(**body_part)
    @field_validator('gender')
    @classmethod
    def check_gender(cls, v):
        for gender in v:
            OntologyTerm(**gender)