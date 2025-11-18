"""
ImagingStudy resource generation function.
Generates FHIR ImagingStudy resources with DICOM-compliant UIDs and metadata.
"""
import uuid
import random
from datetime import datetime, timedelta, timezone
from faker import Faker
from typing import Dict, Any, List, Optional

from common import get_fhir_version
from lib.data.imaging_studies import (
    IMAGING_MODALITIES, IMAGING_STUDY_STATUSES, IMAGING_STUDY_REASONS,
    IMAGING_BODY_SITES, IMAGING_STUDY_DESCRIPTIONS, SERIES_DESCRIPTIONS,
    PERFORMER_FUNCTIONS, DICOM_SOP_CLASSES, STUDY_DESCRIPTIONS_BY_MODALITY
)

# Initialize Faker to generate random data
fake = Faker()


def generate_dicom_uid() -> str:
    """
    Generates a DICOM-compliant UID.
    DICOM UIDs follow the format: root.extension where root is typically 1.2.840.10008
    and extension is a series of numbers.
    
    :return: A DICOM UID string
    """
    # Generate a realistic DICOM UID
    # Format: 1.2.840.10008.x.y.z where x, y, z are random numbers
    root = "1.2.840.10008"
    extension_parts = [str(random.randint(1, 999)) for _ in range(5)]
    return f"{root}.{'.'.join(extension_parts)}"


def create_imaging_instance(instance_uid: str, sop_class: str, instance_num: int) -> Dict[str, Any]:
    """
    Creates a valid ImagingStudy instance with all required fields.
    
    :param instance_uid: DICOM SOP Instance UID
    :param sop_class: DICOM SOP Class OID (required)
    :param instance_num: Instance number in the series
    :return: A dictionary representing a valid ImagingStudy instance
    """
    # Ensure sopClass is valid
    default_sop_class = "1.2.840.10008.5.1.4.1.1.2"  # CT Image Storage
    
    if not sop_class or (isinstance(sop_class, str) and sop_class.strip() == ""):
        sop_class = default_sop_class
    
    if not isinstance(sop_class, str):
        sop_class = str(sop_class)
    
    # sopClass must be a Coding object, not a primitive OID
    # Structure: { "system": "urn:ietf:rfc:3986", "code": "urn:oid:...", "display": "..." }
    sop_class_obj = {
        "system": "urn:ietf:rfc:3986",  # Standard system for OID-based identifiers
        "code": f"urn:oid:{sop_class}",  # OID prefixed with urn:oid:
        "display": f"DICOM SOP Class {sop_class}"  # Human-readable description
    }
    
    # Create instance with all required fields
    instance = {
        "uid": instance_uid,
        "sopClass": sop_class_obj,  # Required field - must be a Coding object
        "number": instance_num,
        "title": f"Image {instance_num}"
    }
    
    # Final validation - this should never fail, but ensures safety
    if "sopClass" not in instance:
        raise ValueError(f"Instance {instance_num} missing sopClass field after creation")
    if not instance["sopClass"] or not isinstance(instance["sopClass"], dict):
        raise ValueError(f"Instance {instance_num} has invalid sopClass field - must be a Coding object")
    
    return instance


