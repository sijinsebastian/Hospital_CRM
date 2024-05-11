import os
import uuid
import json

from flask import request, jsonify
from flask_lambda import FlaskLambda


app = FlaskLambda(__name__)


# Load sample data from JSON file
dirname = os.path.dirname(__file__)
sample_data_file = os.path.join(dirname, './data/sample_data.json')
with open(sample_data_file) as f:
    sample_data = json.load(f)

patients = sample_data['patients']

@app.route('/patients', methods=['GET'])
def get_patients():
    return jsonify(patients)

@app.route('/patients/<uuid:id>', methods=['GET'])
def get_patient(id):
    patient = next((patient for patient in patients if patient['patient_id'] == str(id)), None)
    if patient:
        return jsonify(patient)
    else:
        return jsonify({'message': 'Patient not found'}), 404

@app.route('/patients', methods=['POST'])
def create_patient():
    patient_data = request.get_json()
    new_patient_id = str(uuid.uuid4())
    patient_data.update(patient_id=new_patient_id)
    # new_patient = {"patient_id": new_patient_id, "person_id": data["person_id"], "medical_condition_id": data["medical_condition_id"],
    #                "first_contact_date": data["first_contact_date"], "initial_consult_date": data["initial_consult_date"],
    #                "trial_id": data["trial_id"], "eligible": data["eligible"], "ineligible_reason": data["ineligible_reason"],
    #                "physician_id": data["physician_id"]}
    patients.append(patient_data)
    return jsonify(patient_data), 201


@app.route('/patients/<uuid:id>', methods=['PUT'])
def update_patient(id):
    data = request.get_json()
    patient = next((patient for patient in patients if patient['patient_id'] == str(id)), None)
    if patient:
        patient.update(data)
        return jsonify(patient)
    else:
        return jsonify({'message': 'Patient not found'}), 404

@app.route('/patients/<uuid:id>', methods=['DELETE'])
def delete_patient(id):
    global patients
    try:
        patients = [patient for patient in patients if patient['patient_id'] != id]
        return {}, 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)