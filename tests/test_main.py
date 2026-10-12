import importlib

import pandas as pd


def test_load_or_train_model_returns_pipeline():
    main = importlib.import_module('main')

    model = main.load_or_train_model()
    assert hasattr(model, 'predict')

    sample = pd.DataFrame([
        {
            'Age': 21,
            'Gender': 'Male',
            'Academic_Level': 'Undergraduate',
            'Most_Used_Platform': 'Instagram',
            'Purpose_Of_Use': 'Education',
            'Avg_Daily_Usage_Hours': 4.5,
            'Daily_Unlocks': 120,
            'Study_Hours': 5.0,
            'Physical_Activity_Hours': 2.0,
            'Sleep_Hours_Per_Night': 7.1,
            'Stress_Level': 6,
        }
    ])

    prediction = model.predict(sample)
    assert prediction.shape[0] == 1
