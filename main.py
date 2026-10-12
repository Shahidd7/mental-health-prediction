from fastapi import FastAPI
from pydantic import BaseModel,Field
from typing import Literal
import joblib 
import pandas as pd
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
app = FastAPI()

model = joblib.load('Mental_Health_Prediction.pkl')

app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get('/')
def home():
    return FileResponse('static/index.html')

class StudentData(BaseModel):
    Age: int = Field(...,ge = 0 ,le = 100)
    Gender:Literal["Male",'Female']
    Academic_Level:Literal['Undergraduate', 'Graduate', 'High School']
    most_used_platform: Literal['Facebook', 'LinkedIn', 'Instagram', 'Snapchat','Twitter','YouTube', 'TikTok', 'LINE', 'KakaoTalk', 'VKontakte', 'WhatsApp','WeChat']
    purpose_of_use: Literal['Networking', 'Education', 'Entertainment', 'News']
    Avg_Daily_Usage_Hours: float = Field(...,ge = 0 ,le = 24)
    Daily_Unlocks: int= Field(...,ge = 0)
    Study_Hours: float= Field(...,ge = 0 ,le = 24)
    Physical_Activity_Hours: float= Field(...,ge = 0 ,le = 24)
    Sleep_Hours_Per_Night: float= Field(...,ge = 0 ,le = 24)
    Stress_Level: Literal['Medium', 'Low', 'Very High', 'High']

class Predictionresponse(BaseModel):
    predicted: float

@app.post('/predict', response_model=Predictionresponse)
def predict(data:StudentData):
    input_data = pd.DataFrame([{
        'Age'                       :data.Age,
        'Gender'                    :data.Gender,
        'Academic_Level'            :data.Academic_Level,
        'Most_Used_Platform'        :data.most_used_platform,
        'Purpose_Of_Use'            :data.purpose_of_use,
        'Avg_Daily_Usage_Hours'     :data.Avg_Daily_Usage_Hours,
        'Daily_Unlocks'             :data.Daily_Unlocks,
        'Study_Hours'               :data.Study_Hours,
        'Physical_Activity_Hours'   :data.Physical_Activity_Hours,
        'Sleep_Hours_Per_Night'     :data.Sleep_Hours_Per_Night,
        'Stress_Level'              :data.Stress_Level
   }])

    prediction = model.predict(input_data)[0]
    return Predictionresponse(predicted=round(float(prediction), 2))
