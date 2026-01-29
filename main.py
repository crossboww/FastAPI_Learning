from fastapi import FastAPI, Path, HTTPException, Query
import json

def load_data():
    with open('patients.json', 'r') as f:
        data = json.load(f)
    
    return data

app = FastAPI()

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
def view_patient(patient_id : str = Path(..., description="The ID of the patient to retrieve", example="P001")):

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