import json
import pytest
from patient_management.app import app

@pytest.fixture
def test_client():
    return app.test_client()

def test_get_patients(test_client):
    response = test_client.get('/patients')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert isinstance(data, list)

def test_get_patient(test_client):
    response = test_client.get('/patients/6a7b0bb5-bb18-4e51-b530-0e118e6936a1')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['patient_id'] == '6a7b0bb5-bb18-4e51-b530-0e118e6936a1'

def test_create_patient(test_client):
    new_patient_data = {
        "person_id": "123e4567-e89b-12d3-a456-426614174000",
        "medical_condition_id": "9f9b0fd9-60c3-4d1b-91d7-931dc243678e",
        "first_contact_date": "2024-05-01T09:00:00.000Z",
        "initial_consult_date": "2024-05-10T10:30:00.000Z",
        "trial_id": "TRIAL003",
        "eligible": "Yes",
        "ineligible_reason": "",
        "physician_id": "a1b2c3d4-e5f6-g7h8-i9j0-k1l2m3n4o5p6"
    }
    response = test_client.post('/patients', json=new_patient_data)
    assert response.status_code == 201
    data = json.loads(response.data)
    assert data['person_id'] == new_patient_data["person_id"]

def test_update_patient(test_client):
    updated_data = {
        "trial_id": "TRIAL004",
        "eligible": "No",
        "ineligible_reason": "Not eligible"
    }
    response = test_client.put('/patients/6a7b0bb5-bb18-4e51-b530-0e118e6936a1', json=updated_data)
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['trial_id'] == 'TRIAL004'
    assert data['eligible'] == 'No'
    assert data['ineligible_reason'] == 'Not eligible'

def test_delete_patient(test_client):
    response = test_client.delete('/patients/6a7b0bb5-bb18-4e51-b530-0e118e6936a1')
    assert response.status_code == 204



curl -X GET https://j53d44ee5e.execute-api.eu-west-3.amazonaws.com/Prod/patients


curl -X GET https://j53d44ee5e.execute-api.eu-west-3.amazonaws.com/Prod/patients/{6a7b0bb5-bb18-4e51-b530-0e118e6936a1}

curl -X POST -H "Content-Type: application/json" -d '{"person_id": "...", "medical_condition_id": "...", "first_contact_date": "...", "initial_consult_date": "...", "trial_id": "...", "eligible": "...", "ineligible_reason": "...", "physician_id": "..."}' https://j53d44ee5e.execute-api.eu-west-3.amazonaws.com/Prod/patients

curl -X PUT -H "Content-Type: application/json" -d '{"trial_id": "TRIAL002"}' https://j53d44ee5e.execute-api.eu-west-3.amazonaws.com/Prod/patients/{6a7b0bb5-bb18-4e51-b530-0e118e6936a1}

curl -X DELETE https://j53d44ee5e.execute-api.eu-west-3.amazonaws.com/Prod/patients/{6a7b0bb5-bb18-4e51-b530-0e118e6936a1}
