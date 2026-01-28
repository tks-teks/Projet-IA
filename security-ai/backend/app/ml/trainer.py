from typing import List

import joblib
from sklearn.ensemble import IsolationForest

from app.config import settings
from app.features.feature_builder import batch_features


def train_model(events: List[dict]) -> IsolationForest:
    features = batch_features(events)
    model = IsolationForest(n_estimators=100, contamination=0.08, random_state=42)
    model.fit(features)
    joblib.dump(model, settings.model_path)
    return model