def generate_imaging_study(
    patient_id: str,
    practitioner_id: str,
    encounter_id: Optional[str] = None,
    service_request_id: Optional[str] = None,
    location_id: Optional[str] = None
) -> Dict[str, Any]:
    """
    Generates a single FHIR ImagingStudy resource.
    
    :param patient_id: The ID of the patient for the imaging study.
    :param practitioner_id: The ID of the practitioner who performed/referred the study.
    :param encounter_id: Optional ID of the encounter this study is associated with.
    :param service_request_id: Optional ID of the service request this study fulfills.
    :param location_id: Optional ID of the location where the study was performed.
    :return: A dictionary representing the FHIR ImagingStudy resource.
    """
    imaging_study_id = str(uuid.uuid4())
    status = random.choice(IMAGING_STUDY_STATUSES)
    
    # Select a modality for the study
    modality = random.choice(IMAGING_MODALITIES)
    modality_code = modality["code"]
    
    # Generate study start time
    study_start = fake.date_time_between(start_date='-1y', end_date='now')
    if study_start.tzinfo is None:
        study_start = study_start.replace(tzinfo=timezone.utc)
    
    # Generate DICOM Study Instance UID
    study_instance_uid = generate_dicom_uid()
    
    # Generate study description based on modality
    if modality_code in STUDY_DESCRIPTIONS_BY_MODALITY:
        study_description = random.choice(STUDY_DESCRIPTIONS_BY_MODALITY[modality_code])
    else:
        study_description = random.choice(IMAGING_STUDY_DESCRIPTIONS)
    
    # Generate 1-3 series for the study
    num_series = random.randint(1, 3)
    series_list = []
    total_instances = 0
    
    for series_num in range(1, num_series + 1):
        # Generate Series Instance UID
        series_uid = generate_dicom_uid()
        
        # Series modality (should match study modality, but can have variations)
        series_modality = modality
        
        # Generate series description
        series_description = f"{study_description} - {random.choice(SERIES_DESCRIPTIONS)}"
        
        # Generate series start time (slightly after study start)
        series_start = study_start + timedelta(minutes=random.randint(5, 30))
        
        # Generate 1-50 instances per series (varies by modality)
        if modality_code in ["CT", "MR"]:
            num_instances = random.randint(10, 50)
        elif modality_code in ["US", "NM", "PT"]:
            num_instances = random.randint(5, 20)
        else:  # X-ray, CR, DX, etc.
            num_instances = random.randint(1, 4)
        
        # Generate instances
        instance_list = []
        # Ensure we have valid SOP classes to choose from
        if not DICOM_SOP_CLASSES or len(DICOM_SOP_CLASSES) == 0:
            raise ValueError("DICOM_SOP_CLASSES list is empty")
        
        for instance_num in range(1, num_instances + 1):
            instance_uid = generate_dicom_uid()
            sop_class = random.choice(DICOM_SOP_CLASSES)
            
            # Use helper function to create validated instance
            instance = create_imaging_instance(instance_uid, sop_class, instance_num)
            instance_list.append(instance)
        
        # Select body site for this series
        body_site = random.choice(IMAGING_BODY_SITES)
        
        # Select performer function
        performer_function = random.choice(PERFORMER_FUNCTIONS)
        
        # Get FHIR version to determine field structure
        fhir_version = get_fhir_version()
        
        # Create series modality structure
        # Some servers expect Coding directly (not CodeableConcept with coding array)
        # Try Coding structure first (system, code, display directly)
        series_modality_obj = {
            "system": series_modality["system"],
            "code": series_modality["code"],
            "display": series_modality["display"]
        }
        
        # Create bodySite structure
        # In R4, bodySite should be CodeableConcept, but some servers may expect Coding
        # Try Coding structure first
        body_site_obj = {
            "system": body_site["system"],
            "code": body_site["code"],
            "display": body_site["display"]
        }
        
        # Create series
        series = {
            "uid": series_uid,
            "number": series_num,
            "modality": series_modality_obj,
            "description": series_description,
            "numberOfInstances": num_instances,
            "bodySite": body_site_obj,
            "started": series_start.isoformat(),
            "performer": [
                {
                    "function": {
                        "coding": [
                            {
                                "system": performer_function["system"],
                                "code": performer_function["code"],
                                "display": performer_function["display"]
                            }
                        ]
                    },
                    "actor": {
                        "reference": f"Practitioner/{practitioner_id}"
                    }
                }
            ],
            "instance": instance_list
        }
        
        series_list.append(series)
        total_instances += num_instances
    
    # Select reason for the study
    reason = random.choice(IMAGING_STUDY_REASONS)
    
    # Get FHIR version to determine field structure
    fhir_version = get_fhir_version()
    
    # Create modality structure
    # Some servers expect Coding directly in the array (not CodeableConcept)
    # Try Coding structure (system, code, display directly)
    modality_obj = [
        {
            "system": modality["system"],
            "code": modality["code"],
            "display": modality["display"]
        }
    ]
    
    # Create the imaging study resource
    imaging_study = {
        "resourceType": "ImagingStudy",
        "id": imaging_study_id,
        "identifier": [
            {
                "use": "official",
                "system": "urn:dicom:uid",
                "value": f"urn:oid:{study_instance_uid}"
            }
        ],
        "status": status,
        "modality": modality_obj,
        "subject": {
            "reference": f"Patient/{patient_id}"
        },
        "started": study_start.isoformat(),
        "description": study_description,
        "numberOfSeries": num_series,
        "numberOfInstances": total_instances,
        "series": series_list
    }
    
    # Add encounter reference if provided
    if encounter_id:
        imaging_study["encounter"] = {
            "reference": f"Encounter/{encounter_id}"
        }
    
    # Add service request reference if provided (basedOn)
    if service_request_id:
        imaging_study["basedOn"] = [
            {
                "reference": f"ServiceRequest/{service_request_id}"
            }
        ]
    
    # Add location reference if provided
    if location_id:
        imaging_study["location"] = {
            "reference": f"Location/{location_id}"
        }
    
    # Add referrer (practitioner who referred the study)
    imaging_study["referrer"] = {
        "reference": f"Practitioner/{practitioner_id}"
    }
    
    # Add reason for the study (R5 only - not in R4)
    if fhir_version != "R4":
        imaging_study["reason"] = [
            {
                "concept": {
                    "coding": [
                        {
                            "system": reason["system"],
                            "code": reason["code"],
                            "display": reason["display"]
                        }
                    ]
                }
            }
        ]
    
    # Note: endpoint is optional and would point to a WADO-RS service endpoint
    # In a real system, this would point to an actual PACS endpoint
    # We omit it here since we don't have Endpoint resources in this sandbox
    
    # Final validation: Ensure all instances have sopClass (required field)
    # This is a safety check to catch any edge cases
    default_sop_class = "1.2.840.10008.5.1.4.1.1.2"  # CT Image Storage as fallback
    for series_idx, series in enumerate(imaging_study.get("series", [])):
        if "instance" in series:
            for instance_idx, instance in enumerate(series["instance"]):
                if "sopClass" not in instance or not instance.get("sopClass"):
                    # Log and fix missing sopClass - must be a Coding object
                    print(f"WARNING: Series {series_idx + 1}, Instance {instance_idx + 1} missing sopClass, adding default")
                    instance["sopClass"] = {
                        "system": "urn:ietf:rfc:3986",
                        "code": f"urn:oid:{default_sop_class}",
                        "display": f"DICOM SOP Class {default_sop_class}"
                    }
                # Ensure it's a Coding object (dict), not a string
                if not isinstance(instance.get("sopClass"), dict):
                    # Convert string to Coding object if needed
                    sop_class_value = str(instance.get("sopClass", default_sop_class))
                    instance["sopClass"] = {
                        "system": "urn:ietf:rfc:3986",
                        "code": f"urn:oid:{sop_class_value}",
                        "display": f"DICOM SOP Class {sop_class_value}"
                    }
                # Ensure the Coding object has required fields
                if "code" not in instance["sopClass"] or not instance["sopClass"].get("code"):
                    instance["sopClass"]["code"] = f"urn:oid:{default_sop_class}"
                if "system" not in instance["sopClass"]:
                    instance["sopClass"]["system"] = "urn:ietf:rfc:3986"
    
    # Add text narrative
    # modality is now Coding directly (not CodeableConcept), so access display directly
    series_string = ''.join([
        f'<tr><td>{s["number"]}</td><td>{s["modality"].get("display", "Unknown")}</td><td>{s["description"]}</td><td>{s["numberOfInstances"]}</td></tr>' 
        for s in series_list
    ])
    modality_display = modality["display"]
    imaging_study["text"] = {
        "status": "generated",
        "div": f"""<div xmlns="http://www.w3.org/1999/xhtml">
            <p><b>Generated Narrative: ImagingStudy</b><a name="{imaging_study_id}"> </a></p>
            <div style="display: inline-block; background-color: #d9e0e7; padding: 6px; margin: 4px; border: 1px solid #8da1b4; border-radius: 5px; line-height: 60%">
                <p style="margin-bottom: 0px">Resource ImagingStudy &quot;{imaging_study_id}&quot; </p>
            </div>
            <p><b>status</b>: {status}</p>
            <p><b>modality</b>: {modality_display}</p>
            <p><b>subject</b>: <a href="patient-{patient_id}.html">Patient/{patient_id}</a></p>
            <p><b>started</b>: {study_start.strftime('%Y-%m-%dT%H:%M:%S%z')}</p>
            <p><b>description</b>: {study_description}</p>
            <p><b>numberOfSeries</b>: {num_series}</p>
            <p><b>numberOfInstances</b>: {total_instances}</p>
            <p><b>referrer</b>: <a href="practitioner-{practitioner_id}.html">Practitioner/{practitioner_id}</a></p>
            <h3>Series</h3>
            <table class="grid">
                <tr><td><b>Series</b></td><td><b>Modality</b></td><td><b>Description</b></td><td><b>Instances</b></td></tr>
                {series_string}
            </table>
        </div>"""
    }
    
    return imaging_study

