import requests
from patient import create_patient_resource

# Enviar el recurso FHIR al servidor HAPI FHIR
def send_resource_to_hapi_fhir(resource, resource_type):
    url = f"http://hapi.fhir.org/baseR4/{resource_type}"
    headers = {"Content-Type": "application/fhir+json"}
    resource_json = resource.json()

    response = requests.post(url, headers=headers, data=resource_json)

    if response.status_code == 201:
        print("Recurso creado exitosamente")
        # Devolver el ID del recurso creado
        return response.json()['id']
    else:
        print(f"Error al crear el recurso: {response.status_code}")
        print(response.json())
        return None

# Buscar el recurso por ID o parámetros de búsqueda
def get_resource_from_hapi_fhir(resource_type, **kwargs):
    base_url = f"http://hapi.fhir.org/baseR4/{resource_type}"
    params = {}

    # Si se pasa un id, construir la URL directa
    if 'id' in kwargs or '_id' in kwargs:
        resource_id = kwargs.get('id') or kwargs.get('_id')
        url = f"{base_url}/{resource_id}"
    else:
        # Si hay otros parámetros (como identifier), usar búsqueda
        if 'identifier' in kwargs:
            params['identifier'] = kwargs['identifier']
        url = base_url

    headers = {"Accept": "application/fhir+json"}
    response = requests.get(url, headers=headers, params=params if params else None)

    if response.status_code == 200:
        resource = response.json()
        print(resource)
        return resource
    else:
        print(f"Error al obtener el recurso: {response.status_code}")
        print(response.json())
        return None