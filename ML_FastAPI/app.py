from fastapi import FastAPI
from fastapi.responses import JSONResponse
from typing import Literal, Annotated
from pydantic import BaseModel, Field, computed_field
import pickle
import pandas as pd
import os


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "model.pkl")

#Import the ML Model
with open(MODEL_PATH, "rb") as f:
    model = pickle.load(f)

tier_1_cities = ["Mumbai", "Delhi", "Bangalore", "Chennai", "Kolkata", "Hyderabad", "Pune"]
tier_2_cities = [
    "Jaipur", "Chandigarh", "Indore", "Lucknow", "Patna", "Ranchi", "Visakhapatnam", "Coimbatore",
    "Bhopal", "Nagpur", "Vadodara", "Surat", "Rajkot", "Jodhpur", "Raipur", "Amritsar", "Varanasi",
    "Agra", "Dehradun", "Mysore", "Jabalpur", "Guwahati", "Thiruvananthapuram", "Ludhiana", "Nashik",
    "Allahabad", "Udaipur", "Aurangabad", "Hubli", "Belgaum", "Salem", "Vijayawada", "Tiruchirappalli",
    "Bhavnagar", "Gwalior", "Dhanbad", "Bareilly", "Aligarh", "Gaya", "Kozhikode", "Warangal",
    "Kolhapur", "Bilaspur", "Jalandhar", "Noida", "Guntur", "Asansol", "Siliguri"
]

app = FastAPI()

#pydantic model for input data validation
class UserInput(BaseModel):
    age: Annotated[int, Field(..., gt=0, description="Age must be a positive integer")]
    weight: Annotated[float, Field(..., gt=0, description="Weight of the user")]
    height: Annotated[float, Field(gt=0, description="Height of the user")]
    income_lpa: Annotated[float, Field(..., gt=0, description="Annual Salary of User in LLPA")]
    smoker: Annotated[bool, Field(..., description="Is user a smoker?")]
    city: Annotated[str, Field(..., description="The city that user belongs to")]
    occupation: Annotated[Literal["retired", "freelancer", "student", "government_job","business_owner", "unemployed","private_job" ], Field(..., description="Occupation of the user")]

    @computed_field
    @property
    def bmi(self) -> float:
        height_m = self.height / 100
        return self.weight/(height_m ** 2)
    
    @computed_field
    @property
    def lifestyle_risk(self) -> str:
        if self.smoker and self.bmi > 30:
            return "high"
        elif self.smoker or self.bmi > 27:
            return "medium"
        else:
            return "low"
    
    @computed_field
    @property
    def age_group(self) -> str:
        if self.age < 25:
            return "young"
        elif self.age < 45:
            return "adult"
        elif self.age < 65:
            return "middle_aged"
        else:
            return "senior"
        
    @computed_field
    @property
    def city_tier(self) -> int:
        if self.city in tier_1_cities:
            return 1
        elif self.city in tier_2_cities:
            return 2
        else:
            return 3

@app.post("/predict")
def predict_premium(data: UserInput):

    input_df = pd.DataFrame([{
        "bmi": data.bmi,
        "age_group": data.age_group,
        "lifestyle_risk": data.lifestyle_risk,
        "city_tier": data.city_tier,
        "income_lpa": data.income_lpa,
        "occupation": data.occupation
        }])

    prediction = model.predict(input_df)[0]

    return JSONResponse(status_code=200, content={"Predicted_category": prediction})