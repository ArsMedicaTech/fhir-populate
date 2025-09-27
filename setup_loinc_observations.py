"""
Setup LOINC Observations

This script runs the complete process to generate LOINC observations:
1. Extract data from official LOINC CSV
2. Generate loinc.json file
3. Update observations.py with real LOINC data

Usage:
    python setup_loinc_observations.py
"""

import subprocess
import sys
import os

def run_script(script_name: str, description: str) -> bool:
    """
    Run a Python script and return success status.
    
    :param script_name: Name of the script to run
    :param description: Description of what the script does
        
    :return: True if successful, False otherwise
    """
    print(f"\n{'='*60}")
    print(f"Running: {description}")
    print(f"{'='*60}")
    
    try:
        result = subprocess.run([sys.executable, script_name], 
                              capture_output=True, text=True, check=True)
        print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error running {script_name}:")
        print(f"Return code: {e.returncode}")
        print(f"STDOUT: {e.stdout}")
        print(f"STDERR: {e.stderr}")
        return False
    except FileNotFoundError:
        print(f"Error: {script_name} not found")
        return False

def main() -> None:
    """Main function to run the complete LOINC setup process."""
    print("LOINC Observations Setup")
    print("=" * 60)
    print("This script will:")
    print("1. Extract data from official LOINC CSV")
    print("2. Generate loinc.json file")
    print("3. Update observations.py with real LOINC data")
    print()
    
    # Check if LOINC CSV exists
    csv_path = 'loinc/LoincTable/Loinc.csv'
    if not os.path.exists(csv_path):
        print(f"Error: LOINC CSV file not found at {csv_path}")
        print("Please ensure you have downloaded the official LOINC database")
        print("and placed it in the correct location.")
        return
    
    print(f"Found LOINC CSV at: {csv_path}")
    
    # Step 1: Generate LOINC data
    if not run_script('generate_loinc_data.py', 'Generating LOINC data from CSV'):
        print("Failed to generate LOINC data. Exiting.")
        return
    
    # Step 2: Update observations.py
    if not run_script('update_observations_from_loinc.py', 'Updating observations.py with LOINC data'):
        print("Failed to update observations.py. Exiting.")
        return
    
    print(f"\n{'='*60}")
    print("LOINC Observations Setup Complete!")
    print(f"{'='*60}")
    print("The observations.py file has been updated with real LOINC data.")
    print("You can now run the main FHIR data generator to use the updated observations.")
    print()
    print("Next steps:")
    print("1. Run: python main.py")
    print("2. The generated FHIR data will now use official LOINC codes and names")

if __name__ == "__main__":
    main()
