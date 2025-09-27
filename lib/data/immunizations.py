"""
Common immunization data for FHIR Immunization resources.
Includes vaccine codes, manufacturers, and administration details.
"""

# Immunization statuses
IMMUNIZATION_STATUSES = [
    "completed",
    "entered-in-error",
    "not-done"
]

# Common vaccines (CVX codes)
# TODO: VERIFY THESE...
VACCINES = [
    {
        "code": "175",
        "display": "Rabies - IM Diploid cell culture",
        "text": "Rabies Vaccine",
        "system": "http://hl7.org/fhir/sid/cvx"
    },
    {
        "code": "20",
        "display": "DTaP",
        "text": "Diphtheria, Tetanus, Pertussis",
        "system": "http://hl7.org/fhir/sid/cvx"
    },
    {
        "code": "110",
        "display": "Hepatitis B - adult",
        "text": "Hepatitis B Vaccine",
        "system": "http://hl7.org/fhir/sid/cvx"
    },
    {
        "code": "08",
        "display": "Hepatitis B - pediatric/adolescent",
        "text": "Hepatitis B Vaccine (Pediatric)",
        "system": "http://hl7.org/fhir/sid/cvx"
    },
    {
        "code": "33",
        "display": "Pneumococcal conjugate PCV 13",
        "text": "Pneumococcal Conjugate Vaccine",
        "system": "http://hl7.org/fhir/sid/cvx"
    },
    {
        "code": "111",
        "display": "Influenza, seasonal, injectable",
        "text": "Seasonal Influenza Vaccine",
        "system": "http://hl7.org/fhir/sid/cvx"
    },
    {
        "code": "140",
        "display": "Influenza, seasonal, intranasal",
        "text": "Seasonal Influenza Vaccine (Nasal)",
        "system": "http://hl7.org/fhir/sid/cvx"
    },
    {
        "code": "21",
        "display": "Varicella",
        "text": "Chickenpox Vaccine",
        "system": "http://hl7.org/fhir/sid/cvx"
    },
    {
        "code": "07",
        "display": "Measles, mumps, rubella",
        "text": "MMR Vaccine",
        "system": "http://hl7.org/fhir/sid/cvx"
    },
    {
        "code": "09",
        "display": "Haemophilus influenzae type b",
        "text": "Hib Vaccine",
        "system": "http://hl7.org/fhir/sid/cvx"
    },
    {
        "code": "10",
        "display": "Poliovirus, inactivated",
        "text": "Polio Vaccine (IPV)",
        "system": "http://hl7.org/fhir/sid/cvx"
    },
    {
        "code": "16",
        "display": "Pneumococcal polysaccharide PPV23",
        "text": "Pneumococcal Polysaccharide Vaccine",
        "system": "http://hl7.org/fhir/sid/cvx"
    },
    {
        "code": "43",
        "display": "Hepatitis A - adult",
        "text": "Hepatitis A Vaccine",
        "system": "http://hl7.org/fhir/sid/cvx"
    },
    {
        "code": "52",
        "display": "Hepatitis A - pediatric/adolescent",
        "text": "Hepatitis A Vaccine (Pediatric)",
        "system": "http://hl7.org/fhir/sid/cvx"
    },
    {
        "code": "83",
        "display": "Hepatitis A and Hepatitis B",
        "text": "Hepatitis A and B Combined Vaccine",
        "system": "http://hl7.org/fhir/sid/cvx"
    },
    {
        "code": "115",
        "display": "Tetanus and diphtheria toxoids (Td)",
        "text": "Td Vaccine",
        "system": "http://hl7.org/fhir/sid/cvx"
    },
    {
        "code": "116",
        "display": "Tetanus, diphtheria, pertussis (Tdap)",
        "text": "Tdap Vaccine",
        "system": "http://hl7.org/fhir/sid/cvx"
    },
    {
        "code": "137",
        "display": "COVID-19, mRNA, LNP-S, PF, 100 mcg/0.5mL dose",
        "text": "COVID-19 mRNA Vaccine",
        "system": "http://hl7.org/fhir/sid/cvx"
    },
    {
        "code": "207",
        "display": "COVID-19, mRNA, LNP-S, PF, 30 mcg/0.3mL dose",
        "text": "COVID-19 mRNA Vaccine (Pediatric)",
        "system": "http://hl7.org/fhir/sid/cvx"
    },
    {
        "code": "208",
        "display": "COVID-19, mRNA, LNP-S, PF, 10 mcg/0.2mL dose",
        "text": "COVID-19 mRNA Vaccine (Infant)",
        "system": "http://hl7.org/fhir/sid/cvx"
    }
]

# Vaccine manufacturers
VACCINE_MANUFACTURERS = [
    {
        "reference": "Organization/pfizer",
        "display": "Pfizer Inc"
    },
    {
        "reference": "Organization/moderna",
        "display": "Moderna Inc"
    },
    {
        "reference": "Organization/johnson-johnson",
        "display": "Johnson & Johnson"
    },
    {
        "reference": "Organization/merck",
        "display": "Merck & Co"
    },
    {
        "reference": "Organization/glaxosmithkline",
        "display": "GlaxoSmithKline"
    },
    {
        "reference": "Organization/sanofi",
        "display": "Sanofi Pasteur"
    },
    {
        "reference": "Organization/novavax",
        "display": "Novavax Inc"
    },
    {
        "reference": "Organization/astrazeneca",
        "display": "AstraZeneca"
    }
]

