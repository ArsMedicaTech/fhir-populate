"""
Update Observations from LOINC Data

This script reads the generated loinc.json file and updates the observations.py
file with real LOINC data instead of the hardcoded observations.

Usage:
    python update_observations_from_loinc.py
"""

import json
import os
from typing import List, Dict, Any

def load_loinc_data(json_path: str) -> Dict[str, Any]:
    """
    Load LOINC data from JSON file.
    
    :param json_path: Path to the LOINC JSON file
        
    :return: LOINC data dictionary
    """
    with open(json_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def convert_loinc_to_observations(loinc_data: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    Convert LOINC data to observations format.
    
    :param loinc_data: LOINC data dictionary
        
    :return: List of observations in the expected format
    """
    observations = []
    
    for obs in loinc_data['observations']:
        # Convert to the format expected by the observations.py file
        observation = {
            'code': obs['code'],
            'display': obs['display'],
            'text': obs['text'],
            'system': obs['system'],
            'category': obs['category'],
            'unit': obs['unit'],
            'unit_system': obs['unit_system'],
            'unit_code': obs['unit_code'],
            'normal_range': obs['normal_range'],
            'interpretations': obs['interpretations']
        }
        observations.append(observation)
    
    return observations

def generate_observations_py(observations: List[Dict[str, Any]]) -> str:
    """
    Generate the observations.py file content.
    
    :param observations: List of observations
        
    :return: Python file content as string
    """
    content = '''"""
Common laboratory observations for FHIR Observation resources.
Generated from official LOINC database.
Includes LOINC codes, normal ranges, units, and interpretations.
"""

OBSERVATIONS = [
'''
    
    for i, obs in enumerate(observations):
        content += '    {\n'
        content += f'        "code": "{obs["code"]}",\n'
        content += f'        "display": "{obs["display"]}",\n'
        content += f'        "text": "{obs["text"]}",\n'
        content += f'        "system": "{obs["system"]}",\n'
        content += f'        "category": "{obs["category"]}",\n'
        content += f'        "unit": "{obs["unit"]}",\n'
        content += f'        "unit_system": "{obs["unit_system"]}",\n'
        content += f'        "unit_code": "{obs["unit_code"]}",\n'
        content += f'        "normal_range": {obs["normal_range"]},\n'
        content += f'        "interpretations": {obs["interpretations"]}\n'
        content += '    }'
        
        if i < len(observations) - 1:
            content += ','
        content += '\n'
    
    content += ''']

# Common observation statuses
OBSERVATION_STATUSES = ["registered", "preliminary", "final", "amended", "cancelled", "entered-in-error", "unknown"]

# Common observation categories
OBSERVATION_CATEGORIES = [
    {
        "coding": [
            {
                "system": "http://terminology.hl7.org/CodeSystem/observation-category",
                "code": "laboratory",
                "display": "Laboratory"
            }
        ]
    },
    {
        "coding": [
            {
                "system": "http://terminology.hl7.org/CodeSystem/observation-category",
                "code": "vital-signs",
                "display": "Vital Signs"
            }
        ]
    },
    {
        "coding": [
            {
                "system": "http://terminology.hl7.org/CodeSystem/observation-category",
                "code": "imaging",
                "display": "Imaging"
            }
        ]
    },
    {
        "coding": [
            {
                "system": "http://terminology.hl7.org/CodeSystem/observation-category",
                "code": "social-history",
                "display": "Social History"
            }
        ]
    }
]

# Interpretation codes
INTERPRETATION_CODES = {
    "LOW": {
        "system": "http://terminology.hl7.org/CodeSystem/v3-ObservationInterpretation",
        "code": "L",
        "display": "Low"
    },
    "NORMAL": {
        "system": "http://terminology.hl7.org/CodeSystem/v3-ObservationInterpretation",
        "code": "N",
        "display": "Normal"
    },
    "HIGH": {
        "system": "http://terminology.hl7.org/CodeSystem/v3-ObservationInterpretation",
        "code": "H",
        "display": "High"
    }
}
'''
    
    return content

def main() -> None:
    """Main function to update observations.py from LOINC data."""
    print("Updating observations.py from LOINC data...")
    
    # Check if loinc.json exists
    if not os.path.exists('loinc.json'):
        print("Error: loinc.json not found. Please run generate_loinc_data.py first.")
        return
    
    # Load LOINC data
    try:
        loinc_data = load_loinc_data('loinc.json')
        print(f"Loaded {len(loinc_data['observations'])} observations from LOINC data")
    except Exception as e:
        print(f"Error loading LOINC data: {e}")
        return
    
    # Convert to observations format
    observations = convert_loinc_to_observations(loinc_data)
    print(f"Converted {len(observations)} observations")
    
    # Generate Python file content
    try:
        content = generate_observations_py(observations)
        
        # Write to observations.py
        with open('lib/data/observations.py', 'w', encoding='utf-8') as f:
            f.write(content)
        
        print("Successfully updated lib/data/observations.py")
        
        # Print summary
        print(f"\nSummary:")
        print(f"- Total observations: {len(observations)}")
        
        # Count by units
        unit_counts = {}
        for obs in observations:
            unit = obs['unit']
            unit_counts[unit] = unit_counts.get(unit, 0) + 1
        
        print("- Observations by unit:")
        for unit, count in sorted(unit_counts.items()):
            print(f"  - {unit}: {count}")
        
        print(f"\nTop 10 observations:")
        for i, obs in enumerate(observations[:10]):
            print(f"  {i+1}. {obs['text']} ({obs['code']}) - {obs['unit']}")
            
    except Exception as e:
        print(f"Error updating observations.py: {e}")

if __name__ == "__main__":
    main()
