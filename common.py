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
