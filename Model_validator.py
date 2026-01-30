from pydantic import BaseModel, EmailStr, AnyUrl, Field, model_validator
from typing import List, Dict, Optional, Annotated

class patient(BaseModel):

    name: str
    email: EmailStr
    linkdin_url: AnyUrl
    age: int
    weight: float
    married:bool
    allergies: Optional[List[str]] = None
    contact_details: Dict[str, str]

    @model_validator(mode="after")
    def val_emg_contact(self):
        if self.age > 60 and "emergency" not in self.contact_details:
            raise ValueError("Emergency contact is required for patients above 60 years")
        return self


def insert_patient_data(patient: patient):
    print(patient.name)
    print(patient.age)
    print(patient.email)
    print(patient.contact_details)
    print("Patient data inserted successfully")

patient_info = {
    "name": "krish",
    "email": "krish@konda.com",
    "linkdin_url": "https://www.linkedin.com/in/krish-konda-123456789/",
    "age": 65,
    "weight": 70.5,
    "married": True,
    # "allergies": ["pollen", "dust"],
    "contact_details": {
        "email": "krish@konda.com",
        "phone": "7984992893",
        "emergency" : "939393939"
    }
}

patient_obj = patient(**patient_info)

insert_patient_data(patient_obj)