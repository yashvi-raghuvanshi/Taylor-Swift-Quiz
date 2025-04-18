import pandas as pd
import numpy as np
import joblib


from fastapi import FastAPI
from pydantic import BaseModel
from scipy.spatial.distance import euclidean
import sklearn


# from google.colab import files
# files.download('scaler.pkl')
# files.download('df.pkl')
# files.download('features_columns.pkl')

# Load saved files
scaler = joblib.load('scaler.pkl')  
df = joblib.load('df.pkl')    
feature_columns = joblib.load('features.pkl') 


# Create FastAPI app
app = FastAPI()


@app.get("/")
def read_root():
    return {"message": "API running"}

# Define input model
class UserInput(BaseModel):
    energy: float
    cozy: float
    hype: float
    speech: float

@app.post("/recommended_song")
def recommend_song(user_input: UserInput):

    user_profile = pd.DataFrame(np.array([[user_input.energy, user_input.cozy, user_input.hype, user_input.speech]]), columns=feature_columns)
    
    user_scaled = scaler.transform(user_profile)
    
    # Find distance to all songs
    df["distance"] = df.apply(lambda row: euclidean(user_scaled[0], row[feature_columns]), axis=1)
    
    recommended_song = df.loc[df["distance"].idxmin(), "name"]
    
    return {"recommended_song": recommended_song}