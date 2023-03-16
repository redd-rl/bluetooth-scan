from collections import Counter
from numpy import std
from numpy import mean

def detect_abnormality(array: list) -> bool:
    if len(array) < 6:
        return "Not enough data to determine"
    arrayDeviation = int(std(array))
    arrayMean = int(mean(array))
    cut_off = arrayDeviation * 6
    lower_bound = arrayMean - cut_off
    upper_bound = arrayMean + cut_off
    anomalies = [i for i in array if not i in range(lower_bound, upper_bound)]
    return True if anomalies else False
