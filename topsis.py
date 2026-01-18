import pandas as pd
import numpy as np
import os

def error(msg):
    raise Exception(msg)

def run_topsis(input_file, weights_str, impacts_str, output_file):

    if not os.path.exists(input_file):
        error("Input file not found")

    try:
        df = pd.read_csv(input_file)
    except:
        error("Unable to read input file")

    if df.shape[1] < 3:
        error("Input file must contain three or more columns")

    data = df.iloc[:, 1:]

    if not np.all(data.applymap(lambda x: isinstance(x, (int, float)))):
        error("From 2nd to last columns must contain numeric values only")

    weights = weights_str.split(',')
    impacts = impacts_str.split(',')

    if len(weights) != data.shape[1]:
        error("Number of weights must be equal to number of criteria")

    if len(impacts) != data.shape[1]:
        error("Number of impacts must be equal to number of criteria")

    try:
        weights = np.array(weights, dtype=float)
    except:
        error("Weights must be numeric")

    for i in impacts:
        if i not in ['+', '-']:
            error("Impacts must be either + or -")

    # Normalization
    norm_data = data / np.sqrt((data ** 2).sum())

    # Weighted normalized matrix
    weighted_data = norm_data * weights

    # Ideal best & worst
    ideal_best = []
    ideal_worst = []

    for i in range(len(impacts)):
        if impacts[i] == '+':
            ideal_best.append(weighted_data.iloc[:, i].max())
            ideal_worst.append(weighted_data.iloc[:, i].min())
        else:
            ideal_best.append(weighted_data.iloc[:, i].min())
            ideal_worst.append(weighted_data.iloc[:, i].max())

    # Distances
    dist_best = np.sqrt(((weighted_data - ideal_best) ** 2).sum(axis=1))
    dist_worst = np.sqrt(((weighted_data - ideal_worst) ** 2).sum(axis=1))

    # TOPSIS score & rank
    topsis_score = dist_worst / (dist_best + dist_worst)
    rank = topsis_score.rank(ascending=False, method='dense')

    df['Topsis Score'] = topsis_score
    df['Rank'] = rank.astype(int)

    df.to_csv(output_file, index=False)
