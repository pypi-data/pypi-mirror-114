import joblib
import pandas as pd
from os import path
from sklearn.feature_extraction.text import CountVectorizer

csv_path = path.join(path.dirname(__file__), "emotions.csv")
emotion_dataset = pd.read_csv(csv_path)

pkl_path = path.join(path.dirname(__file__), "emotion_classifier_model.pkl")
model = joblib.load(pkl_path)

features = emotion_dataset['Clean Text']
cv = CountVectorizer()
cv.fit_transform(features)


def find_mood(entry):
    text = [entry]
    vect = cv.transform(text).toarray()
    predictions = model.predict_proba(vect)
    try:
        all_predictions = dict(zip(model.classes_, predictions[0]))
        emotions = sorted(all_predictions, key=all_predictions.get, reverse=True)[:2]
    except:
        return None

    return emotions
