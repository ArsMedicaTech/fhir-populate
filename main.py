"""
Some helper scripts for generating FHIR data for testing environments.
"""
import random
from faker import Faker

import json
from typing import Optional

from lib.crud import Request
from lib.resources import (generate_clinic_and_location, generate_patient, generate_practitioner, generate_condition,
                           generate_appointment, generate_medication_request, generate_procedure)


class FHIRServerConfig:
    """
    Configuration for connecting to a FHIR server.
    """
    def __init__(self, host: str = 'localhost', port: int = 8080, path: str = "/fhir") -> None:
        self.host = host
        self.port = port
        self.path = path


# Initialize Faker to generate random data
fake = Faker()


def main(output_filename: Optional[str] = None, fhir_server: Optional[FHIRServerConfig] = None) -> None:
    """
    Main function to generate a set of interconnected FHIR resources.

    Generates Patients, Practitioners, Clinics, Locations, Conditions, and Appointments,
    and saves them to a JSON file OR sends them to a FHIR server.

    :param output_filename: Optional; if provided, the generated data will be saved to this file.
    :param fhir_server: Optional; if provided, the generated data will be sent to this FHIR server.
    :return: None
    """
    print("Generating FHIR compatible dummy data...")

    # Generate clinics and their locations
    clinics = []
    locations = []
    for _ in range(3):
        clinic, location = generate_clinic_and_location()
        clinics.append(clinic)
        locations.append(location)

    # Generate a pool of practitioners
    practitioners = [generate_practitioner() for _ in range(10)]

    # Generate patients and their related data
    patients = []
    conditions = []
    appointments = []
    medication_requests = []
    procedures = []

    for _ in range(25):
        patient = generate_patient()
        patients.append(patient)

        # Generate 1 to 3 conditions for each patient
        for _ in range(random.randint(1, 3)):
            condition = generate_condition(patient['id'])
            conditions.append(condition)

        # Generate 1 to 5 appointments for each patient
        for _ in range(random.randint(1, 5)):
            # Assign a random practitioner and location to the appointment
            practitioner = random.choice(practitioners)
            location = random.choice(locations)
            appointment = generate_appointment(patient['id'], practitioner['id'], location['id'])
            appointments.append(appointment)

        # Generate 1 to 4 medication requests for each patient
        for _ in range(random.randint(1, 4)):
            # Assign a random practitioner to the medication request
            practitioner = random.choice(practitioners)
            medication_request = generate_medication_request(patient['id'], practitioner['id'])
            medication_requests.append(medication_request)

        # Generate 1 to 3 procedures for each patient
        for _ in range(random.randint(1, 3)):
            # Assign a random practitioner to the procedure
            practitioner = random.choice(practitioners)
            procedure = generate_procedure(patient['id'], practitioner['id'])
            procedures.append(procedure)

    # Combine all generated resources into a single dictionary
    fhir_bundle = {
        "patients": patients,
        "practitioners": practitioners,
        "clinics": clinics,
        "locations": locations,
        "conditions": conditions,
        "appointments": appointments,
        "medication_requests": medication_requests,
        "procedures": procedures
    }

    # Write the output to a JSON file
    if output_filename:
        with open(output_filename, 'w') as f: json.dump(fhir_bundle, f, indent=2)
        print(f"\nSuccessfully generated dummy data and saved it to '{output_filename}'")

    print(f" - Patients: {len(patients)}")
    print(f" - Practitioners: {len(practitioners)}")
    print(f" - Clinics: {len(clinics)}")
    print(f" - Locations: {len(locations)}")
    print(f" - Conditions: {len(conditions)}")
    print(f" - Appointments: {len(appointments)}")
    print(f" - Medication Requests: {len(medication_requests)}")
    print(f" - Procedures: {len(procedures)}")

    if fhir_server:
        fhir_request = Request(host=fhir_server.host, port=fhir_server.port, path=fhir_server.path)
        
        # Create organizations first and store their server-assigned IDs
        organization_id_map = {}
        for i, clinic in enumerate(clinics):
            response = fhir_request.create("Organization", clinic)
            if response.get('issue') and response['issue'][0]['severity'] == 'error':
                err = response['issue'][0]['diagnostics']
                print(err)
                raise Exception(err)
            server_id = response.get('id')
            organization_id_map[clinic['id']] = server_id
            print(f"Created Organization with ID: {server_id}")
        
        # Update location references to use server-assigned organization IDs
        for location in locations:
            original_org_id = location['managingOrganization']['reference'].split('/')[1]
            server_org_id = organization_id_map[original_org_id]
            location['managingOrganization']['reference'] = f"Organization/{server_org_id}"
        
        # Create locations with updated references and store their server-assigned IDs
        location_id_map = {}
        for location in locations:
            response = fhir_request.create("Location", location)
            if response.get('issue') and response['issue'][0]['severity'] == 'error':
                err = response['issue'][0]['diagnostics']
                print(err)
                raise Exception(err)
            server_id = response.get('id')
            location_id_map[location['id']] = server_id
            print(f"Created Location with ID: {server_id}")
        
        # Create patients first and store their server-assigned IDs
        patient_id_map = {}
        for patient in patients:
            response = fhir_request.create("Patient", patient)
            if response.get('issue') and response['issue'][0]['severity'] == 'error':
                err = response['issue'][0]['diagnostics']
                print(err)
                raise Exception(err)
            server_id = response.get('id')
            patient_id_map[patient['id']] = server_id
            print(f"Created Patient with ID: {server_id}")
        
        # Update condition references to use server-assigned patient IDs
        for condition in conditions:
            original_patient_id = condition['subject']['reference'].split('/')[1]
            server_patient_id = patient_id_map[original_patient_id]
            condition['subject']['reference'] = f"Patient/{server_patient_id}"
        
        # Create conditions with updated references
        for condition in conditions:
            response = fhir_request.create("Condition", condition)
            if response.get('issue') and response['issue'][0]['severity'] == 'error':
                err = response['issue'][0]['diagnostics']
                print(err)
                raise Exception(err)
            print(f"Created Condition with ID: {response.get('id')}")
        
        # Create practitioners and store their server-assigned IDs
        practitioner_id_map = {}
        for practitioner in practitioners:
            response = fhir_request.create("Practitioner", practitioner)
            if response.get('issue') and response['issue'][0]['severity'] == 'error':
                err = response['issue'][0]['diagnostics']
                print(err)
                raise Exception(err)
            server_id = response.get('id')
            practitioner_id_map[practitioner['id']] = server_id
            print(f"Created Practitioner with ID: {server_id}")
        
        # Update appointment references to use server-assigned IDs
        for appointment in appointments:
            # Update patient reference
            original_patient_id = appointment['participant'][0]['actor']['reference'].split('/')[1]
            server_patient_id = patient_id_map[original_patient_id]
            appointment['participant'][0]['actor']['reference'] = f"Patient/{server_patient_id}"
            
            # Update practitioner reference
            original_practitioner_id = appointment['participant'][1]['actor']['reference'].split('/')[1]
            server_practitioner_id = practitioner_id_map[original_practitioner_id]
            appointment['participant'][1]['actor']['reference'] = f"Practitioner/{server_practitioner_id}"
            
            # Update location reference
            original_location_id = appointment['participant'][2]['actor']['reference'].split('/')[1]
            server_location_id = location_id_map[original_location_id]
            appointment['participant'][2]['actor']['reference'] = f"Location/{server_location_id}"
        
        # Create appointments with updated references
        for appointment in appointments:
            response = fhir_request.create("Appointment", appointment)
            if response.get('issue') and response['issue'][0]['severity'] == 'error':
                err = response['issue'][0]['diagnostics']
                print(err)
                raise Exception(err)
            print(f"Created Appointment with ID: {response.get('id')}")
        
        # Update medication request references to use server-assigned IDs
        for medication_request in medication_requests:
            # Update patient reference
            original_patient_id = medication_request['subject']['reference'].split('/')[1]
            server_patient_id = patient_id_map[original_patient_id]
            medication_request['subject']['reference'] = f"Patient/{server_patient_id}"
            
            # Update practitioner reference
            original_practitioner_id = medication_request['requester']['reference'].split('/')[1]
            server_practitioner_id = practitioner_id_map[original_practitioner_id]
            medication_request['requester']['reference'] = f"Practitioner/{server_practitioner_id}"
        
        # Create medication requests with updated references
        for medication_request in medication_requests:
            response = fhir_request.create("MedicationRequest", medication_request)
            if response.get('issue') and response['issue'][0]['severity'] == 'error':
                err = response['issue'][0]['diagnostics']
                print(err)
                raise Exception(err)
            print(f"Created MedicationRequest with ID: {response.get('id')}")

        # Update procedure references to use server-assigned IDs
        for procedure in procedures:
            # Update patient reference
            original_patient_id = procedure['subject']['reference'].split('/')[1]
            server_patient_id = patient_id_map[original_patient_id]
            procedure['subject']['reference'] = f"Patient/{server_patient_id}"

            # Update practitioner reference
            original_practitioner_id = procedure['performer'][0]['actor']['reference'].split('/')[1]
            server_practitioner_id = practitioner_id_map[original_practitioner_id]
            procedure['performer'][0]['actor']['reference'] = f"Practitioner/{server_practitioner_id}"

        # Create procedures with updated references
        for procedure in procedures:
            response = fhir_request.create("Procedure", procedure)
            if response.get('issue') and response['issue'][0]['severity'] == 'error':
                err = response['issue'][0]['diagnostics']
                print(err)
                raise Exception(err)
            print(f"Created Procedure with ID: {response.get('id')}")


if __name__ == "__main__":
    main(fhir_server=FHIRServerConfig(host="localhost", port=8080, path="/fhir"))
