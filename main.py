from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import pandas as pd
import numpy as np
from sklearn.neighbors import NearestNeighbors

app = FastAPI()

# Enable CORS for frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all for development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Input model for quiz
class QuizAnswers(BaseModel):
    genre: str
    music_feeling: str
    taylor_era: str
    concert_experience: str
    lyrical_vibe: str
    daily_soundtrack: str

# Convert quiz answers to score values
def calculate_scores(answers):
    scores = {"energy_score": 0, "hype_factor": 0, "cozy_level": 0, "speech_influence": 0}

    dataset_ranges = {
        "energy_score": (1.6877, 6.07),
        "cozy_level": (0.2011, 2.709),
        "hype_factor": (5.4183, 7.8845),
        "speech_influence": (1.492, 2.868)
    }

    mapping = {
        0: {"Pop": (1, 2, 0, 0), "Classical": (-2, -1, 3, 0), "Electronic": (2, 3, -2, 0), "Hip Hop": (2, 2, -1, 3)},
        1: {"Sweater Weather Softcore": (-1, -1, 3, 0), "Sad Girl Summer": (0, 1, 1, 1),
            "Dancefloor Drama": (2, 3, -2, 0), "Bars and Beats": (2, 2, -1, 3)},
        2: {"Lover": (1, 2, 1, 0), "Reputation": (3, 3, -2, 2), "1989": (2, 3, -1, 0), "Red": (1, 1, 2, 1),
            "The Tortured Poets Department": (-1, -1, 3, 2), "Fearless": (1, 1, 2, 0),
            "Folklore": (-2, -2, 3, 0), "Evermore": (-2, -2, 3, 0), "Speak Now": (1, 1, 1, 1)},
        3: {"Massive stadium. Flashing lights.": (3, 3, -2, 2),
            "Music festival with tons of dancing": (2, 3, -1, 0),
            "Small, Lowkey, Acoustic Setup": (-2, -2, 3, 0),
            "High-Energy Rave Craze": (3, 3, -3, 0)},
        4: {"Deep and Poetic": (-1, 0, 2, 2), "Catchy and Fun": (2, 3, -1, 0),
            "Fast-paced and Witty": (3, 2, -2, 3), "Dramatic and Powerful": (2, 1, -1, 1)},
        5: {"Soft, cozy, and warm": (-2, -2, 3, 0), "Bright, fun and energetic": (2, 2, 0, 0),
            "Mysterious, edgy, and bold": (2, 1, -1, 2), "Chill, smooth and vibey": (-1, -1, 2, 0)}
    }

    for i, answer in enumerate(answers):
        if answer in mapping[i]:
            energy, hype, cozy, speech = mapping[i][answer]
            scores["energy_score"] += energy
            scores["hype_factor"] += hype
            scores["cozy_level"] += cozy
            scores["speech_influence"] += speech

    for feature, (data_min, data_max) in dataset_ranges.items():
        raw_min, raw_max = -3, 3
        scores[feature] = ((scores[feature] - raw_min) / (raw_max - raw_min)) * (data_max - data_min) + data_min

    return scores

# Use your actual formulas to compute the derived columns
def create_composite_features(df):
    df["energy_score"] = (df["danceability"] + abs(df["loudness"]) + df["valence"]) / 3
    df["cozy_level"] = ((df["acousticness"] + (1 - df["tempo"] / 200)) / 2) * 10
    df["hype_factor"] = ((df["popularity"] + df["energy"] + df["loudness"]) / 3) / 10
    df["speech_influence"] = ((df["speechiness"] * 2 + df["danceability"]) * 10) / 3
    return df

@app.post("/recommend_song")
async def recommend_song(answers: QuizAnswers):
    user_answers = [
        answers.genre,
        answers.music_feeling,
        answers.taylor_era,
        answers.concert_experience,
        answers.lyrical_vibe,
        answers.daily_soundtrack,
    ]

    user_scores = calculate_scores(user_answers)

    df = pd.read_csv("data.csv")
    df = create_composite_features(df)

    feature_columns = ["energy_score", "cozy_level", "hype_factor", "speech_influence"]
    user_vector = np.array([
        user_scores["energy_score"],
        user_scores["cozy_level"],
        user_scores["hype_factor"],
        user_scores["speech_influence"]
    ]).reshape(1, -1)

    knn = NearestNeighbors(n_neighbors=1, metric="euclidean")
    knn.fit(df[feature_columns])
    distances, indices = knn.kneighbors(user_vector)

    recommended_song = df.iloc[indices[0][0]]["song_name"]

    return {"recommended_song": recommended_song}

@app.get("/")
async def serve_quiz():
    return HTMLResponse(content=open("index.html").read(), status_code=200)
