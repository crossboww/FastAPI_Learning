from pydantic import BaseModel

class patient(BaseModel):

    name: str
    age: int

def insert_patient_data(patient: patient):
    print(patient.name)
    print(patient.age)
    print("Patient data inserted successfully")

def update_patient_data(patient: patient):
    print(patient.name)
    print(patient.age)
    print("Patient data updated successfully")

patient_info = {
    "name": "krish",
    "age": 22
}

patient_obj = patient(**patient_info)

insert_patient_data(patient_obj)