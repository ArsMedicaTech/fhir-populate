# LOINC Data Setup

This directory contains scripts to generate realistic FHIR observations using the official LOINC database.

## Overview

The LOINC (Logical Observation Identifiers Names and Codes) database is the global standard for identifying laboratory and clinical observations. This setup process extracts data from the official LOINC CSV file and generates a structured JSON file with common laboratory observations, including proper LOINC codes, names, units, and clinical reference ranges.

## Files

- `generate_loinc_data.py` - Extracts data from official LOINC CSV and generates `loinc.json`
- `update_observations_from_loinc.py` - Updates `lib/data/observations.py` with real LOINC data
- `setup_loinc_observations.py` - Runs the complete setup process
- `requirements_loinc.txt` - Additional Python dependencies for LOINC processing

## Prerequisites

1. **Official LOINC Database**: Download the official LOINC database from [loinc.org](https://loinc.org)
   - Place the `Loinc.csv` file in `loinc/LoincTable/Loinc.csv`
   - The file should be the complete LOINC table (typically ~100k+ rows)

2. **Python Dependencies**: Install additional requirements
   ```bash
   pip install -r requirements_loinc.txt
   ```

## Quick Start

Run the complete setup process:

```bash
python setup_loinc_observations.py
```

This will:
1. Extract laboratory observations from the LOINC CSV
2. Generate a `loinc.json` file with structured data
3. Update `lib/data/observations.py` with real LOINC codes and names

## Manual Process

If you prefer to run the steps individually:

### Step 1: Generate LOINC Data
```bash
python generate_loinc_data.py
```

This creates `loinc.json` with:
- Official LOINC codes and names
- Proper units and unit systems
- Clinical reference ranges
- Interpretation thresholds (Low/Normal/High)

### Step 2: Update Observations
```bash
python update_observations_from_loinc.py
```

This updates `lib/data/observations.py` with the real LOINC data.

## What Gets Generated

The process extracts the most common laboratory tests from LOINC, including:

- **Basic Metabolic Panel**: Glucose, Sodium, Potassium, Chloride, CO2, BUN, Creatinine, Calcium
- **Lipid Panel**: Total Cholesterol, HDL, LDL, Triglycerides
- **Complete Blood Count**: WBC, RBC, Hemoglobin, Hematocrit, Platelets
- **Liver Function**: ALT, AST, Alkaline Phosphatase, Bilirubin, Albumin
- **Thyroid Function**: TSH, T4, T3
- **Cardiac Markers**: BNP, NT-proBNP
- **Coagulation**: PT, PTT, INR
- **Vitamins**: B12, Folate, Vitamin D
- **Inflammatory Markers**: CRP, ESR
- **Tumor Markers**: PSA
- **Diabetes**: Hemoglobin A1c

## Data Quality

The generated observations include:

- **Official LOINC Codes**: Real codes from the official database
- **Proper Names**: Long Common Names and Short Names from LOINC
- **Accurate Units**: Standardized units with proper UCUM codes
- **Clinical Ranges**: Realistic normal ranges and interpretation thresholds
- **Metadata**: Component, property, time aspect, system, scale type, method type

## Output

After running the setup:

1. **`loinc.json`**: Structured JSON file with all extracted LOINC data
2. **`lib/data/observations.py`**: Updated Python file with real LOINC observations
3. **FHIR Observations**: Generated FHIR observations will now use official LOINC codes

## Verification

To verify the setup worked correctly:

```bash
python main.py
```

The generated FHIR observations should now include:
- Official LOINC codes (e.g., "33747-0" instead of placeholder codes)
- Real laboratory test names (e.g., "Glucose [Mass/volume] in Blood" instead of "Glucose")
- Proper units and reference ranges
- Clinically accurate interpretation values

## Troubleshooting

### Common Issues

1. **LOINC CSV not found**
   - Ensure the file is at `loinc/LoincTable/Loinc.csv`
   - Check the file name and path

2. **Import errors**
   - Install required dependencies: `pip install -r requirements_loinc.txt`

3. **Empty observations**
   - Check that the LOINC CSV has the expected column names
   - Verify the file is not corrupted

### File Structure

```
fhir-populate/
├── loinc/
│   └── LoincTable/
│       └── Loinc.csv          # Official LOINC database
├── lib/
│   └── data/
│       └── observations.py     # Generated observations
├── generate_loinc_data.py      # LOINC extraction script
├── update_observations_from_loinc.py  # Update script
├── setup_loinc_observations.py # Complete setup
└── loinc.json                  # Generated LOINC data
```

## License

The LOINC database is available under the [LOINC Terms of Use](http://loinc.org/terms-of-use), which permits both commercial and non-commercial usage with proper attribution.
