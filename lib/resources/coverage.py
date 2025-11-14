"""
Coverage resource generation function.
"""
import uuid
import random
from datetime import timedelta
from faker import Faker
from typing import Dict, Any, Optional

from common import get_fhir_version
from lib.data.coverages import (COVERAGE_STATUSES, COVERAGE_KINDS, COVERAGE_TYPES,
                               COVERAGE_RELATIONSHIPS, COVERAGE_CLASS_TYPES,
                               INSURANCE_COMPANIES, COVERAGE_PLAN_NAMES,
                               COVERAGE_CLASS_NAMES, COVERAGE_TIER_NAMES,
                               COVERAGE_SUBCLASS_NAMES, COVERAGE_IDENTIFIERS,
                               COVERAGE_COST_SHARING, COVERAGE_NETWORK_TYPES,
                               COVERAGE_BENEFIT_TYPES)


# Initialize Faker to generate random data
fake = Faker()


def generate_coverage(patient_id: str, organization_id: str, 
                     policy_holder_id: Optional[str] = None) -> Dict[str, Any]:
    """
    Generates a single FHIR Coverage resource.
    
    :param patient_id: The ID of the patient who is the beneficiary.
    :param organization_id: The ID of the organization providing the coverage.
    :param policy_holder_id: Optional ID of the policy holder (if different from patient).
    :return: A dictionary representing the FHIR Coverage resource.
    """
    coverage_id = str(uuid.uuid4())
    status = random.choice(COVERAGE_STATUSES)
    kind = random.choice(COVERAGE_KINDS)
    # Filter out invalid coverage type codes (HS and VISION are not valid in v3-ActCode)
    valid_coverage_types = [t for t in COVERAGE_TYPES if t["code"] not in ["HS", "VISION"]]
    coverage_type = random.choice(valid_coverage_types if valid_coverage_types else COVERAGE_TYPES)
    relationship = random.choice(COVERAGE_RELATIONSHIPS)
    insurance_company = random.choice(INSURANCE_COMPANIES)
    plan_name = random.choice(COVERAGE_PLAN_NAMES)
    identifier_data = random.choice(COVERAGE_IDENTIFIERS)
    # Filter out invalid copay type codes (coinsurance is not valid)
    valid_cost_sharing = [c for c in COVERAGE_COST_SHARING if c["type"] != "coinsurance"]
    cost_sharing = random.choice(valid_cost_sharing if valid_cost_sharing else COVERAGE_COST_SHARING)
    network_type = random.choice(COVERAGE_NETWORK_TYPES)
    benefit_types = random.sample(COVERAGE_BENEFIT_TYPES, random.randint(3, 8))
    
    # Get FHIR version to determine field structure
    fhir_version = get_fhir_version()
    
    # Generate dates
    start_date = fake.date_between(start_date='-5y', end_date='-1d')
    end_date = start_date + timedelta(days=random.randint(365, 1095))  # 1-3 years
    
    # Generate identifier
    identifier_value = f"{identifier_data['value_prefix']}{fake.random_number(digits=6)}"
    
    # Generate coverage classes
    coverage_classes = []
    
    # Group class
    # In R4, class.value must be a simple string value, not an object
    group_class = {
        "type": {
            "coding": [
                {
                    "system": COVERAGE_CLASS_TYPES[0]["system"],
                    "code": COVERAGE_CLASS_TYPES[0]["code"],
                    "display": COVERAGE_CLASS_TYPES[0]["display"]
                }
            ]
        },
        "value": f"{insurance_company['code']}{fake.random_number(digits=3)}",
        "name": random.choice(COVERAGE_CLASS_NAMES)
    }
    coverage_classes.append(group_class)
    
    # Plan class
    plan_class = {
        "type": {
            "coding": [
                {
                    "system": COVERAGE_CLASS_TYPES[2]["system"],
                    "code": COVERAGE_CLASS_TYPES[2]["code"],
                    "display": COVERAGE_CLASS_TYPES[2]["display"]
                }
            ]
        },
        "value": f"{fake.random_letter().upper()}{fake.random_number(digits=4)}",
        "name": plan_name
    }
    coverage_classes.append(plan_class)
    
    # Class (tier)
    tier_class = {
        "type": {
            "coding": [
                {
                    "system": COVERAGE_CLASS_TYPES[4]["system"],
                    "code": COVERAGE_CLASS_TYPES[4]["code"],
                    "display": COVERAGE_CLASS_TYPES[4]["display"]
                }
            ]
        },
        "value": random.choice(COVERAGE_TIER_NAMES),
        "name": f"{random.choice(COVERAGE_TIER_NAMES)}: {plan_name}"
    }
    coverage_classes.append(tier_class)
    
    # Subclass
    subclass = {
        "type": {
            "coding": [
                {
                    "system": COVERAGE_CLASS_TYPES[5]["system"],
                    "code": COVERAGE_CLASS_TYPES[5]["code"],
                    "display": COVERAGE_CLASS_TYPES[5]["display"]
                }
            ]
        },
        "value": random.choice(COVERAGE_SUBCLASS_NAMES),
        "name": f"{random.choice(COVERAGE_SUBCLASS_NAMES)}, max ${cost_sharing.get('amount', 50)} copay"
    }
    coverage_classes.append(subclass)
    
    # Add pharmacy classes if applicable
    if random.random() < 0.7:  # 70% chance of pharmacy coverage
        rx_classes = [
            {
                "type": {
                    "coding": [
                        {
                            "system": COVERAGE_CLASS_TYPES[7]["system"],
                            "code": COVERAGE_CLASS_TYPES[7]["code"],
                            "display": COVERAGE_CLASS_TYPES[7]["display"]
                        }
                    ]
                },
                "value": f"RX{fake.random_number(digits=5)}"
            },
            {
                "type": {
                    "coding": [
                        {
                            "system": COVERAGE_CLASS_TYPES[8]["system"],
                            "code": COVERAGE_CLASS_TYPES[8]["code"],
                            "display": COVERAGE_CLASS_TYPES[8]["display"]
                        }
                    ]
                },
                "value": f"{fake.random_number(digits=6)}"
            },
            {
                "type": {
                    "coding": [
                        {
                            "system": COVERAGE_CLASS_TYPES[9]["system"],
                            "code": COVERAGE_CLASS_TYPES[9]["code"],
                            "display": COVERAGE_CLASS_TYPES[9]["display"]
                        }
                    ]
                },
                "value": f"{fake.random_letter().upper()}{fake.random_number(digits=4)}"
            },
            {
                "type": {
                    "coding": [
                        {
                            "system": COVERAGE_CLASS_TYPES[10]["system"],
                            "code": COVERAGE_CLASS_TYPES[10]["code"],
                            "display": COVERAGE_CLASS_TYPES[10]["display"]
                        }
                    ]
                },
                "value": f"{fake.random_number(digits=6)}"
            }
        ]
        coverage_classes.extend(rx_classes)
    
    # Create the coverage resource
    coverage = {
        "resourceType": "Coverage",
        "id": coverage_id,
        "identifier": [
            {
                "system": identifier_data["system"],
                "value": identifier_value
            }
        ],
        "status": status,
        "type": {
            "coding": [
                {
                    "system": coverage_type["system"],
                    "code": coverage_type["code"],
                    "display": coverage_type["display"]
                }
            ]
        },
        "policyHolder": {
            "reference": f"Organization/{organization_id}",
            "display": insurance_company["display"]
        },
        "subscriber": {
            "reference": f"Patient/{patient_id}",
            "display": f"Patient {patient_id[:8]}"
        },
        "beneficiary": {
            "reference": f"Patient/{patient_id}",
            "display": f"Patient {patient_id[:8]}"
        },
        "dependent": str(random.randint(0, 5)),
        "relationship": {
            "coding": [
                {
                    "system": relationship["system"],
                    "code": relationship["code"],
                    "display": relationship["display"]
                }
            ]
        },
        "period": {
            "start": start_date.isoformat(),
            "end": end_date.isoformat()
        },
        "class": coverage_classes
    }
    
    # Add version-specific fields
    if fhir_version == "R4":
        # R4: payor is required (not insurer)
        coverage["payor"] = [
            {
                "reference": f"Organization/{organization_id}",
                "display": insurance_company["display"]
            }
        ]
    else:  # FHIR R5
        # R5: kind and insurer are available
        coverage["kind"] = kind
        coverage["insurer"] = {
            "reference": f"Organization/{organization_id}",
            "display": insurance_company["display"]
        }
    
    # Add policy holder if different from patient
    if policy_holder_id and policy_holder_id != patient_id:
        coverage["policyHolder"] = {
            "reference": f"Patient/{policy_holder_id}",
            "display": f"Patient {policy_holder_id[:8]}"
        }
    
    # Add cost sharing information (30% chance)
    # Only include valid copay types (copay, deductible) - coinsurance is not valid
    if random.random() < 0.3 and cost_sharing["type"] in ["copay", "deductible"]:
        coverage["costToBeneficiary"] = [
            {
                "type": {
                    "coding": [
                        {
                            "system": "http://terminology.hl7.org/CodeSystem/coverage-copay-type",
                            "code": cost_sharing["type"],
                            "display": cost_sharing["display"]
                        }
                    ]
                },
                "valueMoney": {
                    "value": cost_sharing.get("amount", 25),
                    "currency": "USD"
                }
            }
        ]
    
    # Add network information (40% chance)
    if random.random() < 0.4:
        coverage["network"] = f"{insurance_company['name']} {network_type} Network"
    
    # Add benefit information (50% chance) - only in R5
    if random.random() < 0.5 and fhir_version != "R4":
        coverage["benefit"] = [
            {
                "type": {
                    "coding": [
                        {
                            "system": "http://terminology.hl7.org/CodeSystem/coverage-benefit-type",
                            "code": benefit_type.upper().replace(" ", "_"),
                            "display": benefit_type
                        }
                    ]
                }
            } for benefit_type in benefit_types
        ]
    
    # Generate text narrative
    coverage["text"] = {
        "status": "generated",
        "div": f"""<div xmlns="http://www.w3.org/1999/xhtml">
            <p><b>Coverage Information</b></p>
            <p><b>Insurance Company:</b> {insurance_company['display']}</p>
            <p><b>Plan:</b> {plan_name}</p>
            <p><b>Type:</b> {coverage_type['display']}</p>
            <p><b>Status:</b> {status}</p>
            {f'<p><b>Kind:</b> {kind}</p>' if fhir_version != "R4" else ''}
            <p><b>Relationship:</b> {relationship['display']}</p>
            <p><b>Period:</b> {start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')}</p>
            <p><b>Network:</b> {network_type}</p>
            {f'<p><b>Benefits:</b> {", ".join(benefit_types)}</p>' if fhir_version != "R4" else ''}
            <p><b>Identifier:</b> {identifier_value}</p>
        </div>"""
    }
    
    return coverage
