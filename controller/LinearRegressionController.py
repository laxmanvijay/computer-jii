from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.externals import joblib
import json
import numpy as np
import pandas as pd


def LinearRegressionController(request=None):
    user_name = request.form['user_name']
    model_name = request.form['model_name']
    if request.form['process']=='train':
        x_features = request.form['x_features']
        x_features = properify(x_features)
        y_features = request.form['y_features']
        test_size = float(request.form['test_size'])
        dataset = request.files['data']
        df = pd.read_csv(dataset)
        X_data = df[['Avg. Area Income', 'Avg. Area House Age', 'Avg. Area Number of Rooms','Avg. Area Number of Bedrooms', 'Area Population']]
        label = df[y_features]
        X_train, X_test, y_train, y_test = train_test_split(X_data, label, test_size=test_size, random_state=101)
        lr = LinearRegression()
        lr.fit(X_train,y_train)
        joblib.dump(lr,'trained_models/'+'linear_model'+user_name+model_name+'.pkl')
        return 'Ok model trained'
    x = request.form['x']
    lr = joblib.load('trained_models/'+'linear_model'+user_name+model_name+'.pkl')
    return " ".join(list(map(str,lr.predict(x))))

def properify(features):
    t = features.split(',')
    print(t)
    return t