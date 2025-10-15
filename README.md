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

## Environment Variables (for FHIR server)

Set the following environment variables in a `.env` file or export them in your shell:
- `FHIR_HOST`: The hostname of the FHIR server (e.g., `localhost`).
- `FHIR_PORT`: The port number of the FHIR server (e.g., `8080`).
- `FHIR_PATH`: The base path of the FHIR server (e.g., `fhir`).
