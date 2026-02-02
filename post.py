from fastapi import FastAPI, Path, HTTPException, Query
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, computed_field
from typing import Annotated, Literal, Optional
import json

app = FastAPI()

class patient(BaseModel):

    id: Annotated[str, Field(..., description="ID of the Patient", example="P001")]
    name: Annotated[str, Field(..., description="Name of the Patient")]
    city: Annotated[str, Field(..., description="City of the Patient")]
    age: Annotated[int, Field(..., gt=0, lt=120, description="Age of the Patient")] 
    gender: Annotated[Literal["male", "female", "other"], Field(..., description="Gender of the Patient")]
    height: Annotated[float, Field(..., description="Height of the Patient in mtr")]
    weight: Annotated[float, Field(..., description="Weight of the Patient in KGs")]

    @computed_field
    @property
    def bmi(self) -> float:
        height_m = self.height/ 100
        bmi = self.weight / (height_m ** 2)
        return round(bmi, 2)
    
    @computed_field
    @property
    def verdict(self) -> str:
        if self.bmi < 18.5:
            return "Underweight"
        elif self.bmi < 25:
            return "Normal weight"
        elif self.bmi < 30:
            return "Overweight"
        else:
            return "Obesity"
        
class PatientUpdate(BaseModel):
    name: Annotated[Optional[str], Field(default=None)]
    city: Annotated[Optional[str], Field(default=None)]
    age: Annotated[Optional[int], Field(default=None, gt=0, lt=120)]
    gender: Annotated[Optional[Literal["male", "female", "other"]], Field(default=None)]
    height: Annotated[Optional[float], Field(default=None, gt=0)]
    weight: Annotated[Optional[float], Field(default=None, gt=0)]


def load_data():
    with open("patients.json", "r") as f:
        data = json.load(f)

    return data

def save_data(data):
    with open("patients.json", "w") as f:
        json.dump(data, f)

    return data

@app.get("/")
def home():
    return{
        "message" : "Welcome to Patients management Application!"
        }


@app.get("/about")
def about():
    return{
        "app": "FastAPI Application",
        "version": "1.0.0",
        "description": "This is a sample FastAPI application."
    }

@app.get("/view")
def view_data():
    data = load_data()
    return data


# -- Making a get request with path parameter --
@app.get("/patients/{patient_id}")
def view_patient(patient_id : str = Path(..., description="The ID of the patient to retrieve", examples="P001")):

    #Load the all data
    data = load_data()

    if patient_id in data:
        return data[patient_id]
    else:
        raise HTTPException(status_code=404, detail="Patient not found")

#-- Making a get request with query parameter --
@app.get("/sort")
def sort_patients(sort_by: str = Query(..., description="Sort on the basis of height, weight or bmi"),
                  order:str = Query("asc", description="Sort in acending or descending order")):
    data = load_data()

    valid_fields = ["height", "weight", "bmi"]

    if sort_by not in valid_fields:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid field select from {valid_fields}"
        )
    
    if order not in ["asc", "desc"]:
        raise HTTPException(
            status_code=400,
            detail="Invalid Order Selected"
        )
    
    sort_order= True if order=="desc" else False
    sorted_data = sorted(data.values(), key=lambda X: X[sort_by], reverse=sort_order)

    return sorted_data

@app.post("/create")
def create_patient(patient: patient):

    # Load the existing data
    data = load_data()

    #Check if patient ID already exists
    if patient.id in data:
        raise HTTPException(
            status_code=400,
            detail="Patient with this ID already exists"
        )
    
    #New data add to the database
    data[patient.id] = patient.model_dump(exclude=["id"])

    # Save the updated data back to the file
    save_data(data)

    return JSONResponse(
        status_code=201,
        content={
            "message": "Patient created successfully",
            "patient_id": patient.id
        }
    )

@app.put("/update/{patient_id}")
def update_patient(patient_id: str, patient_update: PatientUpdate):

    #Load the existing data
    data = load_data()
    if patient_id not in data:
        raise HTTPException(status_code=404, detail="Patient not found")
    
    existing_patient_info = data[patient_id]

    updated_patient_info = patient_update.model_dump(exclude_unset=True)

    for key, value in updated_patient_info.items():
        existing_patient_info[key] = value

    #existing_patient_info -> pydantic object -> updated bmi and verdict
    existing_patient_info["id"] = patient_id
    patient_pydantic_obj= patient(**existing_patient_info)

    #convert Pydantic object to dictionary
    existing_patient_info = patient_pydantic_obj.model_dump(exclude=["id"])

    #Add this Dict to the data
    data[patient_id] = existing_patient_info

    #Save the data
    save_data(data)

    return JSONResponse(
        status_code=200,
        content={
            "message": "Patient information updated successfully"
        }
    )

@app.delete("/delete/{patient_id}")
def delete_patient(patient_id: str):

    #Load the existing  data
    data = load_data()

    if patient_id not in data:
        raise HTTPException(status_code=404, detail="Patient not found")
    
    #Delete the patient Records
    del data[patient_id]

    #Save the data
    save_data(data)

    return JSONResponse(
        status_code=200,
        content={
            "message": "Patient record deleted successfully"
        }
    )

