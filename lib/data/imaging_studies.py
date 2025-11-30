"""
Common imaging study data for FHIR ImagingStudy resources.
Includes DICOM modalities, body sites, reasons, and other imaging-related data.
"""

# DICOM Modalities (from DICOM CID 33)
IMAGING_MODALITIES = [
    {
        "code": "CR",
        "display": "Computed Radiography",
        "system": "http://dicom.nema.org/resources/ontology/DCM"
    },
    {
        "code": "CT",
        "display": "Computed Tomography",
        "system": "http://dicom.nema.org/resources/ontology/DCM"
    },
    {
        "code": "MR",
        "display": "Magnetic Resonance",
        "system": "http://dicom.nema.org/resources/ontology/DCM"
    },
    {
        "code": "US",
        "display": "Ultrasound",
        "system": "http://dicom.nema.org/resources/ontology/DCM"
    },
    {
        "code": "DX",
        "display": "Digital Radiography",
        "system": "http://dicom.nema.org/resources/ontology/DCM"
    },
    {
        "code": "MG",
        "display": "Mammography",
        "system": "http://dicom.nema.org/resources/ontology/DCM"
    },
    {
        "code": "NM",
        "display": "Nuclear Medicine",
        "system": "http://dicom.nema.org/resources/ontology/DCM"
    },
    {
        "code": "PT",
        "display": "Positron emission tomography (PET)",
        "system": "http://dicom.nema.org/resources/ontology/DCM"
    },
    {
        "code": "XA",
        "display": "X-Ray Angiography",
        "system": "http://dicom.nema.org/resources/ontology/DCM"
    },
    {
        "code": "RF",
        "display": "Radiofluoroscopy",
        "system": "http://dicom.nema.org/resources/ontology/DCM"
    },
    {
        "code": "ES",
        "display": "Endoscopy",
        "system": "http://dicom.nema.org/resources/ontology/DCM"
    },
    {
        "code": "OT",
        "display": "Other",
        "system": "http://dicom.nema.org/resources/ontology/DCM"
    }
]

# Imaging Study Statuses (FHIR R4 valid values)
# Note: "inactive" is only available in FHIR R6, not R4
IMAGING_STUDY_STATUSES = [
    "registered",
    "available",
    "cancelled",
    "entered-in-error",
    "unknown"
]

# Common reasons for imaging studies (SNOMED CT)
IMAGING_STUDY_REASONS = [
    {
        "code": "161891005",
        "display": "Chest pain",
        "system": "http://snomed.info/sct"
    },
    {
        "code": "21522001",
        "display": "Abdominal pain",
        "system": "http://snomed.info/sct"
    },
    {
        "code": "25064002",
        "display": "Headache",
        "system": "http://snomed.info/sct"
    },
    {
        "code": "267036007",
        "display": "Dyspnea",
        "system": "http://snomed.info/sct"
    },
    {
        "code": "29857009",
        "display": "Cough",
        "system": "http://snomed.info/sct"
    },
    {
        "code": "29857009",
        "display": "Trauma",
        "system": "http://snomed.info/sct"
    },
    {
        "code": "399211009",
        "display": "History of malignancy",
        "system": "http://snomed.info/sct"
    },
    {
        "code": "161891005",
        "display": "Screening",
        "system": "http://snomed.info/sct"
    },
    {
        "code": "183932001",
        "display": "Follow-up examination",
        "system": "http://snomed.info/sct"
    },
    {
        "code": "183945002",
        "display": "Pre-operative assessment",
        "system": "http://snomed.info/sct"
    },
    {
        "code": "183946001",
        "display": "Post-operative monitoring",
        "system": "http://snomed.info/sct"
    }
]

# Body sites for imaging studies (SNOMED CT)
IMAGING_BODY_SITES = [
    {
        "code": "39607008",
        "display": "Lung structure",
        "system": "http://snomed.info/sct"
    },
    {
        "code": "113197003",
        "display": "Abdomen",
        "system": "http://snomed.info/sct"
    },
    {
        "code": "71341001",
        "display": "Brain structure",
        "system": "http://snomed.info/sct"
    },
    {
        "code": "421060004",
        "display": "Spine structure",
        "system": "http://snomed.info/sct"
    },
    {
        "code": "302551006",
        "display": "Pelvis structure",
        "system": "http://snomed.info/sct"
    },
    {
        "code": "80248007",
        "display": "Heart structure",
        "system": "http://snomed.info/sct"
    },
    {
        "code": "76752008",
        "display": "Breast structure",
        "system": "http://snomed.info/sct"
    },
    {
        "code": "244466001",
        "display": "Extremity structure",
        "system": "http://snomed.info/sct"
    },
    {
        "code": "181220008",
        "display": "Entire chest",
        "system": "http://snomed.info/sct"
    },
    {
        "code": "181220008",
        "display": "Entire head",
        "system": "http://snomed.info/sct"
    },
    {
        "code": "181220008",
        "display": "Entire neck",
        "system": "http://snomed.info/sct"
    },
    {
        "code": "181220008",
        "display": "Entire knee",
        "system": "http://snomed.info/sct"
    },
    {
        "code": "181220008",
        "display": "Entire shoulder",
        "system": "http://snomed.info/sct"
    }
]

