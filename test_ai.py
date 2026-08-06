from modules.anomaly_detector import AnomalyDetector

training_data = [

    [8, 5, 20, 0, 0],
    [9, 4, 18, 0, 1],
    [8, 6, 22, 1, 0],
    [9, 5, 19, 0, 2],
    [8, 5, 21, 0, 0],
    [9, 4, 20, 1, 1],
    [8, 6, 18, 0, 0],
    [9, 5, 23, 1, 1]

]

detector = AnomalyDetector()

detector.train(training_data)

result = detector.predict([23, 100, 450])

print(result)