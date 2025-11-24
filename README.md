**EUCAIM Federated Query JSON Schemas**

This repository contains four JSON Schemas developed within the framework of the EUCAIM project to provide a structured, interoperable, and traceable metadata representation for the entities required in federated queries. The schemas define the minimum and optional attributes for patients, diseases, imaging studies, and tumors.

There are 4 json schema available:

PatientMetadata.json
Defines the minimum set of patient attributes (e.g., patient identifier, sex).

DiseaseMetadata.json
Describes a disease or diagnostic episode associated with a patient, including diagnosis, pathology, treatment information, and relevant clinical attributes.

ImagingMetadata.json
Contains metadata associated with imaging studies, such as modality, anatomical region, manufacturer, and date of acquisition.

TumorMetadata.json
Provides optional tumor-related attributes, including tumor markers, staging categories, and standardized assessment systems such as BI-RADS and PI-RADS.

To improve traceability and data integration within federated environments, the schemas introduce a set of structured identifiers:

patientId
A unique and anonymized identifier for the patient, aligned with DICOM tag (0010,0020).

diseaseId
An identifier corresponding to a specific diagnostic episode or disease instance for a patient.

imageId
An identifier for an imaging study, linked to both the associated patient and disease.

tumorId
An identifier for a tumor or lesion, linked to patient, disease, and imaging data.

This identifier structure enables explicit relationships across metadata entities, supporting consistent referencing and harmonized query execution.

Source Table Mapping

The content of each schema is derived from the federated query metadata tables as follows:

Table 14	PatientMetadata, DiseaseMetadata, ImagingMetadata
Table 15	DiseaseMetadata
Table 16	TumorMetadata

The next development phase will involve generating synthetic test datasets compliant with these schemas. This will enable the Beacon team to begin validation and implementation work within the federated query infrastructure. Further adjustments to the schemas may take place based on partner feedback and downstream integration requirements.
