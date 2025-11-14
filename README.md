# fhir-populate 

## About

This is a collection of scripts to populate a FHIR server with sample data for testing and development purposes. It includes functionality to create patients, practitioners, and other FHIR resources.

You have the option of saving to a JSON file or to `POST` directly to an FHIR-compatible server.

## Usage

1. Create a virtual environment and activate it:

```bash
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```

2. Install the required packages:

```bash
pip install -r requirements.txt
```

3. Run the script:

```bash
python main.py
```

## Configuration Files

The script uses JSON configuration files to control how many entities are generated. This allows you to easily switch between high volume (for production/testing) and low volume (for quick testing/debugging) configurations.

### Available Configuration Files

- **`config_high_volume.json`**: Default configuration with realistic data volumes (25 patients, 10 practitioners, etc.)
- **`config_low_volume.json`**: Minimal configuration for quick testing (3 patients, 2 practitioners, etc.)

### Using Configuration Files

You can specify a configuration file in three ways:

1. **Command line argument**:
   ```bash
   python main.py config_low_volume.json
   ```

2. **Environment variable**:
   ```bash
   export FHIR_CONFIG=config_low_volume.json
   python main.py
   ```

3. **Default**: If no config is specified, it defaults to `config_high_volume.json`

### Configuration File Structure

The configuration file has two main sections:

- **`base_counts`**: Defines the number of base entities (clinics, practitioners, patients)
- **`per_patient`**: Defines ranges (min/max) for how many of each resource type to generate per patient

Example:
```json
{
  "base_counts": {
    "clinics": 3,
    "practitioners": 10,
    "patients": 25
  },
  "per_patient": {
    "conditions": {"min": 1, "max": 3},
    "appointments": {"min": 1, "max": 5},
    "encounters": {
      "min": 1,
      "max": 4,
      "document_reference_probability": 0.8
    }
  }
}
```

### Creating Custom Configuration Files

You can create your own configuration files by copying one of the existing files and modifying the values. All `per_patient` entries support `min` and `max` values, and `encounters` also supports `document_reference_probability` (0.0 to 1.0) to control how often clinical notes are generated.

## Environment Variables (for FHIR server)

Set the following environment variables in a `.env` file or export them in your shell:
- `FHIR_HOST`: The hostname of the FHIR server (e.g., `localhost`).
- `FHIR_PORT`: The port number of the FHIR server (e.g., `8080`).
- `FHIR_PATH`: The base path of the FHIR server (e.g., `fhir`).
