""" Common utils and configurations for FHIR population scripts. """
import os
from typing import Any, Dict
import dotenv

from faker import Faker


dotenv.load_dotenv()

FHIR_HOST = os.getenv("FHIR_HOST", "localhost")
FHIR_PORT_VAR = os.getenv("FHIR_PORT", "8080")
if FHIR_PORT_VAR.isdigit():
    FHIR_PORT = int(FHIR_PORT_VAR)
else:
    FHIR_PORT = None
FHIR_PATH = os.getenv("FHIR_PATH", "/fhir")


FINAL_VERIFICATION_CHECK_WAIT_TIME = 30


WARNINGS_TO_IGNORE = [
    "Unable to expand ValueSet: cannot apply filters",
    "Unable to expand ValueSet because CodeSystem could not be found: http://loinc.org",
]


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


def check_fhir_response(response: Dict[str, Any], resource_type: str, resource_id: str = None) -> bool:
    """
    Check FHIR server response for warnings and errors.
    Prints warnings and returns False if there are errors.
    
    Note: HAPI FHIR's LenientErrorHandler may log warnings to server logs
    without including them in the HTTP response. This function only catches
    warnings/errors that are returned in the response's 'issue' field.
    Server-side validation warnings may not be caught here.
    
    :param response: The FHIR server response dictionary
    :param resource_type: The type of resource being created/updated
    :param resource_id: Optional resource ID for better error messages
    :return: True if successful (no errors), False if errors found
    """
    if not response.get('issue'):
        return True
    
    has_errors = False
    has_warnings = False
    
    for issue in response['issue']:
        severity = issue.get('severity', 'unknown')
        diagnostics = issue.get('diagnostics', 'No details provided')
        code = issue.get('code', 'unknown')
        expression = issue.get('expression', [])
        
        if severity == 'error':
            has_errors = True
            resource_info = f" (ID: {resource_id})" if resource_id else ""
            print(f"❌ ERROR creating {resource_type}{resource_info}: {diagnostics}")
            if code:
                print(f"   Code: {code}")
            if expression:
                print(f"   Location: {', '.join(expression)}")
        elif severity == 'warning':
            has_warnings = True
            resource_info = f" (ID: {resource_id})" if resource_id else ""
            if any(warning in diagnostics for warning in WARNINGS_TO_IGNORE):
                pass
            else:
                print(f"⚠️  WARNING for {resource_type}{resource_info}: {diagnostics}")
            if code:
                print(f"   Code: {code}")
            if expression:
                print(f"   Location: {', '.join(expression)}")
        elif severity == 'information':
            # Only print if verbose mode (could add flag later)
            pass
    
    if has_errors:
        return False
    if has_warnings:
        print(f"   (Resource was created but may have validation issues)")
    
    return True


def get_fhir_version() -> str:
    """
    Get the FHIR version from environment variable or default to R4.
    
    :return: FHIR version string ('R4' or 'R5')
    """
    fhir_version = os.getenv('FHIR_VERSION', 'R4').upper()
    if fhir_version not in ['R4', 'R5']:
        print(f"Warning: Invalid FHIR_VERSION '{fhir_version}', defaulting to R4")
        fhir_version = 'R4'
    return fhir_version


def should_validate_resources() -> bool:
    """
    Check if resource validation should be performed before creation.
    Uses FHIR_VALIDATE environment variable (default: False).
    
    :return: True if validation should be performed, False otherwise
    """
    validate_env = os.getenv('FHIR_VALIDATE', 'false').lower()
    return validate_env in ['true', '1', 'yes', 'on']


def create_with_validation(fhir_request, resource_type: str, resource_data: Dict[str, Any], 
                          validate: bool = False) -> Dict[str, Any]:
    """
    Create a FHIR resource, optionally validating it first.
    
    :param fhir_request: The Request object for making FHIR calls
    :param resource_type: The type of resource to create
    :param resource_data: The resource data to create
    :param validate: Whether to validate before creating (default: False, or use FHIR_VALIDATE env var)
    :return: The creation response from the FHIR server
    """
    # Validate if requested (either via parameter or env var)
    if validate or should_validate_resources():
        try:
            validation_response = fhir_request.validate(resource_type, resource_data)
            # Check validation response - this will print warnings/errors
            validation_passed = check_fhir_response(validation_response, f"{resource_type} (validation)", None)
            if not validation_passed:
                print(f"⚠️  Validation found errors for {resource_type}, but proceeding with creation...")
        except Exception as e:
            print(f"⚠️  Validation request failed for {resource_type}: {e}")
            print("   Proceeding with creation anyway...")
    
    # Create the resource
    return fhir_request.create(resource_type, resource_data)
