"""
Flask web application for configuring and executing FHIR data generation.
"""
import os
import json
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from typing import Optional, Dict, Any, List

from common import FHIR_HOST, FHIR_PATH, FHIR_PORT, FHIRServerConfig
from main import main as generate_fhir_data
from lib.data.icd import CONDITIONS_ICD10
from lib.data.medications import MEDICATIONS

app = Flask(__name__)
app.secret_key = os.getenv('FLASK_SECRET_KEY', 'dev-secret-key-change-in-production')


def load_available_conditions() -> List[Dict[str, str]]:
    """Load available conditions from ICD-10 data."""
    return CONDITIONS_ICD10


def load_available_medications() -> List[Dict[str, Any]]:
    """Load available medications."""
    return MEDICATIONS


@app.route('/')
def index():
    """Home page with overview and quick actions."""
    return render_template('index.html')


@app.route('/configure', methods=['GET', 'POST'])
def configure():
    """Configure patient-specific data generation."""
    if request.method == 'POST':
        # Collect form data
        config = {
            'description': request.form.get('description', 'Custom patient configuration'),
            'base_counts': {
                'clinics': int(request.form.get('clinics', 3)),
                'practitioners': int(request.form.get('practitioners', 10)),
                'patients': int(request.form.get('patients', 1))
            },
            'per_patient': {},
            'patient_configs': []
        }
        
        # Get number of patients to configure
        num_patients = int(request.form.get('num_patients', 1))
        
        # Collect patient-specific configurations
        for i in range(num_patients):
            patient_config = {
                'patient_index': i,
                'first_name': request.form.get(f'patient_{i}_first_name', ''),
                'last_name': request.form.get(f'patient_{i}_last_name', ''),
                'gender': request.form.get(f'patient_{i}_gender', 'unknown'),
                'birth_date': request.form.get(f'patient_{i}_birth_date', ''),
                'conditions': [],
                'medications': [],
                'allergies': [],
                'appointments': int(request.form.get(f'patient_{i}_appointments', 1)),
                'encounters': int(request.form.get(f'patient_{i}_encounters', 1)),
                'observations': int(request.form.get(f'patient_{i}_observations', 2)),
                'procedures': int(request.form.get(f'patient_{i}_procedures', 1))
            }
            
            # Collect conditions
            condition_count = int(request.form.get(f'patient_{i}_condition_count', 0))
            for j in range(condition_count):
                condition_code = request.form.get(f'patient_{i}_condition_{j}_code', '')
                if condition_code:
                    patient_config['conditions'].append({
                        'code': condition_code,
                        'display': request.form.get(f'patient_{i}_condition_{j}_display', '')
                    })
            
            # Collect medications
            medication_count = int(request.form.get(f'patient_{i}_medication_count', 0))
            for j in range(medication_count):
                medication_name = request.form.get(f'patient_{i}_medication_{j}_name', '')
                if medication_name:
                    patient_config['medications'].append({
                        'name': medication_name
                    })
            
            # Collect allergies
            allergy_count = int(request.form.get(f'patient_{i}_allergy_count', 0))
            for j in range(allergy_count):
                allergy_substance = request.form.get(f'patient_{i}_allergy_{j}_substance', '')
                if allergy_substance:
                    patient_config['allergies'].append({
                        'substance': allergy_substance
                    })
            
            config['patient_configs'].append(patient_config)
        
        # Set per_patient defaults (can be overridden per patient)
        config['per_patient'] = {
            'conditions': {'min': 0, 'max': 0},  # Will be set per patient
            'medication_requests': {'min': 0, 'max': 0},  # Will be set per patient
            'allergy_intolerances': {'min': 0, 'max': 0},  # Will be set per patient
            'appointments': {'min': 1, 'max': 5},
            'encounters': {'min': 1, 'max': 4, 'document_reference_probability': 0.8},
            'observations': {'min': 2, 'max': 6},
            'procedures': {'min': 1, 'max': 3},
            'diagnostic_reports': {'min': 1, 'max': 2},
            'service_requests': {'min': 1, 'max': 3},
            'clinical_impressions': {'min': 1, 'max': 2},
            'family_member_histories': {'min': 2, 'max': 4},
            'immunizations': {'min': 1, 'max': 3},
            'medication_administrations': {'min': 2, 'max': 5},
            'care_plans': {'min': 1, 'max': 3},
            'coverages': {'min': 1, 'max': 2}
        }
        
        # Save configuration to session or file
        config_file = 'config_custom.json'
        with open(config_file, 'w') as f:
            json.dump(config, f, indent=2)
        
        flash(f'Configuration saved! Ready to generate data for {num_patients} patient(s).', 'success')
        return redirect(url_for('execute', config_file=config_file))
    
    # GET request - show configuration form
    conditions = load_available_conditions()
    medications = load_available_medications()
    return render_template('configure.html', conditions=conditions, medications=medications)


@app.route('/execute')
def execute():
    """Execute data generation with the configured parameters."""
    config_file = request.args.get('config_file', 'config_custom.json')
    output_file = request.args.get('output_file', 'fhir_dummy_data.json')
    send_to_server = request.args.get('send_to_server', 'false').lower() == 'true'
    
    try:
        # Load configuration
        if not os.path.exists(config_file):
            flash(f'Configuration file not found: {config_file}', 'error')
            return redirect(url_for('configure'))
        
        # Determine if we should send to server
        fhir_server = None
        if send_to_server:
            fhir_server = FHIRServerConfig(host=FHIR_HOST, port=FHIR_PORT, path=FHIR_PATH)
        
        # Execute generation
        generate_fhir_data(
            output_filename=output_file,
            fhir_server=fhir_server,
            config_file=config_file
        )
        
        flash('Data generation completed successfully!', 'success')
        return render_template('execute.html', 
                             config_file=config_file,
                             output_file=output_file,
                             sent_to_server=send_to_server)
    
    except Exception as e:
        flash(f'Error during data generation: {str(e)}', 'error')
        return redirect(url_for('configure'))


@app.route('/api/conditions')
def api_conditions():
    """API endpoint to get available conditions."""
    return jsonify(load_available_conditions())


@app.route('/api/medications')
def api_medications():
    """API endpoint to get available medications."""
    return jsonify(load_available_medications())


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

