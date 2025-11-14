"""
Some helper scripts for generating FHIR data for testing environments.
"""
import time
import random
from datetime import datetime

import json
from typing import Optional

from common import FHIR_HOST, FHIR_PATH, FHIR_PORT, FINAL_VERIFICATION_CHECK_WAIT_TIME, FHIRServerConfig, check_fhir_response, create_with_validation
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
from lib.resources.clinical_impression import generate_clinical_impression
from lib.resources.family_member_history import generate_family_member_history
from lib.resources.immunization import generate_immunization
from lib.resources.medication_administration import generate_medication_administration
from lib.resources.allergy_intolerance import generate_allergy_intolerance
from lib.resources.care_plan import generate_care_plan
from lib.resources.coverage import generate_coverage
from lib.resources.document_reference import generate_document_reference, generate_binary_resource
from lib.data.document_references import DOCUMENT_TYPES



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
    clinical_impressions = []
    family_member_histories = []
    immunizations = []
    medication_administrations = []
    allergy_intolerances = []
    care_plans = []
    coverages = []
    document_references = []
    binaries = []

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
            
            # Generate clinical notes (DocumentReference) for most encounters (80% chance)
            if random.random() < 0.8:
                # Extract encounter date from period
                encounter_date_str = encounter.get('period', {}).get('start')
                if encounter_date_str:
                    try:
                        encounter_date = datetime.fromisoformat(encounter_date_str.replace('Z', '+00:00'))
                    except:
                        encounter_date = datetime.now()
                else:
                    encounter_date = datetime.now()
                
                # Select a document type for this note
                document_type = random.choice(DOCUMENT_TYPES)
                
                # Generate Binary resource for the note content
                binary = generate_binary_resource(
                    patient['id'],
                    practitioner['id'],
                    document_type,
                    encounter_date
                )
                binaries.append(binary)
                
                # Generate DocumentReference linked to the encounter
                document_reference = generate_document_reference(
                    patient['id'],
                    practitioner['id'],
                    encounter['id'],
                    binary['id'],
                    encounter_date
                )
                document_references.append(document_reference)

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

        # Generate 1 to 2 clinical impressions for each patient
        for _ in range(random.randint(1, 2)):
            # Assign a random practitioner to the clinical impression
            practitioner = random.choice(practitioners)
            # Optionally link to an encounter (70% chance)
            encounter = random.choice(patient_encounters) if random.random() < 0.7 else None
            
            clinical_impression = generate_clinical_impression(
                patient['id'], 
                practitioner['id'], 
                encounter['id'] if encounter else None
            )
            clinical_impressions.append(clinical_impression)

        # Generate 2 to 4 family member histories for each patient
        for _ in range(random.randint(2, 4)):
            # Assign a random practitioner to the family member history (optional)
            practitioner = random.choice(practitioners) if random.random() < 0.7 else None
            
            family_member_history = generate_family_member_history(
                patient['id'], 
                practitioner['id'] if practitioner else None
            )
            family_member_histories.append(family_member_history)

        # Generate 1 to 3 immunizations for each patient
        for _ in range(random.randint(1, 3)):
            # Assign a random practitioner to the immunization
            practitioner = random.choice(practitioners)
            # Optionally link to an encounter (60% chance)
            encounter = random.choice(patient_encounters) if random.random() < 0.6 else None
            # Optionally link to a location (80% chance)
            location = random.choice(locations) if random.random() < 0.8 else None
            
            immunization = generate_immunization(
                patient['id'], 
                practitioner['id'], 
                encounter['id'] if encounter else None,
                location['id'] if location else None
            )
            immunizations.append(immunization)

        # Generate 2 to 5 medication administrations for each patient
        for _ in range(random.randint(2, 5)):
            # Assign a random practitioner to the medication administration
            practitioner = random.choice(practitioners)
            # Optionally link to an encounter (70% chance)
            encounter = random.choice(patient_encounters) if random.random() < 0.7 else None
            # Optionally link to a medication request (50% chance)
            medication_request = random.choice(medication_requests) if random.random() < 0.5 else None
            
            medication_administration = generate_medication_administration(
                patient['id'], 
                practitioner['id'],
                medication_request['id'] if medication_request else None,
                encounter['id'] if encounter else None
            )
            medication_administrations.append(medication_administration)

        # Generate 1 to 4 allergy intolerances for each patient
        for _ in range(random.randint(1, 4)):
            # Assign a random practitioner to the allergy (optional, 60% chance)
            practitioner = random.choice(practitioners) if random.random() < 0.6 else None
            
            allergy_intolerance = generate_allergy_intolerance(
                patient['id'],
                practitioner['id'] if practitioner else None
            )
            allergy_intolerances.append(allergy_intolerance)

        # Generate 1 to 3 care plans for each patient
        for _ in range(random.randint(1, 3)):
            # Assign a random practitioner to the care plan
            practitioner = random.choice(practitioners)
            # Optionally link to an encounter (50% chance)
            encounter = random.choice(patient_encounters) if random.random() < 0.5 else None
            # Optionally link to a condition (70% chance)
            condition = random.choice(conditions) if random.random() < 0.7 else None
            
            care_plan = generate_care_plan(
                patient['id'],
                practitioner['id'],
                encounter['id'] if encounter else None,
                condition['id'] if condition else None
            )
            care_plans.append(care_plan)

        # Generate 1 to 2 coverages for each patient
        for _ in range(random.randint(1, 2)):
            # Assign a random organization as the insurer
            organization = random.choice(clinics)
            # Optionally assign a different policy holder (20% chance)
            policy_holder = random.choice(patients) if random.random() < 0.2 else None
            
            coverage = generate_coverage(
                patient['id'],
                organization['id'],
                policy_holder['id'] if policy_holder else None
            )
            coverages.append(coverage)

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
        "service_requests": service_requests,
        "clinical_impressions": clinical_impressions,
        "family_member_histories": family_member_histories,
        "immunizations": immunizations,
        "medication_administrations": medication_administrations,
        "allergy_intolerances": allergy_intolerances,
        "care_plans": care_plans,
        "coverages": coverages,
        "document_references": document_references,
        "binaries": binaries
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
    print(f" - Clinical Impressions: {len(clinical_impressions)}")
    print(f" - Family Member Histories: {len(family_member_histories)}")
    print(f" - Immunizations: {len(immunizations)}")
    print(f" - Medication Administrations: {len(medication_administrations)}")
    print(f" - Allergy Intolerances: {len(allergy_intolerances)}")
    print(f" - Care Plans: {len(care_plans)}")
    print(f" - Coverages: {len(coverages)}")
    print(f" - Document References: {len(document_references)}")
    print(f" - Binaries: {len(binaries)}")

    if fhir_server:
        fhir_request = Request(host=fhir_server.host, port=fhir_server.port, path=fhir_server.path)
        
        # Test FHIR server connectivity
        print("Testing FHIR server connectivity...")
        try:
            # Simple connectivity test - just check if server responds
            # We skip the appointment test since it requires a real patient
            test_response = fhir_request.search("Patient", params="_count=1")
            if test_response.get('resourceType') == 'Bundle':
                print("✓ FHIR server connectivity test passed")
            else:
                print("WARNING: Unexpected response from FHIR server")
        except Exception as e:
            print(f"WARNING: FHIR server connectivity test failed: {e}")
            print("Continuing with data generation...")
        
        # Create organizations first and store their server-assigned IDs
        organization_id_map = {}
        for i, clinic in enumerate(clinics):
            response = fhir_request.create("Organization", clinic)
            server_id = response.get('id')
            if not check_fhir_response(response, "Organization", server_id):
                raise Exception(f"Failed to create Organization: {response.get('issue', [{}])[0].get('diagnostics', 'Unknown error')}")
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
            server_id = response.get('id')
            if not check_fhir_response(response, "Location", server_id):
                raise Exception(f"Failed to create Location: {response.get('issue', [{}])[0].get('diagnostics', 'Unknown error')}")
            location_id_map[location['id']] = server_id
            print(f"Created Location with ID: {server_id}")
        
        # Create patients first and store their server-assigned IDs
        patient_id_map = {}
        for patient in patients:
            response = fhir_request.create("Patient", patient)
            server_id = response.get('id')
            if not check_fhir_response(response, "Patient", server_id):
                raise Exception(f"Failed to create Patient: {response.get('issue', [{}])[0].get('diagnostics', 'Unknown error')}")
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
            server_id = response.get('id')
            if not check_fhir_response(response, "Condition", server_id):
                raise Exception(f"Failed to create Condition: {response.get('issue', [{}])[0].get('diagnostics', 'Unknown error')}")
            print(f"Created Condition with ID: {server_id}")
        
        # Create practitioners and store their server-assigned IDs
        practitioner_id_map = {}
        for practitioner in practitioners:
            response = fhir_request.create("Practitioner", practitioner)
            server_id = response.get('id')
            if not check_fhir_response(response, "Practitioner", server_id):
                raise Exception(f"Failed to create Practitioner: {response.get('issue', [{}])[0].get('diagnostics', 'Unknown error')}")
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
        for i, appointment in enumerate(appointments):
            print(f"\n--- Creating Appointment {i+1}/{len(appointments)} ---")
            print(f"Appointment participants before creation:")
            for j, participant in enumerate(appointment['participant']):
                print(f"  Participant {j+1}: {participant['actor']['reference']} (status: {participant['status']})")
            
            # Debug: Print reason field before sending (version-aware)
            if 'reasonCode' in appointment:
                print(f"Appointment reasonCode before creation (FHIR R4):")
                for j, reason in enumerate(appointment['reasonCode']):
                    if 'coding' in reason:
                        coding = reason['coding'][0]
                        print(f"  Reason {j+1}: {coding['display']} (Code: {coding['code']}, System: {coding['system']})")
            elif 'reason' in appointment:
                print(f"Appointment reason before creation (FHIR R5):")
                for j, reason in enumerate(appointment['reason']):
                    if 'concept' in reason and 'coding' in reason['concept']:
                        coding = reason['concept']['coding'][0]
                        print(f"  Reason {j+1}: {coding['display']} (Code: {coding['code']}, System: {coding['system']})")
            else:
                print("WARNING: No reason field found in appointment!")
            
            response = fhir_request.create("Appointment", appointment)
            
            # Enhanced error handling - check for any issues, not just errors
            if response.get('issue'):
                for issue in response['issue']:
                    severity = issue.get('severity', 'unknown')
                    diagnostics = issue.get('diagnostics', 'No details provided')
                    print(f"FHIR Server Issue - Severity: {severity}, Details: {diagnostics}")
                    
                    if severity == 'error':
                        print(f"ERROR: Failed to create appointment due to: {diagnostics}")
                        raise Exception(f"Appointment creation failed: {diagnostics}")
                    elif severity == 'warning':
                        print(f"WARNING: Appointment created with warnings: {diagnostics}")
            
            # Verify the created appointment has participants
            if response.get('id'):
                print(f"Created Appointment with ID: {response['id']}")
                
                # Fetch the created appointment to verify participants were stored
                try:
                    created_appointment = fhir_request.send_latest("Appointment", response['id'])
                    if 'participant' in created_appointment:
                        print(f"Verification - Stored participants:")
                        for j, participant in enumerate(created_appointment['participant']):
                            print(f"  Participant {j+1}: {participant['actor']['reference']} (status: {participant['status']})")
                    else:
                        print("WARNING: No participants found in stored appointment!")
                    
                    # Debug: Check if reason field was stored (version-aware)
                    if 'reasonCode' in created_appointment:
                        print(f"Verification - Stored reasonCode field (FHIR R4):")
                        for j, reason in enumerate(created_appointment['reasonCode']):
                            if 'coding' in reason:
                                coding = reason['coding'][0]
                                print(f"  Reason {j+1}: {coding['display']} (Code: {coding['code']}, System: {coding['system']})")
                    elif 'reason' in created_appointment:
                        print(f"Verification - Stored reason field (FHIR R5):")
                        for j, reason in enumerate(created_appointment['reason']):
                            if 'concept' in reason and 'coding' in reason['concept']:
                                coding = reason['concept']['coding'][0]
                                print(f"  Reason {j+1}: {coding['display']} (Code: {coding['code']}, System: {coding['system']})")
                    else:
                        print("WARNING: No reason field found in stored appointment!")
                        print(f"Available fields in stored appointment: {list(created_appointment.keys())}")
                except Exception as e:
                    print(f"Could not verify stored appointment: {e}")
            else:
                print("ERROR: No ID returned from appointment creation")
                print(f"Full response: {response}")
        
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
            server_id = response.get('id')
            if not check_fhir_response(response, "Procedure", server_id):
                raise Exception(f"Failed to create Procedure: {response.get('issue', [{}])[0].get('diagnostics', 'Unknown error')}")
            print(f"Created Procedure with ID: {server_id}")

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

        # Create encounters with updated references and store their server-assigned IDs
        encounter_id_map = {}
        for encounter in encounters:
            response = create_with_validation(fhir_request, "Encounter", encounter)
            server_id = response.get('id')
            if not check_fhir_response(response, "Encounter", server_id):
                raise Exception(f"Failed to create Encounter: {response.get('issue', [{}])[0].get('diagnostics', 'Unknown error')}")
            encounter_id_map[encounter['id']] = server_id
            print(f"Created Encounter with ID: {server_id}")

        # Create observations with updated references and store their server-assigned IDs
        observation_id_map = {}
        for observation in observations:
            response = fhir_request.create("Observation", observation)
            server_id = response.get('id')
            if not check_fhir_response(response, "Observation", server_id):
                raise Exception(f"Failed to create Observation: {response.get('issue', [{}])[0].get('diagnostics', 'Unknown error')}")
            observation_id_map[observation['id']] = server_id
            print(f"Created Observation with ID: {server_id}")

        # Create medication requests with updated references and store their server-assigned IDs
        medication_request_id_map = {}
        for medication_request in medication_requests:
            response = fhir_request.create("MedicationRequest", medication_request)
            server_id = response.get('id')
            if not check_fhir_response(response, "MedicationRequest", server_id):
                raise Exception(f"Failed to create MedicationRequest: {response.get('issue', [{}])[0].get('diagnostics', 'Unknown error')}")
            medication_request_id_map[medication_request['id']] = server_id
            print(f"Created MedicationRequest with ID: {server_id}")

        # Update diagnostic report references to use server-assigned IDs
        for diagnostic_report in diagnostic_reports:
            # Update patient reference
            original_patient_id = diagnostic_report['subject']['reference'].split('/')[1]
            server_patient_id = patient_id_map[original_patient_id]
            diagnostic_report['subject']['reference'] = f"Patient/{server_patient_id}"

            # Update practitioner reference
            original_practitioner_id = diagnostic_report['performer'][0]['reference'].split('/')[1]
            if original_practitioner_id in practitioner_id_map:
                server_practitioner_id = practitioner_id_map[original_practitioner_id]
                diagnostic_report['performer'][0]['reference'] = f"Practitioner/{server_practitioner_id}"

            # Update encounter reference
            original_encounter_id = diagnostic_report['encounter']['reference'].split('/')[1]
            server_encounter_id = encounter_id_map.get(original_encounter_id)
            if server_encounter_id:
                diagnostic_report['encounter']['reference'] = f"Encounter/{server_encounter_id}"

            # Update observation references
            for result in diagnostic_report.get('result', []):
                original_obs_id = result['reference'].split('/')[1]
                server_obs_id = observation_id_map.get(original_obs_id)
                if server_obs_id:
                    result['reference'] = f"Observation/{server_obs_id}"

        # Create diagnostic reports with updated references
        for diagnostic_report in diagnostic_reports:
            response = fhir_request.create("DiagnosticReport", diagnostic_report)
            server_id = response.get('id')
            if not check_fhir_response(response, "DiagnosticReport", server_id):
                raise Exception(f"Failed to create DiagnosticReport: {response.get('issue', [{}])[0].get('diagnostics', 'Unknown error')}")
            print(f"Created DiagnosticReport with ID: {server_id}")

        # Update service request references to use server-assigned IDs
        for service_request in service_requests:
            # Update patient reference
            original_patient_id = service_request['subject']['reference'].split('/')[1]
            server_patient_id = patient_id_map[original_patient_id]
            service_request['subject']['reference'] = f"Patient/{server_patient_id}"

            # Update practitioner reference
            original_practitioner_id = service_request['requester']['reference'].split('/')[1]
            if original_practitioner_id in practitioner_id_map:
                server_practitioner_id = practitioner_id_map[original_practitioner_id]
                service_request['requester']['reference'] = f"Practitioner/{server_practitioner_id}"

            # Update encounter reference if present
            if 'encounter' in service_request:
                original_encounter_id = service_request['encounter']['reference'].split('/')[1]
                server_encounter_id = encounter_id_map.get(original_encounter_id)
                if server_encounter_id:
                    service_request['encounter']['reference'] = f"Encounter/{server_encounter_id}"

        # Create service requests with updated references
        for service_request in service_requests:
            response = fhir_request.create("ServiceRequest", service_request)
            server_id = response.get('id')
            if not check_fhir_response(response, "ServiceRequest", server_id):
                raise Exception(f"Failed to create ServiceRequest: {response.get('issue', [{}])[0].get('diagnostics', 'Unknown error')}")
            print(f"Created ServiceRequest with ID: {server_id}")

        # Update clinical impression references to use server-assigned IDs
        for clinical_impression in clinical_impressions:
            # Update patient reference
            original_patient_id = clinical_impression['subject']['reference'].split('/')[1]
            server_patient_id = patient_id_map[original_patient_id]
            clinical_impression['subject']['reference'] = f"Patient/{server_patient_id}"

            # Update practitioner reference
            original_practitioner_id = clinical_impression['performer']['reference'].split('/')[1]
            if original_practitioner_id in practitioner_id_map:
                server_practitioner_id = practitioner_id_map[original_practitioner_id]
                clinical_impression['performer']['reference'] = f"Practitioner/{server_practitioner_id}"

            # Update encounter reference if present
            if 'encounter' in clinical_impression:
                original_encounter_id = clinical_impression['encounter']['reference'].split('/')[1]
                server_encounter_id = encounter_id_map.get(original_encounter_id)
                if server_encounter_id:
                    clinical_impression['encounter']['reference'] = f"Encounter/{server_encounter_id}"

        # Create clinical impressions with updated references
        for clinical_impression in clinical_impressions:
            response = fhir_request.create("ClinicalImpression", clinical_impression)
            server_id = response.get('id')
            if not check_fhir_response(response, "ClinicalImpression", server_id):
                raise Exception(f"Failed to create ClinicalImpression: {response.get('issue', [{}])[0].get('diagnostics', 'Unknown error')}")
            print(f"Created ClinicalImpression with ID: {server_id}")

        # Update family member history references to use server-assigned IDs
        for family_member_history in family_member_histories:
            # Update patient reference
            original_patient_id = family_member_history['patient']['reference'].split('/')[1]
            server_patient_id = patient_id_map[original_patient_id]
            family_member_history['patient']['reference'] = f"Patient/{server_patient_id}"

            # Update practitioner reference if present
            if 'recorder' in family_member_history:
                original_practitioner_id = family_member_history['recorder']['reference'].split('/')[1]
                if original_practitioner_id in practitioner_id_map:
                    server_practitioner_id = practitioner_id_map[original_practitioner_id]
                    family_member_history['recorder']['reference'] = f"Practitioner/{server_practitioner_id}"

        # Create family member histories with updated references
        for family_member_history in family_member_histories:
            response = fhir_request.create("FamilyMemberHistory", family_member_history)
            server_id = response.get('id')
            if not check_fhir_response(response, "FamilyMemberHistory", server_id):
                raise Exception(f"Failed to create FamilyMemberHistory: {response.get('issue', [{}])[0].get('diagnostics', 'Unknown error')}")
            print(f"Created FamilyMemberHistory with ID: {server_id}")

        # Update immunization references to use server-assigned IDs
        for immunization in immunizations:
            # Update patient reference
            original_patient_id = immunization['patient']['reference'].split('/')[1]
            server_patient_id = patient_id_map[original_patient_id]
            immunization['patient']['reference'] = f"Patient/{server_patient_id}"

            # Update practitioner references
            for performer in immunization.get('performer', []):
                original_practitioner_id = performer['actor']['reference'].split('/')[1]
                if original_practitioner_id in practitioner_id_map:
                    server_practitioner_id = practitioner_id_map[original_practitioner_id]
                    performer['actor']['reference'] = f"Practitioner/{server_practitioner_id}"

            # Update encounter reference if present
            if 'encounter' in immunization:
                original_encounter_id = immunization['encounter']['reference'].split('/')[1]
                server_encounter_id = encounter_id_map.get(original_encounter_id)
                if server_encounter_id:
                    immunization['encounter']['reference'] = f"Encounter/{server_encounter_id}"

            # Update location reference if present
            if 'location' in immunization:
                original_location_id = immunization['location']['reference'].split('/')[1]
                server_location_id = location_id_map[original_location_id]
                immunization['location']['reference'] = f"Location/{server_location_id}"

        # Create immunizations with updated references
        for immunization in immunizations:
            response = fhir_request.create("Immunization", immunization)
            server_id = response.get('id')
            if not check_fhir_response(response, "Immunization", server_id):
                raise Exception(f"Failed to create Immunization: {response.get('issue', [{}])[0].get('diagnostics', 'Unknown error')}")
            print(f"Created Immunization with ID: {server_id}")

        # Update medication administration references to use server-assigned IDs
        for medication_administration in medication_administrations:
            # Update patient reference
            original_patient_id = medication_administration['subject']['reference'].split('/')[1]
            server_patient_id = patient_id_map[original_patient_id]
            medication_administration['subject']['reference'] = f"Patient/{server_patient_id}"

            # Update practitioner reference
            original_practitioner_id = medication_administration['performer'][0]['actor']['reference']['reference'].split('/')[1]
            if original_practitioner_id in practitioner_id_map:
                server_practitioner_id = practitioner_id_map[original_practitioner_id]
                medication_administration['performer'][0]['actor']['reference']['reference'] = f"Practitioner/{server_practitioner_id}"

            # Update encounter reference if present
            if 'encounter' in medication_administration:
                original_encounter_id = medication_administration['encounter']['reference'].split('/')[1]
                server_encounter_id = encounter_id_map.get(original_encounter_id)
                if server_encounter_id:
                    medication_administration['encounter']['reference'] = f"Encounter/{server_encounter_id}"

            # Update medication request reference if present
            if 'request' in medication_administration:
                original_med_req_id = medication_administration['request']['reference'].split('/')[1]
                server_med_req_id = medication_request_id_map.get(original_med_req_id)
                if server_med_req_id:
                    medication_administration['request']['reference'] = f"MedicationRequest/{server_med_req_id}"

        # Create medication administrations with updated references
        for medication_administration in medication_administrations:
            response = fhir_request.create("MedicationAdministration", medication_administration)
            server_id = response.get('id')
            if not check_fhir_response(response, "MedicationAdministration", server_id):
                raise Exception(f"Failed to create MedicationAdministration: {response.get('issue', [{}])[0].get('diagnostics', 'Unknown error')}")
            print(f"Created MedicationAdministration with ID: {server_id}")

        # Update allergy intolerance references to use server-assigned IDs
        for allergy_intolerance in allergy_intolerances:
            # Update patient reference
            original_patient_id = allergy_intolerance['patient']['reference'].split('/')[1]
            server_patient_id = patient_id_map[original_patient_id]
            allergy_intolerance['patient']['reference'] = f"Patient/{server_patient_id}"

            # Update practitioner reference if present
            if 'recorder' in allergy_intolerance:
                original_practitioner_id = allergy_intolerance['recorder']['reference'].split('/')[1]
                if original_practitioner_id in practitioner_id_map:
                    server_practitioner_id = practitioner_id_map[original_practitioner_id]
                    allergy_intolerance['recorder']['reference'] = f"Practitioner/{server_practitioner_id}"

        # Create allergy intolerances with updated references
        for allergy_intolerance in allergy_intolerances:
            response = fhir_request.create("AllergyIntolerance", allergy_intolerance)
            server_id = response.get('id')
            if not check_fhir_response(response, "AllergyIntolerance", server_id):
                raise Exception(f"Failed to create AllergyIntolerance: {response.get('issue', [{}])[0].get('diagnostics', 'Unknown error')}")
            print(f"Created AllergyIntolerance with ID: {server_id}")

        # Update care plan references to use server-assigned IDs
        for care_plan in care_plans:
            # Update patient reference
            original_patient_id = care_plan['subject']['reference'].split('/')[1]
            server_patient_id = patient_id_map[original_patient_id]
            care_plan['subject']['reference'] = f"Patient/{server_patient_id}"

            # Update practitioner reference (R5 only - custodian field)
            if 'custodian' in care_plan:
                original_practitioner_id = care_plan['custodian']['reference'].split('/')[1]
                if original_practitioner_id in practitioner_id_map:
                    server_practitioner_id = practitioner_id_map[original_practitioner_id]
                    care_plan['custodian']['reference'] = f"Practitioner/{server_practitioner_id}"

            # Update encounter reference if present
            if 'encounter' in care_plan:
                original_encounter_id = care_plan['encounter']['reference'].split('/')[1]
                server_encounter_id = encounter_id_map.get(original_encounter_id)
                if server_encounter_id:
                    care_plan['encounter']['reference'] = f"Encounter/{server_encounter_id}"

            # Update contained condition reference if present
            for contained in care_plan.get('contained', []):
                if contained.get('resourceType') == 'Condition':
                    original_patient_id = contained['subject']['reference'].split('/')[1]
                    server_patient_id = patient_id_map[original_patient_id]
                    contained['subject']['reference'] = f"Patient/{server_patient_id}"

        # Create care plans with updated references
        for care_plan in care_plans:
            response = fhir_request.create("CarePlan", care_plan)
            server_id = response.get('id')
            if not check_fhir_response(response, "CarePlan", server_id):
                raise Exception(f"Failed to create CarePlan: {response.get('issue', [{}])[0].get('diagnostics', 'Unknown error')}")
            print(f"Created CarePlan with ID: {server_id}")

        # Update coverage references to use server-assigned IDs
        for coverage in coverages:
            # Update patient references
            original_patient_id = coverage['subscriber']['reference'].split('/')[1]
            server_patient_id = patient_id_map[original_patient_id]
            coverage['subscriber']['reference'] = f"Patient/{server_patient_id}"
            coverage['beneficiary']['reference'] = f"Patient/{server_patient_id}"

            # Update organization reference
            original_org_id = coverage['policyHolder']['reference'].split('/')[1]
            if original_org_id in organization_id_map:
                server_org_id = organization_id_map[original_org_id]
                coverage['policyHolder']['reference'] = f"Organization/{server_org_id}"
                coverage['insurer']['reference'] = f"Organization/{server_org_id}"

            # Update policy holder reference if different from patient
            if 'policyHolder' in coverage and coverage['policyHolder']['reference'].startswith('Patient/'):
                original_policy_holder_id = coverage['policyHolder']['reference'].split('/')[1]
                server_policy_holder_id = patient_id_map[original_policy_holder_id]
                coverage['policyHolder']['reference'] = f"Patient/{server_policy_holder_id}"

        # Create coverages with updated references
        for coverage in coverages:
            response = fhir_request.create("Coverage", coverage)
            server_id = response.get('id')
            if not check_fhir_response(response, "Coverage", server_id):
                raise Exception(f"Failed to create Coverage: {response.get('issue', [{}])[0].get('diagnostics', 'Unknown error')}")
            print(f"Created Coverage with ID: {server_id}")
        
        # Create Binary resources first and store their server-assigned IDs
        binary_id_map = {}
        for binary in binaries:
            response = fhir_request.create("Binary", binary)
            server_id = response.get('id')
            if not check_fhir_response(response, "Binary", server_id):
                raise Exception(f"Failed to create Binary: {response.get('issue', [{}])[0].get('diagnostics', 'Unknown error')}")
            binary_id_map[binary['id']] = server_id
            print(f"Created Binary with ID: {server_id}")
        
        # Update document reference references to use server-assigned IDs
        for document_reference in document_references:
            # Update patient reference
            original_patient_id = document_reference['subject']['reference'].split('/')[1]
            server_patient_id = patient_id_map[original_patient_id]
            document_reference['subject']['reference'] = f"Patient/{server_patient_id}"
            
            # Update practitioner reference
            original_practitioner_id = document_reference['author'][0]['reference'].split('/')[1]
            if original_practitioner_id in practitioner_id_map:
                server_practitioner_id = practitioner_id_map[original_practitioner_id]
                document_reference['author'][0]['reference'] = f"Practitioner/{server_practitioner_id}"
            
            # Update encounter reference
            original_encounter_id = document_reference['context'][0]['reference'].split('/')[1]
            server_encounter_id = encounter_id_map.get(original_encounter_id)
            if server_encounter_id:
                document_reference['context'][0]['reference'] = f"Encounter/{server_encounter_id}"
            
            # Update binary reference
            original_binary_id = document_reference['content'][0]['attachment']['url'].split('/')[1]
            server_binary_id = binary_id_map.get(original_binary_id)
            if server_binary_id:
                document_reference['content'][0]['attachment']['url'] = f"Binary/{server_binary_id}"
            
            # Update attester reference if present
            if 'attester' in document_reference:
                original_attester_id = document_reference['attester'][0]['party']['reference'].split('/')[1]
                if original_attester_id in practitioner_id_map:
                    server_attester_id = practitioner_id_map[original_attester_id]
                    document_reference['attester'][0]['party']['reference'] = f"Practitioner/{server_attester_id}"
        
        # Create document references with updated references
        for document_reference in document_references:
            response = fhir_request.create("DocumentReference", document_reference)
            server_id = response.get('id')
            if not check_fhir_response(response, "DocumentReference", server_id):
                raise Exception(f"Failed to create DocumentReference: {response.get('issue', [{}])[0].get('diagnostics', 'Unknown error')}")
            print(f"Created DocumentReference with ID: {server_id}")
        
        # Final verification: Check a few appointments to ensure participants are stored
        print("\n" + "="*60)
        print("FINAL VERIFICATION: Checking stored appointments for participants")

        for i in range(FINAL_VERIFICATION_CHECK_WAIT_TIME):
            print(f"Waiting {FINAL_VERIFICATION_CHECK_WAIT_TIME - i} seconds before verification...")
            time.sleep(1)

        print("="*60)
        
        try:
            # Get a sample of appointments from the server
            search_response = fhir_request.search("Appointment")
            if 'entry' in search_response and search_response['entry']:
                sample_size = min(3, len(search_response['entry']))
                print(f"Checking {sample_size} appointments from the server...")
                
                for i in range(sample_size):
                    appointment = search_response['entry'][i]['resource']
                    appointment_id = appointment.get('id', 'unknown')
                    print(f"\nAppointment {i+1} (ID: {appointment_id}):")
                    
                    if 'participant' in appointment and appointment['participant']:
                        print(f"  Found {len(appointment['participant'])} participants:")
                        for j, participant in enumerate(appointment['participant']):
                            actor_ref = participant.get('actor', {}).get('reference', 'No reference')
                            status = participant.get('status', 'No status')
                            print(f"    Participant {j+1}: {actor_ref} (status: {status})")
                    else:
                        print("  WARNING: No participants found in this appointment!")
                        print(f"  Full appointment structure: {list(appointment.keys())}")
            else:
                print("No appointments found in server response")
                print(f"Search response: {search_response}")
        except Exception as e:
            print(f"Could not verify appointments: {e}")
            print("This might be due to server configuration or search endpoint availability")


if __name__ == "__main__":
    main(output_filename="fhir_dummy_data.json", fhir_server=FHIRServerConfig(host=FHIR_HOST, port=FHIR_PORT, path=FHIR_PATH))

