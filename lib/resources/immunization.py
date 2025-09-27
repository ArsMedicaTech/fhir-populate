"""
Immunization resource generation function.
"""
import uuid
import random
from datetime import timedelta
from faker import Faker
from typing import Dict, Any

from lib.data.immunizations import (IMMUNIZATION_STATUSES, VACCINES, VACCINE_MANUFACTURERS,
                                  ADMINISTRATION_SITES, ROUTES_OF_ADMINISTRATION, 
                                  PERFORMER_FUNCTIONS, VACCINE_REACTIONS, IMMUNIZATION_REASONS,
                                  IMMUNIZATION_NOTES, DOSE_QUANTITIES)


# Initialize Faker to generate random data
fake = Faker()


def generate_immunization(patient_id: str, practitioner_id: str, encounter_id: str = None, location_id: str = None) -> Dict[str, Any]:
    """
    Generates a single FHIR Immunization resource.
    
    :param patient_id: The ID of the patient receiving the immunization.
    :param practitioner_id: The ID of the practitioner administering the immunization.
    :param encounter_id: Optional ID of the encounter this immunization is associated with.
    :param location_id: Optional ID of the location where immunization was given.
    :return: A dictionary representing the FHIR Immunization resource.
    """
    immunization_id = str(uuid.uuid4())
    status = random.choice(IMMUNIZATION_STATUSES)
    vaccine = random.choice(VACCINES)
    manufacturer = random.choice(VACCINE_MANUFACTURERS)
    site = random.choice(ADMINISTRATION_SITES)
    route = random.choice(ROUTES_OF_ADMINISTRATION)
    dose_quantity = random.choice(DOSE_QUANTITIES)
    reason = random.choice(IMMUNIZATION_REASONS)
    note = random.choice(IMMUNIZATION_NOTES)
    
    # Generate occurrence date (when vaccine was given)
    occurrence_date = fake.date_between(start_date='-2y', end_date='today')
    
    # Generate lot number
    lot_number = f"{fake.random_letter().upper()}{fake.random_letter().upper()}{fake.random_letter().upper()}{fake.random_number(digits=3)}{fake.random_letter().upper()}"
    
    # Generate expiration date (1-3 years from occurrence)
    expiration_date = occurrence_date + timedelta(days=random.randint(365, 1095))
    
    # Generate identifier
    identifier_value = f"urn:oid:1.3.6.1.4.1.21367.2005.3.7.{fake.random_number(digits=4)}"
    
    # Create the immunization resource
    immunization = {
        "resourceType": "Immunization",
        "id": immunization_id,
        "identifier": [
            {
                "system": "urn:ietf:rfc:3986",
                "value": identifier_value
            }
        ],
        "status": status,
        "vaccineCode": {
            "coding": [
                {
                    "system": vaccine["system"],
                    "code": vaccine["code"],
                    "display": vaccine["display"]
                }
            ],
            "text": vaccine["text"]
        },
        "manufacturer": {
            "reference": manufacturer["reference"],
            "display": manufacturer["display"]
        },
        "lotNumber": lot_number,
        "expirationDate": expiration_date.isoformat(),
        "patient": {
            "reference": f"Patient/{patient_id}",
            "display": f"Patient {patient_id[:8]}"
        },
        "occurrenceDateTime": occurrence_date.isoformat(),
        "primarySource": True,
        "site": {
            "coding": [
                {
                    "system": site["system"],
                    "code": site["code"],
                    "display": site["display"]
                }
            ]
        },
        "route": {
            "coding": [
                {
                    "system": route["system"],
                    "code": route["code"],
                    "display": route["display"]
                }
            ]
        },
        "doseQuantity": {
            "value": dose_quantity["value"],
            "system": "http://unitsofmeasure.org",
            "code": dose_quantity["code"],
            "unit": dose_quantity["unit"]
        },
        "performer": [
            {
                "function": {
                    "coding": [
                        {
                            "system": PERFORMER_FUNCTIONS[0]["system"],
                            "code": PERFORMER_FUNCTIONS[0]["code"],
                            "display": PERFORMER_FUNCTIONS[0]["display"]
                        }
                    ]
                },
                "actor": {
                    "reference": f"Practitioner/{practitioner_id}",
                    "display": f"Dr. {fake.last_name()}"
                }
            },
            {
                "function": {
                    "coding": [
                        {
                            "system": PERFORMER_FUNCTIONS[1]["system"],
                            "code": PERFORMER_FUNCTIONS[1]["code"],
                            "display": PERFORMER_FUNCTIONS[1]["display"]
                        }
                    ]
                },
                "actor": {
                    "reference": f"Practitioner/{practitioner_id}",
                    "display": f"Dr. {fake.last_name()}"
                }
            }
        ],
        "note": [
            {
                "text": note
            }
        ],
        "reason": [
            {
                "reference": {
                    "reference": f"Observation/{str(uuid.uuid4())}"
                }
            }
        ],
        "isSubpotent": False
    }
    
    # Add encounter reference if provided
    if encounter_id:
        immunization["encounter"] = {
            "reference": f"Encounter/{encounter_id}"
        }
    
    # Add location reference if provided
    if location_id:
        immunization["location"] = {
            "reference": f"Location/{location_id}"
        }
    
    # Add reaction information (30% chance)
    if random.random() < 0.3:
        reaction = random.choice(VACCINE_REACTIONS)
        immunization["reaction"] = [
            {
                "date": occurrence_date.isoformat(),
                "manifestation": {
                    "reference": {
                        "reference": f"Observation/{str(uuid.uuid4())}"
                    }
                },
                "reported": random.choice([True, False])
            }
        ]
    
    # Generate text narrative
    immunization["text"] = {
        "status": "generated",
        "div": f"""<div xmlns="http://www.w3.org/1999/xhtml">
            <p><b>Generated Narrative: Immunization</b><a name="{immunization_id}"> </a></p>
            <div style="display: inline-block; background-color: #d9e0e7; padding: 6px; margin: 4px; border: 1px solid #8da1b4; border-radius: 5px; line-height: 60%">
                <p style="margin-bottom: 0px">Resource Immunization &quot;{immunization_id}&quot; </p>
            </div>
            <p><b>identifier</b>: id: {identifier_value}</p>
            <p><b>status</b>: {status}</p>
            <p><b>vaccineCode</b>: {vaccine['text']} <span style="background: LightGoldenRodYellow; margin: 4px; border: 1px solid khaki"> (<a href="http://terminology.hl7.org/5.1.0/CodeSystem-CVX.html">Vaccine Administered Code Set (CVX)</a>#{vaccine['code']})</span></p>
            <h3>Manufacturers</h3>
            <table class="grid">
                <tr><td>-</td><td><b>Reference</b></td></tr>
                <tr><td>*</td><td><a href="organization-{manufacturer['reference'].split('/')[-1]}.html">{manufacturer['reference']}</a> &quot;{manufacturer['display']}&quot;</td></tr>
            </table>
            <p><b>lotNumber</b>: {lot_number}</p>
            <p><b>expirationDate</b>: {expiration_date.strftime('%Y-%m-%d')}</p>
            <p><b>patient</b>: <a href="patient-{patient_id}.html">Patient/{patient_id}</a></p>
            <p><b>occurrence</b>: {occurrence_date.strftime('%Y-%m-%d')}</p>
            <p><b>primarySource</b>: true</p>
            <p><b>site</b>: {site['display']} <span style="background: LightGoldenRodYellow; margin: 4px; border: 1px solid khaki"> (<a href="http://terminology.hl7.org/5.1.0/CodeSystem-v3-ActSite.html">ActSite</a>#{site['code']})</span></p>
            <p><b>route</b>: {route['display']} <span style="background: LightGoldenRodYellow; margin: 4px; border: 1px solid khaki"> (<a href="http://terminology.hl7.org/5.1.0/CodeSystem-v3-RouteOfAdministration.html">RouteOfAdministration</a>#{route['code']})</span></p>
            <p><b>doseQuantity</b>: {dose_quantity['value']} {dose_quantity['unit']}<span style="background: LightGoldenRodYellow"> (Details: UCUM code {dose_quantity['code']} = '{dose_quantity['unit']}')</span></p>
            <blockquote>
                <p><b>performer</b></p>
                <p><b>function</b>: {PERFORMER_FUNCTIONS[0]['display']} <span style="background: LightGoldenRodYellow; margin: 4px; border: 1px solid khaki"> (<a href="http://terminology.hl7.org/5.1.0/CodeSystem-v2-0443.html">providerRole</a>#{PERFORMER_FUNCTIONS[0]['code']})</span></p>
                <p><b>actor</b>: <a href="practitioner-{practitioner_id}.html">Practitioner/{practitioner_id}</a></p>
            </blockquote>
            <blockquote>
                <p><b>performer</b></p>
                <p><b>function</b>: {PERFORMER_FUNCTIONS[1]['display']} <span style="background: LightGoldenRodYellow; margin: 4px; border: 1px solid khaki"> (<a href="http://terminology.hl7.org/5.1.0/CodeSystem-v2-0443.html">providerRole</a>#{PERFORMER_FUNCTIONS[1]['code']})</span></p>
                <p><b>actor</b>: <a href="practitioner-{practitioner_id}.html">Practitioner/{practitioner_id}</a></p>
            </blockquote>
            <p><b>note</b>: {note}</p>
            <h3>Reasons</h3>
            <table class="grid">
                <tr><td>-</td><td><b>Reference</b></td></tr>
                <tr><td>*</td><td><a href="observation-example.html">Observation/example</a></td></tr>
            </table>
            <p><b>isSubpotent</b>: false</p>
            {'<blockquote><p><b>reaction</b></p><p><b>date</b>: ' + occurrence_date.strftime('%Y-%m-%d') + '</p><h3>Manifestations</h3><table class="grid"><tr><td>-</td><td><b>Reference</b></td></tr><tr><td>*</td><td><a href="broken-link.html">Observation/example2</a></td></tr></table><p><b>reported</b>: false</p></blockquote>' if 'reaction' in immunization else ''}
        </div>"""
    }
    
    return immunization
