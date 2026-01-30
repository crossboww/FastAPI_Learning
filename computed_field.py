from pydantic import BaseModel, EmailStr, AnyUrl, Field, computed_field
from typing import List, Dict, Optional, Annotated

class patient(BaseModel):

    name: str
    email: EmailStr
    linkdin_url: AnyUrl
    age: int
    weight: float #KG
    height: float #Meters
    married:bool
    allergies: Optional[List[str]] = None
    contact_details: Dict[str, str]

    @computed_field
    @property
    def bmi(self) -> float:
        bmi = self.weight / (self.height ** 2)
        return round(bmi, 2)
    
def insert_patient_data(patient: patient):
    print(patient.name)
    print(patient.age)
    print("BMI:", patient.bmi)
    # print(patient.email)
    # print(patient.contact_details)
    print("Patient data inserted successfully")

patient_info = {
    "name": "krish",
    "email": "krish@konda.com",
    "linkdin_url": "https://www.linkedin.com/in/krish-konda-123456789/",
    "age": 65,
    "weight": 70.5,
    "height": 1.60,
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