"""
Some helper scripts for generating FHIR data for testing environments.
"""
import random
from faker import Faker

from lib.crud import Request
from lib.resources import generate_clinic_and_location, generate_patient, generate_practitioner, generate_condition, generate_appointment


# Initialize Faker to generate random data
fake = Faker()


def main():
    """Main function to generate a set of interconnected FHIR resources."""
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

    # Combine all generated resources into a single dictionary
    fhir_bundle = {
        "patients": patients,
        "practitioners": practitioners,
        "clinics": clinics,
        "locations": locations,
        "conditions": conditions,
        "appointments": appointments
    }

    # Write the output to a JSON file
    output_filename = "fhir_dummy_data.json"
    #with open(output_filename, 'w') as f: json.dump(fhir_bundle, f, indent=2)

    print(f"\nSuccessfully generated dummy data and saved it to '{output_filename}'")
    print(f" - Patients: {len(patients)}")
    print(f" - Practitioners: {len(practitioners)}")
    print(f" - Clinics: {len(clinics)}")
    print(f" - Locations: {len(locations)}")
    print(f" - Conditions: {len(conditions)}")
    print(f" - Appointments: {len(appointments)}")

    # Example of sending a request using the Request class from lib.crud
    # Note: Uncomment and configure the following lines to test sending requests
    fhir_request = Request(host="localhost", port=8080, path="/fhir")
    for clinic in clinics:
        response = fhir_request.create("Organization", clinic)
        if response.get('issue') and response['issue'][0]['severity'] == 'error':
            err = response['issue'][0]['diagnostics']
            print(err)
            raise Exception(err)
        print(f"Created Organization with ID: {response.get('id')}")
    for location in locations:
        response = fhir_request.create("Location", location)
        if response.get('issue') and response['issue'][0]['severity'] == 'error':
            err = response['issue'][0]['diagnostics']
            print(err)
            raise Exception(err)
        print(f"Created Location with ID: {response.get('id')}")
    for condition in conditions:
        response = fhir_request.create("Condition", condition)
        if response.get('issue') and response['issue'][0]['severity'] == 'error':
            err = response['issue'][0]['diagnostics']
            print(err)
            raise Exception(err)
        print(f"Created Condition with ID: {response.get('id')}")
    for patient in patients:
        response = fhir_request.create("Patient", patient)
        if response.get('issue') and response['issue'][0]['severity'] == 'error':
            err = response['issue'][0]['diagnostics']
            print(err)
            raise Exception(err)
        print(f"Created Patient with ID: {response.get('id')}")
    for practitioner in practitioners:
        response = fhir_request.create("Practitioner", practitioner)
        if response.get('issue') and response['issue'][0]['severity'] == 'error':
            err = response['issue'][0]['diagnostics']
            print(err)
            raise Exception(err)
        print(f"Created Practitioner with ID: {response.get('id')}")
    for appointment in appointments:
        response = fhir_request.create("Appointment", appointment)
        if response.get('issue') and response['issue'][0]['severity'] == 'error':
            err = response['issue'][0]['diagnostics']
            print(err)
            raise Exception(err)
        print(f"Created Appointment with ID: {response.get('id')}")


if __name__ == "__main__":
    main()
