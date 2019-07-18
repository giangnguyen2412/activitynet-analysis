"""
Created on Nov 7, 2018

@author: Giang Nguyen
@email: dexter.nguyen7@kaist.ac.kr
"""


import json
import pandas as pd
import re


def read_data(path):
    """
    Read json data files
    :param: path: The relative path to the input dataset directory (string)
    :return: df: The dataset in dataframe format (dataframe)
    """

    df = pd.DataFrame(columns=[])
    prep_dict = {}

    with open(path, 'r') as f:
        raw = json.load(f)
        for key, obj in raw.items():
            sub_obj_num = len(obj['timestamps']) # Number of cuts in a video
            for i in range(sub_obj_num):
                sub_obj_key = key + str(i)
                prep_dict[sub_obj_key] = obj['timestamps'][i][1] - obj['timestamps'][i][0]  # stop_time- start_time
                if prep_dict[sub_obj_key] <= 0:
                    print("In video of ID {}, the {}th cut has wrong annotations when start time is {} and "
                          "stop time is {}".format(key, (i+1), obj['timestamps'][i][0], obj['timestamps'][i][1]))

        data_df = pd.DataFrame.from_dict(prep_dict, orient='index')
        df = pd.concat([df, data_df], axis=0, sort=True)

    return df


df = read_data('train.json')
df.dropna(inplace=True)
#print(df)

percentiles = [.10, .20, .30, .40, .50, .60, .70, .80, .90]
include = ['float', 'int', 'object']
desc = df.describe(percentiles=percentiles, include=include)
#print(desc)

print("To debug above")
