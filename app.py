"""
Flask web application for configuring and executing FHIR data generation.
"""
import os
import json
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from typing import Optional, Dict, Any, List

from common import FHIR_HOST, FHIR_PATH, FHIR_PORT, FHIRServerConfig, get_fhir_version
from main import main as generate_fhir_data
from lib.data.icd import CONDITIONS_ICD10
from lib.data.medications import MEDICATIONS
from lib.crud import Request

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


@app.route('/server-config', methods=['GET', 'POST'])
def server_config():
    """Configure FHIR server settings."""
    if request.method == 'POST':
        # Save server configuration
        server_config_data = {
            'host': request.form.get('host', 'localhost'),
            'port': int(request.form.get('port', 8080)),
            'path': request.form.get('path', '/fhir'),
            'fhir_version': request.form.get('fhir_version', 'R4')
        }
        
        # Save to file
        config_file = 'server_config.json'
        with open(config_file, 'w') as f:
            json.dump(server_config_data, f, indent=2)
        
        flash('Server configuration saved!', 'success')
        return redirect(url_for('server_config'))
    
    # GET request - load existing config or use defaults
    config_file = 'server_config.json'
    if os.path.exists(config_file):
        with open(config_file, 'r') as f:
            server_config_data = json.load(f)
    else:
        server_config_data = {
            'host': FHIR_HOST,
            'port': FHIR_PORT if FHIR_PORT else 8080,
            'path': FHIR_PATH,
            'fhir_version': get_fhir_version()
        }
    
    return render_template('server_config.html', config=server_config_data)


@app.route('/api/check-fhir-version', methods=['POST'])
def check_fhir_version():
    """Check FHIR version from the configured server."""
    try:
        import requests
        data = request.get_json()
        host = data.get('host', 'localhost')
        port = int(data.get('port', 8080))
        path = data.get('path', '/fhir')
        
        # Construct the metadata URL
        port_str = f":{port}" if port else ""
        metadata_url = f"http://{host}{port_str}{path}/metadata"
        
        try:
            # Try to get capability statement from metadata endpoint
            headers = {
                "Accept": "application/fhir+json",
                "User-Agent": "FHIR-Data-Generator/1.0"
            }
            response = requests.get(metadata_url, headers=headers, timeout=5)
            response.raise_for_status()
            
            capability = response.json()
            version = capability.get('fhirVersion', 'Unknown')
            
            # Map version to R4/R5
            version_mapping = {
                '4.0': 'R4',
                '4.0.1': 'R4',
                '4.0.2': 'R4',
                '4.3.0': 'R4',
                '5.0': 'R5',
                '5.0.0': 'R5'
            }
            
            # Try to match version
            mapped_version = 'Unknown'
            for v, r in version_mapping.items():
                if version.startswith(v) or version == v:
                    mapped_version = r
                    break
            
            return jsonify({
                'success': True,
                'version': version,
                'mapped_version': mapped_version,
                'message': f'FHIR version detected: {version}' + (f' (maps to {mapped_version})' if mapped_version != 'Unknown' else '')
            })
        except requests.exceptions.RequestException as e:
            return jsonify({
                'success': False,
                'message': f'Could not connect to server or retrieve metadata: {str(e)}'
            })
        except Exception as e:
            return jsonify({
                'success': False,
                'message': f'Could not determine FHIR version: {str(e)}'
            })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error checking FHIR version: {str(e)}'
        }), 500


@app.route('/execute', methods=['GET', 'POST'])
def execute():
    """Execute data generation with the configured parameters."""
    if request.method == 'POST':
        # Handle execution request
        config_file = request.form.get('config_file', 'config_custom.json')
        output_file = request.form.get('output_file', 'fhir_dummy_data.json')
        send_to_server = request.form.get('send_to_server', 'false').lower() == 'true'
        
        # Load server configuration if sending to server
        fhir_server = None
        if send_to_server:
            server_config_file = 'server_config.json'
            if os.path.exists(server_config_file):
                with open(server_config_file, 'r') as f:
                    server_config_data = json.load(f)
                fhir_server = FHIRServerConfig(
                    host=server_config_data.get('host', FHIR_HOST),
                    port=server_config_data.get('port', FHIR_PORT if FHIR_PORT else 8080),
                    path=server_config_data.get('path', FHIR_PATH)
                )
                # Set FHIR version environment variable
                fhir_version = server_config_data.get('fhir_version', 'R4')
                os.environ['FHIR_VERSION'] = fhir_version
            else:
                flash('Server configuration not found. Please configure server settings first.', 'error')
                return redirect(url_for('server_config'))
        
        try:
            # Load configuration
            if not os.path.exists(config_file):
                flash(f'Configuration file not found: {config_file}', 'error')
                return redirect(url_for('configure'))
            
            # Execute generation
            generate_fhir_data(
                output_filename=output_file,
                fhir_server=fhir_server,
                config_file=config_file
            )
            
            flash('Data generation completed successfully!', 'success')
        
            # Load server config for display
            server_config_file = 'server_config.json'
            if os.path.exists(server_config_file):
                with open(server_config_file, 'r') as f:
                    server_config_data = json.load(f)
            else:
                server_config_data = {
                    'host': FHIR_HOST,
                    'port': FHIR_PORT if FHIR_PORT else 8080,
                    'path': FHIR_PATH,
                    'fhir_version': get_fhir_version()
                }
            
            return render_template('execute.html', 
                                config_file=config_file,
                                output_file=output_file,
                                sent_to_server=send_to_server,
                                server_config=server_config_data)
        
        except Exception as e:
            import traceback
            error_details = traceback.format_exc()
            print(f"Error during data generation: {error_details}")  # Print full traceback to console
            flash(f'Error during data generation: {str(e)}', 'error')
            return redirect(url_for('execute', config_file=config_file))
    
    # GET request - show execution page
    config_file = request.args.get('config_file', 'config_custom.json')
    
    # Load server configuration
    server_config_file = 'server_config.json'
    if os.path.exists(server_config_file):
        with open(server_config_file, 'r') as f:
            server_config_data = json.load(f)
    else:
        server_config_data = {
            'host': FHIR_HOST,
            'port': FHIR_PORT if FHIR_PORT else 8080,
            'path': FHIR_PATH,
            'fhir_version': get_fhir_version()
        }
    
    return render_template('execute.html', 
                         config_file=config_file,
                         server_config=server_config_data)


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