# Administration sites
ADMINISTRATION_SITES = [
    {
        "code": "LA",
        "display": "left arm",
        "system": "http://terminology.hl7.org/CodeSystem/v3-ActSite"
    },
    {
        "code": "RA",
        "display": "right arm",
        "system": "http://terminology.hl7.org/CodeSystem/v3-ActSite"
    },
    {
        "code": "LDELT",
        "display": "left deltoid",
        "system": "http://terminology.hl7.org/CodeSystem/v3-ActSite"
    },
    {
        "code": "RDELT",
        "display": "right deltoid",
        "system": "http://terminology.hl7.org/CodeSystem/v3-ActSite"
    },
    {
        "code": "LTHIGH",
        "display": "left thigh",
        "system": "http://terminology.hl7.org/CodeSystem/v3-ActSite"
    },
    {
        "code": "RTHIGH",
        "display": "right thigh",
        "system": "http://terminology.hl7.org/CodeSystem/v3-ActSite"
    },
    {
        "code": "BUTT",
        "display": "buttock",
        "system": "http://terminology.hl7.org/CodeSystem/v3-ActSite"
    }
]

# Routes of administration
ROUTES_OF_ADMINISTRATION = [
    {
        "code": "IM",
        "display": "Injection, intramuscular",
        "system": "http://terminology.hl7.org/CodeSystem/v3-RouteOfAdministration"
    },
    {
        "code": "SC",
        "display": "Injection, subcutaneous",
        "system": "http://terminology.hl7.org/CodeSystem/v3-RouteOfAdministration"
    },
    {
        "code": "ID",
        "display": "Injection, intradermal",
        "system": "http://terminology.hl7.org/CodeSystem/v3-RouteOfAdministration"
    },
    {
        "code": "IN",
        "display": "Inhalation, nasal",
        "system": "http://terminology.hl7.org/CodeSystem/v3-RouteOfAdministration"
    },
    {
        "code": "PO",
        "display": "Swallow, oral",
        "system": "http://terminology.hl7.org/CodeSystem/v3-RouteOfAdministration"
    }
]

# Performer functions
PERFORMER_FUNCTIONS = [
    {
        "code": "OP",
        "display": "Ordering Provider",
        "system": "http://terminology.hl7.org/CodeSystem/v2-0443"
    },
    {
        "code": "AP",
        "display": "Administering Provider",
        "system": "http://terminology.hl7.org/CodeSystem/v2-0443"
    },
    {
        "code": "PRF",
        "display": "Performer",
        "system": "http://terminology.hl7.org/CodeSystem/v2-0443"
    }
]

# Common vaccine reactions
VACCINE_REACTIONS = [
    "Mild fever",
    "Redness at injection site",
    "Swelling at injection site",
    "Pain at injection site",
    "Fatigue",
    "Headache",
    "Muscle aches",
    "Nausea",
    "Chills",
    "Mild allergic reaction",
    "Rash",
    "Dizziness",
    "Fainting",
    "Severe allergic reaction",
    "Anaphylaxis"
]

# Common immunization reasons
IMMUNIZATION_REASONS = [
    "Routine immunization",
    "Travel vaccination",
    "Occupational requirement",
    "Outbreak response",
    "Catch-up vaccination",
    "Booster dose",
    "High-risk population",
    "Pregnancy",
    "Immunocompromised",
    "Elderly care",
    "School requirement",
    "Healthcare worker",
    "Military service",
    "International travel",
    "Seasonal vaccination"
]

# Common immunization notes
IMMUNIZATION_NOTES = [
    "Patient tolerated vaccine well",
    "No adverse reactions observed",
    "Patient advised to monitor for side effects",
    "Next dose due in 4 weeks",
    "Series completed",
    "Booster recommended in 1 year",
    "Patient has history of allergies",
    "Administered with other vaccines",
    "Patient was fasting",
    "Temperature checked before administration",
    "Patient provided informed consent",
    "Vaccine stored at proper temperature",
    "Lot number verified",
    "Expiration date checked",
    "Patient education provided"
]

# Dose quantities (varies by vaccine)
DOSE_QUANTITIES = [
    {"value": 0.5, "unit": "mL", "code": "mL"},
    {"value": 1.0, "unit": "mL", "code": "mL"},
    {"value": 2.0, "unit": "mL", "code": "mL"},
    {"value": 0.25, "unit": "mL", "code": "mL"},
    {"value": 0.1, "unit": "mL", "code": "mL"},
    {"value": 5, "unit": "mg", "code": "mg"},
    {"value": 10, "unit": "mg", "code": "mg"},
    {"value": 25, "unit": "mcg", "code": "mcg"},
    {"value": 50, "unit": "mcg", "code": "mcg"},
    {"value": 100, "unit": "mcg", "code": "mcg"}
]
