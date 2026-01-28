from datetime import datetime

import numpy as np

from app.features.feature_builder import build_features


def test_feature_builder_shape():
    event = {
        "parsed_type": "auth",
        "status": "FAIL",
        "timestamp": datetime.utcnow(),
        "message": "Failed password",
    }
    features = build_features(event)
    assert isinstance(features, np.ndarray)
    assert features.shape == (5,)
