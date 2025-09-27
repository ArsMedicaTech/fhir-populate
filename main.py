"""
Some helper scripts for generating FHIR data for testing environments.
"""
import random
from faker import Faker

import json
from typing import Optional

from lib.crud import Request

from lib.resources.appointment import generate_appointment
from lib.resources.clinic import generate_clinic_and_location
from lib.resources.condition import generate_condition
from lib.resources.encounter import generate_encounter
from lib.resources.medication import generate_medication_request
from lib.resources.observation import generate_observation
from lib.resources.patient import generate_patient
from lib.resources.practitioner import generate_practitioner
from lib.resources.procedure import generate_procedure
from lib.resources.diagnostic_report import generate_diagnostic_report
from lib.resources.service_request import generate_service_request


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
    observations = []
    encounters = []
    diagnostic_reports = []
    service_requests = []

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

        # Generate 2 to 6 observations for each patient
        for _ in range(random.randint(2, 6)):
            # Assign a random practitioner to the observation
            practitioner = random.choice(practitioners)
            observation = generate_observation(patient['id'], practitioner['id'])
            observations.append(observation)

        # Generate 1 to 4 encounters for each patient
        patient_encounters = []
        for _ in range(random.randint(1, 4)):
            # Assign a random practitioner, location, and organization to the encounter
            practitioner = random.choice(practitioners)
            location = random.choice(locations)
            organization = random.choice(clinics)
            encounter = generate_encounter(patient['id'], practitioner['id'], location['id'], organization['id'])
            encounters.append(encounter)
            patient_encounters.append(encounter)

        # Generate 1 to 2 diagnostic reports for each patient
        for _ in range(random.randint(1, 2)):
            # Assign a random practitioner and encounter to the diagnostic report
            practitioner = random.choice(practitioners)
            encounter = random.choice(patient_encounters)
            
            # Get some observations for this patient to include in the report
            patient_observations = [obs for obs in observations if obs['subject']['reference'] == f"Patient/{patient['id']}"]
            selected_observations = random.sample(patient_observations, min(3, len(patient_observations)))
            observation_ids = [obs['id'] for obs in selected_observations]
            
            diagnostic_report = generate_diagnostic_report(patient['id'], practitioner['id'], encounter['id'], observation_ids)
            diagnostic_reports.append(diagnostic_report)

        # Generate 1 to 3 service requests for each patient
        for _ in range(random.randint(1, 3)):
            # Assign a random practitioner to the service request
            practitioner = random.choice(practitioners)
            # Optionally link to an encounter (50% chance)
            encounter = random.choice(patient_encounters) if random.choice([True, False]) else None
            
            service_request = generate_service_request(
                patient['id'], 
                practitioner['id'], 
                encounter['id'] if encounter else None
            )
            service_requests.append(service_request)

    # Combine all generated resources into a single dictionary
    fhir_bundle = {
        "patients": patients,
        "practitioners": practitioners,
        "clinics": clinics,
        "locations": locations,
        "conditions": conditions,
        "appointments": appointments,
        "medication_requests": medication_requests,
        "procedures": procedures,
        "observations": observations,
        "encounters": encounters,
        "diagnostic_reports": diagnostic_reports,
        "service_requests": service_requests
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
    print(f" - Observations: {len(observations)}")
    print(f" - Encounters: {len(encounters)}")
    print(f" - Diagnostic Reports: {len(diagnostic_reports)}")
    print(f" - Service Requests: {len(service_requests)}")

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

        # Update observation references to use server-assigned IDs
        for observation in observations:
            # Update patient reference
            original_patient_id = observation['subject']['reference'].split('/')[1]
            server_patient_id = patient_id_map[original_patient_id]
            observation['subject']['reference'] = f"Patient/{server_patient_id}"

            # Update practitioner reference if performer exists
            if 'performer' in observation:
                original_practitioner_id = observation['performer'][0]['reference'].split('/')[1]
                server_practitioner_id = practitioner_id_map[original_practitioner_id]
                observation['performer'][0]['reference'] = f"Practitioner/{server_practitioner_id}"

        # Create observations with updated references
        for observation in observations:
            response = fhir_request.create("Observation", observation)
            if response.get('issue') and response['issue'][0]['severity'] == 'error':
                err = response['issue'][0]['diagnostics']
                print(err)
                raise Exception(err)
            print(f"Created Observation with ID: {response.get('id')}")

        # Update encounter references to use server-assigned IDs
        for encounter in encounters:
            # Update patient reference
            original_patient_id = encounter['subject']['reference'].split('/')[1]
            server_patient_id = patient_id_map[original_patient_id]
            encounter['subject']['reference'] = f"Patient/{server_patient_id}"

            # Update practitioner reference
            original_practitioner_id = encounter['participant'][0]['actor']['reference'].split('/')[1]
            server_practitioner_id = practitioner_id_map[original_practitioner_id]
            encounter['participant'][0]['actor']['reference'] = f"Practitioner/{server_practitioner_id}"

            # Update location reference
            original_location_id = encounter['location'][0]['location']['reference'].split('/')[1]
            server_location_id = location_id_map[original_location_id]
            encounter['location'][0]['location']['reference'] = f"Location/{server_location_id}"

            # Update organization reference
            original_organization_id = encounter['serviceProvider']['reference'].split('/')[1]
            server_organization_id = organization_id_map[original_organization_id]
            encounter['serviceProvider']['reference'] = f"Organization/{server_organization_id}"

        # Create encounters with updated references
        for encounter in encounters:
            response = fhir_request.create("Encounter", encounter)
            if response.get('issue') and response['issue'][0]['severity'] == 'error':
                err = response['issue'][0]['diagnostics']
                print(err)
                raise Exception(err)
            print(f"Created Encounter with ID: {response.get('id')}")


if __name__ == "__main__":
    main(output_filename="fhir_dummy_data.json", fhir_server=FHIRServerConfig(host="localhost", port=8080, path="/fhir"))