# Common imaging study descriptions
IMAGING_STUDY_DESCRIPTIONS = [
    "Chest X-ray PA and lateral",
    "CT chest with contrast",
    "CT abdomen and pelvis with contrast",
    "MRI brain without contrast",
    "MRI brain with and without contrast",
    "MRI spine cervical",
    "MRI spine lumbar",
    "Ultrasound abdomen complete",
    "Ultrasound pelvis transabdominal",
    "Echocardiogram transthoracic",
    "Mammography screening bilateral",
    "Mammography diagnostic",
    "Bone density scan",
    "Nuclear medicine bone scan",
    "PET scan whole body",
    "CT angiography chest",
    "CT angiography head and neck",
    "X-ray knee AP and lateral",
    "X-ray shoulder AP and Y-view",
    "X-ray wrist PA and lateral"
]

# Common series descriptions
SERIES_DESCRIPTIONS = [
    "Axial",
    "Coronal",
    "Sagittal",
    "3D Reconstruction",
    "MIP",
    "MPR",
    "T1 weighted",
    "T2 weighted",
    "FLAIR",
    "DWI",
    "ADC",
    "STIR",
    "Contrast enhanced",
    "Non-contrast",
    "Arterial phase",
    "Venous phase",
    "Delayed phase",
    "Portal venous phase",
    "Pre-contrast",
    "Post-contrast"
]

# Performer functions for imaging studies
# Using valid codes from ImagingStudySeriesPerformerFunction value set
# Valid codes: primary-performer, secondary-performer, consulter, assistant-performer, technician, observer
# Try standard HL7 FHIR CodeSystem URL format
PERFORMER_FUNCTIONS = [
    {
        "code": "primary-performer",
        "display": "Primary Performer",
        "system": "http://hl7.org/fhir/CodeSystem/imagingstudy-series-performer-function"
    },
    {
        "code": "secondary-performer",
        "display": "Secondary Performer",
        "system": "http://hl7.org/fhir/CodeSystem/imagingstudy-series-performer-function"
    },
    {
        "code": "consulter",
        "display": "Consulter",
        "system": "http://hl7.org/fhir/CodeSystem/imagingstudy-series-performer-function"
    },
    {
        "code": "assistant-performer",
        "display": "Assistant Performer",
        "system": "http://hl7.org/fhir/CodeSystem/imagingstudy-series-performer-function"
    },
    {
        "code": "technician",
        "display": "Technician",
        "system": "http://hl7.org/fhir/CodeSystem/imagingstudy-series-performer-function"
    },
    {
        "code": "observer",
        "display": "Observer",
        "system": "http://hl7.org/fhir/CodeSystem/imagingstudy-series-performer-function"
    }
]

# DICOM SOP Classes (common ones)
DICOM_SOP_CLASSES = [
    "1.2.840.10008.5.1.4.1.1.1",  # Computed Radiography Image Storage
    "1.2.840.10008.5.1.4.1.1.2",  # CT Image Storage
    "1.2.840.10008.5.1.4.1.1.4",  # MR Image Storage
    "1.2.840.10008.5.1.4.1.1.6.1",  # Ultrasound Image Storage
    "1.2.840.10008.5.1.4.1.1.1.1",  # Digital X-Ray Image Storage
    "1.2.840.10008.5.1.4.1.1.1.2",  # Digital Mammography X-Ray Image Storage
    "1.2.840.10008.5.1.4.1.1.128",  # Positron Emission Tomography Image Storage
    "1.2.840.10008.5.1.4.1.1.12.1",  # X-Ray Angiographic Image Storage
    "1.2.840.10008.5.1.4.1.1.12.2",  # X-Ray Radiofluoroscopic Image Storage
    "1.2.840.10008.5.1.4.1.1.20",  # Nuclear Medicine Image Storage
]

# Common study descriptions by modality
STUDY_DESCRIPTIONS_BY_MODALITY = {
    "CR": ["Chest X-ray PA and lateral", "X-ray knee AP and lateral", "X-ray wrist PA and lateral"],
    "CT": ["CT chest with contrast", "CT abdomen and pelvis with contrast", "CT head without contrast"],
    "MR": ["MRI brain without contrast", "MRI brain with and without contrast", "MRI spine cervical"],
    "US": ["Ultrasound abdomen complete", "Ultrasound pelvis transabdominal", "Echocardiogram transthoracic"],
    "DX": ["Chest X-ray PA and lateral", "X-ray knee AP and lateral"],
    "MG": ["Mammography screening bilateral", "Mammography diagnostic"],
    "NM": ["Nuclear medicine bone scan", "Nuclear medicine thyroid scan"],
    "PT": ["PET scan whole body", "PET-CT scan"]
}

