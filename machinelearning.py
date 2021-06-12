import sys
sys.path.append('C:/Users/Иван/PycharmProjects/pythonProject')
import getHistory
import json
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from pandas import read_json


def getPrediction(ticker):

    data = getHistory.getHistory(ticker, 60)
    myset = json.dumps(data)
    dataset = read_json(myset)
    dataset = dataset.drop(dataset.columns[4], axis=1)
    dataset = dataset.append({'c':dataset.values[59][0], 'h':dataset.values[59][1], 'l':dataset.values[59][2], 'o':dataset.values[59][3], 'v':dataset.values[59][4], 'isRised': 2}, ignore_index = True)
    scaler = MinMaxScaler(feature_range=(0,1))
    scaled_data = scaler.fit_transform(dataset['c'].values.reshape(-1,1))

    X = (dataset.values)[:,:5]
    y = (dataset.values)[:,5]
    y = y.astype(int)

    X_train, X_validation, Y_train, Y_validation = train_test_split(X, y, test_size=0.015, shuffle=False)

    model = LinearDiscriminantAnalysis()
    model.fit(X_train, Y_train)
    predictions = model.predict(X_validation)
    print(str(predictions[0]))
    return str(predictions[0])