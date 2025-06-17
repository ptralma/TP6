from patient import create_patient_resource
from base import send_resource_to_hapi_fhir, get_resource_from_hapi_fhir
from fhir.resources.encounter import Encounter

def search_patient_by_document(doc_id):
    return get_resource_from_hapi_fhir("Patient", identifier=f"http://example.com/document|{doc_id}")

def create_encounter_resource(patient_id):
    encounter = Encounter(
        status="finished",
        class_fhir={"code": "AMB"},
        subject={"reference": f"Patient/{patient_id}"},
        period={"start": "2025-06-16", "end": "2025-06-16"}
    )
    encounter_id = send_resource_to_hapi_fhir(encounter, "Encounter")
    return encounter_id

if __name__ == "__main__":
    # Crear el recurso de paciente
    patient = create_patient_resource(family_name="Doe", given_name="John", birth_date="1990-01-01", gender="male", phone=None, identifier="12345678")
    patient_id = send_resource_to_hapi_fhir(patient, "Patient")
    print(f"Recurso creado exitosamente")

    # Leer el recurso creado usando el id
    retrieved_patient = get_resource_from_hapi_fhir("Patient", id=patient_id)
    print("Recurso leído:", retrieved_patient)

    # Buscar el paciente por documento
    found_patient = search_patient_by_document("12345678")
    print("Paciente encontrado por documento:", found_patient)

    # Crear el recurso Encounter
    encounter_id = create_encounter_resource(patient_id)
    print(f"Encounter creado con ID: {encounter_id}")