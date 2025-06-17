from patient import create_patient_resource
from base import send_resource_to_hapi_fhir, get_resource_from_hapi_fhir
from fhir.resources.encounter import Encounter

# Función para buscar un paciente por su identificador (documento)
def search_patient_by_document(doc_id):
    return get_resource_from_hapi_fhir("Patient", identifier=f"http://example.com/document|{doc_id}")

# Función para crear un recurso Encounter
def create_encounter_resource(patient_id):
    # Crear el recurso Encounter con los campos requeridos
    encounter = Encounter(
        status="finished",  # Estado del encuentro: finalizado
        class_fhir={"code": "AMB"},  # Tipo de encuentro: ambulatorio
        subject={"reference": f"Patient/{patient_id}"},  # Relación con el paciente
        period={"start": "2025-06-16", "end": "2025-06-16"}  # Período del encuentro
    )
    # Enviar el recurso al servidor HAPI FHIR y obtener su ID
    encounter_id = send_resource_to_hapi_fhir(encounter, "Encounter")
    return encounter_id

if __name__ == "__main__":
    # Crear un recurso Patient con datos de ejemplo
    patient = create_patient_resource(
        family_name="Doe",
        given_name="John",
        birth_date="1990-01-01",
        gender="male",
        phone=None,
        identifier="12345678"
    )
    # Enviar el recurso Patient al servidor y obtener su ID
    patient_id = send_resource_to_hapi_fhir(patient, "Patient")
    print(f"Recurso Patient creado exitosamente con ID: {patient_id}")

    # Leer el recurso Patient creado usando su ID
    retrieved_patient = get_resource_from_hapi_fhir("Patient", id=patient_id)
    print("Recurso Patient leído:", retrieved_patient)

    # Buscar el paciente por su documento
    found_patient = search_patient_by_document("12345678")
    print("Paciente encontrado por documento:", found_patient)

    # Crear el recurso Encounter vinculado al paciente
    encounter_id = create_encounter_resource(patient_id)
    print(f"Encounter creado con ID: {encounter_id}")