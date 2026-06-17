"""
LOINC Data Generator

This script reads the official LOINC CSV file and generates a structured JSON file
with common laboratory observations, including proper LOINC codes, names, units,
and clinical reference ranges.

Usage:
    python generate_loinc_data.py

Requirements:
    - loinc/LoincTable/Loinc.csv (official LOINC database)
    - pandas (for CSV processing)
"""

UNITS_OF_MEASURE_RESOURCE = 'http://unitsofmeasure.org'

import csv
import json
from typing import Dict, List, Any

def load_loinc_data(csv_path: str) -> List[Dict[str, Any]]:
    """
    Load LOINC data from CSV file.
    
    :param csv_path: Path to the LOINC CSV file
        
    :return: list: List of LOINC records as dictionaries
    """
    loinc_data = []
    
    with open(csv_path, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            loinc_data.append(row)
    
    return loinc_data

def is_laboratory_test(loinc_record: Dict[str, Any]) -> bool:
    """
    Determine if a LOINC record represents a laboratory test.

    :param loinc_record: A single LOINC record
    :return: bool: True if it's a laboratory test, False otherwise
    """
    # Check if it's a quantitative test
    scale_type = loinc_record.get('SCALE_TYP', '').upper()
    if scale_type not in ['QN', 'ORD']:  # Quantitative or Ordinal
        return False
    
    # Check if it's a laboratory class (CLASSTYPE 1 = Chemistry, 2 = Clinical, etc.)
    class_type = loinc_record.get('CLASSTYPE', '')
    if class_type not in ['1', '2']:  # Chemistry or Clinical
        return False
    
    # Check if it has units
    example_units = loinc_record.get('EXAMPLE_UNITS', '')
    if not example_units or example_units.strip() == '':
        return False
    
    # Check if it's active
    status = loinc_record.get('STATUS', '').upper()
    if status != 'ACTIVE':
        return False
    
    # Check if it has a common test rank (indicates it's commonly used)
    common_test_rank = loinc_record.get('COMMON_TEST_RANK', '')
    if not common_test_rank or common_test_rank == '0':
        return False
    
    # Check if it's a blood/serum/plasma test (common laboratory specimens)
    system = loinc_record.get('SYSTEM', '').upper()
    if not any(specimen in system for specimen in ['BLOOD', 'SERUM', 'PLASMA', 'URINE', 'CSF']):
        return False
    
    return True

def extract_units(example_units: str) -> Dict[str, str]:
    """
    Extract and standardize units from LOINC example units.
    
    :param example_units: Example units string from LOINC
    :return: Dictionary with unit, system, and code
    """
    # Common unit mappings
    unit_mappings = {
        'mg/dL': {'unit': 'mg/dL', 'system':  UNITS_OF_MEASURE_RESOURCE, 'code': 'mg/dL'},
        'g/dL': {'unit': 'g/dL', 'system':  UNITS_OF_MEASURE_RESOURCE, 'code': 'g/dL'},
        'mEq/L': {'unit': 'mEq/L', 'system':  UNITS_OF_MEASURE_RESOURCE, 'code': 'mEq/L'},
        'mmol/L': {'unit': 'mmol/L', 'system':  UNITS_OF_MEASURE_RESOURCE, 'code': 'mmol/L'},
        'U/L': {'unit': 'U/L', 'system':  UNITS_OF_MEASURE_RESOURCE, 'code': 'U/L'},
        'IU/mL': {'unit': 'IU/mL', 'system':  UNITS_OF_MEASURE_RESOURCE, 'code': 'IU/mL'},
        'ng/mL': {'unit': 'ng/mL', 'system':  UNITS_OF_MEASURE_RESOURCE, 'code': 'ng/mL'},
        'pg/mL': {'unit': 'pg/mL', 'system':  UNITS_OF_MEASURE_RESOURCE, 'code': 'pg/mL'},
        'mcg/dL': {'unit': 'mcg/dL', 'system':  UNITS_OF_MEASURE_RESOURCE, 'code': 'mcg/dL'},
        'K/uL': {'unit': 'K/uL', 'system':  UNITS_OF_MEASURE_RESOURCE, 'code': 'K/uL'},
        'M/uL': {'unit': 'M/uL', 'system':  UNITS_OF_MEASURE_RESOURCE, 'code': 'M/uL'},
        '%': {'unit': '%', 'system':  UNITS_OF_MEASURE_RESOURCE, 'code': '%'},
        'sec': {'unit': 'sec', 'system':  UNITS_OF_MEASURE_RESOURCE, 'code': 'sec'},
        'mm/hr': {'unit': 'mm/hr', 'system':  UNITS_OF_MEASURE_RESOURCE, 'code': 'mm/hr'},
        'mg/L': {'unit': 'mg/L', 'system':  UNITS_OF_MEASURE_RESOURCE, 'code': 'mg/L'},
        'mIU/L': {'unit': 'mIU/L', 'system':  UNITS_OF_MEASURE_RESOURCE, 'code': 'mIU/L'},
    }
    
    # Try to find a matching unit
    for unit_key, unit_info in unit_mappings.items():
        if unit_key in example_units:
            return unit_info
    
    # Default fallback
    return {'unit': example_units, 'system':  UNITS_OF_MEASURE_RESOURCE, 'code': example_units}

def get_clinical_reference_ranges(loinc_code: str, component: str, units: str) -> Dict[str, Any]:
    """
    Get clinical reference ranges based on LOINC code and component.
    
    :param loinc_code: LOINC code
    :param component: Component name
    :param units: Units of measurement
        
    :return: Dictionary with normal ranges and interpretations
    """
    # Common laboratory reference ranges
    reference_ranges = {
        # Basic Metabolic Panel
        'GLUC': {'normal': (70, 100), 'unit': 'mg/dL'},
        'NA': {'normal': (136, 145), 'unit': 'mEq/L'},
        'K': {'normal': (3.5, 5.0), 'unit': 'mEq/L'},
        'CL': {'normal': (98, 107), 'unit': 'mEq/L'},
        'CO2': {'normal': (22, 28), 'unit': 'mEq/L'},
        'BUN': {'normal': (7, 20), 'unit': 'mg/dL'},
        'CREAT': {'normal': (0.6, 1.2), 'unit': 'mg/dL'},
        'CA': {'normal': (8.5, 10.5), 'unit': 'mg/dL'},
        
        # Lipid Panel
        'CHOL': {'normal': (0, 200), 'unit': 'mg/dL'},
        'HDL': {'normal': (40, 100), 'unit': 'mg/dL'},
        'LDL': {'normal': (0, 100), 'unit': 'mg/dL'},
        'TRIG': {'normal': (0, 150), 'unit': 'mg/dL'},
        
        # Complete Blood Count
        'WBC': {'normal': (4.5, 11.0), 'unit': 'K/uL'},
        'RBC': {'normal': (4.5, 5.9), 'unit': 'M/uL'},
        'HGB': {'normal': (12.0, 16.0), 'unit': 'g/dL'},
        'HCT': {'normal': (36, 46), 'unit': '%'},
        'PLT': {'normal': (150, 450), 'unit': 'K/uL'},
        
        # Liver Function
        'ALT': {'normal': (7, 56), 'unit': 'U/L'},
        'AST': {'normal': (10, 40), 'unit': 'U/L'},
        'ALP': {'normal': (44, 147), 'unit': 'U/L'},
        'TBIL': {'normal': (0.3, 1.2), 'unit': 'mg/dL'},
        'ALB': {'normal': (3.5, 5.0), 'unit': 'g/dL'},
        'TP': {'normal': (6.0, 8.3), 'unit': 'g/dL'},
        
        # Thyroid Function
        'TSH': {'normal': (0.4, 4.0), 'unit': 'mIU/L'},
        'T4': {'normal': (0.8, 1.8), 'unit': 'ng/dL'},
        'T3': {'normal': (2.3, 4.2), 'unit': 'pg/mL'},
        
        # Cardiac Markers
        'BNP': {'normal': (0, 100), 'unit': 'pg/mL'},
        'NTBNP': {'normal': (0, 300), 'unit': 'pg/mL'},
        
        # Coagulation
        'PT': {'normal': (11, 13), 'unit': 'sec'},
        'PTT': {'normal': (25, 35), 'unit': 'sec'},
        'INR': {'normal': (0.8, 1.1), 'unit': ''},
        
        # Vitamins
        'B12': {'normal': (200, 900), 'unit': 'pg/mL'},
        'FOL': {'normal': (3.0, 17.0), 'unit': 'ng/mL'},
        'D25': {'normal': (30, 100), 'unit': 'ng/mL'},
        
        # Inflammatory Markers
        'CRP': {'normal': (0, 3.0), 'unit': 'mg/L'},
        'ESR': {'normal': (0, 20), 'unit': 'mm/hr'},
        
        # Tumor Markers
        'PSA': {'normal': (0, 4.0), 'unit': 'ng/mL'},
        
        # Diabetes
        'HBA1C': {'normal': (4.0, 5.6), 'unit': '%'},
    }
    
    # Try to match component
    component_upper = component.upper()
    for key, ranges in reference_ranges.items():
        if key in component_upper:
            normal_low, normal_high = ranges['normal']
            return {
                'normal_range': {'low': normal_low, 'high': normal_high},
                'interpretations': {
                    'LOW': {'low': normal_low - (normal_high - normal_low), 'high': normal_low - 0.1},
                    'NORMAL': {'low': normal_low, 'high': normal_high},
                    'HIGH': {'low': normal_high + 0.1, 'high': normal_high + (normal_high - normal_low) * 2}
                }
            }
    
    # Default ranges for unknown tests
    return {
        'normal_range': {'low': 0, 'high': 100},
        'interpretations': {
            'LOW': {'low': 0, 'high': 0},
            'NORMAL': {'low': 1, 'high': 100},
            'HIGH': {'low': 101, 'high': 1000}
        }
    }

# Sort by common test rank (if available) to prioritize common tests
def get_rank(record: Dict[str, Any]) -> int:
    """
    Get the common test rank for sorting.
    :param record: LOINC record
    :return: Rank as integer (lower is more common)
    """
    rank = record.get('COMMON_TEST_RANK', '')
    try:
        return int(rank) if rank and rank != '0' else 999999
    except (ValueError, TypeError):
        return 999999

def process_loinc_data(loinc_data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Process LOINC data and extract laboratory observations.
    
    :param loinc_data: Raw LOINC data
        
    :return: Processed laboratory observations
    """
    observations = []
    seen_codes = set()
    
    # Filter for laboratory tests
    lab_tests = [record for record in loinc_data if is_laboratory_test(record)]
    
    lab_tests.sort(key=get_rank)
    
    for record in lab_tests:
        loinc_code = record.get('LOINC_NUM', '')
        if not loinc_code or loinc_code in seen_codes:
            continue
            
        seen_codes.add(loinc_code)
        
        # Extract basic information
        component = record.get('COMPONENT', '')
        long_name = record.get('LONG_COMMON_NAME', '')
        short_name = record.get('SHORTNAME', '')
        example_units = record.get('EXAMPLE_UNITS', '')
        
        if not component or not long_name:
            continue
        
        # Extract units
        unit_info = extract_units(example_units)
        
        # Get reference ranges
        reference_info = get_clinical_reference_ranges(loinc_code, component, unit_info['unit'])
        
        # Create observation record
        observation = {
            'code': loinc_code,
            'display': long_name,
            'text': short_name or component,
            'system': 'http://loinc.org',
            'category': 'laboratory',
            'unit': unit_info['unit'],
            'unit_system': unit_info['system'],
            'unit_code': unit_info['code'],
            'normal_range': reference_info['normal_range'],
            'interpretations': reference_info['interpretations'],
            'component': component,
            'property': record.get('PROPERTY', ''),
            'time_aspect': record.get('TIME_ASPCT', ''),
            'system_specimen': record.get('SYSTEM', ''),
            'scale_type': record.get('SCALE_TYP', ''),
            'method_type': record.get('METHOD_TYP', ''),
            'class_type': record.get('CLASSTYPE', ''),
            'definition': record.get('DefinitionDescription', ''),
            'status': record.get('STATUS', ''),
            'consumer_name': record.get('CONSUMER_NAME', ''),
            'example_answers': record.get('EXMPL_ANSWERS', ''),
            'related_names': record.get('RELATEDNAMES2', ''),
            'common_test_rank': record.get('COMMON_TEST_RANK', ''),
            'common_order_rank': record.get('COMMON_ORDER_RANK', ''),
            'version_last_changed': record.get('VersionLastChanged', ''),
            'version_first_released': record.get('VersionFirstReleased', '')
        }
        
        observations.append(observation)
        
        # Limit to top 1000 most common tests
        if len(observations) >= 1000:
            break
    
    return observations

def main() -> None:
    """Main function to generate LOINC JSON data."""
    print("Loading LOINC data from CSV...")
    
    # Load LOINC data
    csv_path = 'loinc/LoincTable/Loinc.csv'
    try:
        loinc_data = load_loinc_data(csv_path)
        print(f"Loaded {len(loinc_data)} LOINC records")
    except FileNotFoundError:
        print(f"Error: Could not find LOINC CSV file at {csv_path}")
        print("Please ensure the file exists and try again.")
        return
    except Exception as e:
        print(f"Error loading LOINC data: {e}")
        return
    
    # Process data
    print("Processing laboratory observations...")
    observations = process_loinc_data(loinc_data)
    print(f"Generated {len(observations)} laboratory observations")
    
    # Create output structure
    output_data = {
        'metadata': {
            'source': 'Official LOINC Database',
            'version': '2.74',
            'generated_date': '2024-12-30',
            'total_observations': len(observations),
            'description': 'Common laboratory observations extracted from official LOINC database'
        },
        'observations': observations
    }
    
    # Save to JSON file
    output_file = 'loinc.json'
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(output_data, f, indent=2, ensure_ascii=False)
        print(f"Successfully saved LOINC data to {output_file}")
        
        # Print summary statistics
        print("\nSummary Statistics:")
        print(f"- Total observations: {len(observations)}")
        
        # Count by class type
        class_counts = {}
        for obs in observations:
            class_type = obs.get('class_type', 'Unknown')
            class_counts[class_type] = class_counts.get(class_type, 0) + 1
        
        print("- Observations by class type:")
        for class_type, count in sorted(class_counts.items()):
            print(f"  - {class_type}: {count}")
        
        # Count by units
        unit_counts = {}
        for obs in observations:
            unit = obs.get('unit', 'Unknown')
            unit_counts[unit] = unit_counts.get(unit, 0) + 1
        
        print("- Observations by unit:")
        for unit, count in sorted(unit_counts.items()):
            print(f"  - {unit}: {count}")
        
        print(f"\nTop 10 most common tests:")
        for i, obs in enumerate(observations[:10]):
            print(f"  {i+1}. {obs['text']} ({obs['code']}) - {obs['unit']}")
            
    except Exception as e:
        print(f"Error saving JSON file: {e}")

if __name__ == "__main__":
    main()
