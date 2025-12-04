import re
from datetime import datetime
from dateutil.parser import parse

from pydantic import (
    BaseModel,
    field_validator,
    PrivateAttr
)
from typing import Optional, List

class OntologyTerm(BaseModel):
    id: str
    label: Optional[str]=None
    @field_validator('id')
    @classmethod
    def id_must_be_CURIE(cls, v: str) -> str:
        if re.match("[A-Za-z0-9]+:[A-Za-z0-9]", v):
            pass
        else:
            raise ValueError('id must be CURIE, e.g. EUCAIM:COM1001288')
        return v.title()

class Tumor(BaseModel, extra="forbid"):

    def __init__(self, **data) -> None:
        for private_key in self.__class__.__private_attributes__.keys():
            try:
                value = data.pop(private_key)
            except KeyError:
                pass
        super().__init__(**data)

    _id: Optional[str] = PrivateAttr()
    tumorId: str
    tumorMarkerTestResult: Optional[OntologyTerm] = None
    cancerStageCMCategory: Optional[OntologyTerm] = None
    cancerStagePMCategory: Optional[OntologyTerm] = None
    histologicGraceGleasonScore: Optional[OntologyTerm] = None
    histologicGradeISUP: Optional[OntologyTerm] = None
    tumorBIRADSAssesment: Optional[OntologyTerm] = None
    tumorPIRADSAssesment: Optional[OntologyTerm] = None

class Disease(BaseModel, extra='forbid'):
    def __init__(self, **data) -> None:
        for private_key in self.__class__.__private_attributes__.keys():
            try:
                value = data.pop(private_key)
            except KeyError:
                pass

        super().__init__(**data)
    _id: Optional[str] = PrivateAttr()
    diseaseId: str
    ageAtDiagnosis: float
    diagnosis: OntologyTerm
    yearOfDiagnosis:  Optional[int]=None
    dateOfFirstTreatment: Optional[datetime]=None
    pathologyConfirmation: Optional[OntologyTerm]=None
    pathology: Optional[list]=None
    imagingProcedureProtocol: Optional[OntologyTerm]=None
    treatment: Optional[List]=None
    tumorMetadata: Optional[List]=None
    @field_validator('pathology')
    @classmethod
    def check_pathology(cls, v):
        for pathology in v:
            OntologyTerm(**pathology)
    @field_validator('treatment')
    @classmethod
    def check_treatment(cls, v):
        for treatment in v:
            OntologyTerm(**treatment)
    @field_validator('tumorMetadata')
    @classmethod
    def check_tumorMetadata(cls, v):
        for tumor_metadata in v:
            Tumor(**tumor_metadata)

class Imaging(BaseModel, extra='forbid'):
    def __init__(self, **data) -> None:
        for private_key in self.__class__.__private_attributes__.keys():
            try:
                value = data.pop(private_key)
            except KeyError:
                pass

        super().__init__(**data)
    _id: Optional[str] = PrivateAttr()
    imageStudyId: str
    disease: Disease
    imageModality: OntologyTerm
    imageBodypart: OntologyTerm
    imageManufacturer: OntologyTerm
    dateOfImageAcquisition: datetime
    @field_validator('dateOfImageAcquisition')
    @classmethod
    def check_dateOfImageAcquisition(cls, v: str) -> str:
        if isinstance(v, str):
            try:
                parse(v)
            except Exception as e:
                raise ValueError('dateOfImageAcquisition, if string, must be a date, getting this error: {}'.format(e))
            return v

class Patient(BaseModel, extra='forbid'):
    def __init__(self, **data) -> None:
        for private_key in self.__class__.__private_attributes__.keys():
            try:
                value = data.pop(private_key)
            except KeyError:
                pass

        super().__init__(**data)
    _id: Optional[str] = PrivateAttr()
    patientId: str
    sex: OntologyTerm
    diseases: Optional[List]=None
    imageStudies: Optional[List]=None
    @field_validator('diseases')
    @classmethod
    def check_diseases(cls, v):
        for disease in v:
            Disease(**disease)
    @field_validator('imageStudies')
    @classmethod
    def check_imageStudies(cls, v):
        for image_study in v:
            Imaging(**image_study)