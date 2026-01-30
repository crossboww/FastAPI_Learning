from pydantic import BaseModel, EmailStr, AnyUrl, Field, field_validator
from typing import List, Dict, Optional, Annotated

class patient(BaseModel):

    name: str
    email: EmailStr
    age: int
    weight: float
    married:bool
    allergies: Optional[List[str]] = None
    contact_details: Dict[str, str]

    @field_validator("email")
    @classmethod
    def email_validator(cls, value):

        valid_domains = ["hdfc.com", "icici.com"]

        domain = value.split("@")[-1]
        if domain not in valid_domains:
            raise ValueError("Invalid email domain")
        return value
    
    @field_validator("name")
    @classmethod
    def transform_name(cls, value):
        return value.upper()
    
    @field_validator("age", mode="after")
    @classmethod
    def age_validator(cls, value):
        if 0 < value < 120:
            return value
        raise ValueError("Age must be between 0 and 120")


def insert_patient_data(patient: patient):
    print(patient.name)
    print(patient.age)
    print(patient.email)

patient_info = {
    "name": "krish",
    "email": "krish@hdfc.com",
    "linkdin_url": "https://www.linkedin.com/in/krish-konda-123456789/",
    "age": 22,
    "weight": 70.5,
    "married": True,
    # "allergies": ["pollen", "dust"],
    "contact_details": {
        "email": "krish@konda.com",
        "phone": "7984992893"
    }
}

patient_obj = patient(**patient_info)

insert_patient_data(patient_obj)