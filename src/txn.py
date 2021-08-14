import pandas as pd
import numpy as np
import itertools
from operator import itemgetter
from itertools import groupby


# find duplicate transactions
def find_duplicate_transactions(*transactions: dict):
    # initialize "duplicateTransactions" list to be returned
    duplicateTransactions = []
    # sort list based on columns "sourceAccount", "targetAccount", "amount", "category"
    transactions = sorted(list(itertools.chain(*transactions)),
                          key=itemgetter("sourceAccount", "targetAccount", "amount", "category"))

    # group list based on the duplicate values of columns "sourceAccount", "targetAccount", "amount", "category"
    for i, g in groupby(transactions,
                        key=itemgetter("sourceAccount", "targetAccount", "amount", "category")):
        # used python pandas to reduce the complexity to O(n)
        # convert list to dataframe
        df = pd.DataFrame(list(g))
        # update time format to get the time difference in later stage
        df["time"] = pd.to_datetime(df["time"])
        # further group by "category" and sort via "time" in ascending
        df = df.groupby(["category"]).apply(lambda x:
                                x.sort_values(["time"], ascending=True)).reset_index(drop=True)
        # add temporary rows of time diff to get the duplicate values
        # create temporary column 'n_time_diff' with time diff between two consecutive rows
        df['n_time_diff'] = df["time"].diff().apply(lambda x: x / np.timedelta64(1, 's'))

        # create temporary column 'p_time_diff' with time diff between two consecutive rows with shift upwards
        df['p_time_diff'] = df["n_time_diff"].transform(lambda x: x.shift(-1))

        # fetch only the min value in two column to get two rows which have duplicate values
        df['row_rtn'] = df[['n_time_diff', 'p_time_diff']].min(axis=1)

        # apply boundary values with time difference
        df['flag'] = df['row_rtn'].between(0, 60, inclusive="neither")

        # fetch required rows which carries duplicate values and time diff less than a min
        df = df[(df.flag == True)]

        # cleanup task :  drop temporary columns after fetching desired result
        df = df.drop(columns=['n_time_diff', 'row_rtn', 'p_time_diff', 'flag'])

        # format time to get the desired results of outcome
        df["time"] = df["time"].dt.strftime('%Y-%m-%dT%H:%M:%S.%f').str[:-3] + 'Z'

        # return only duplicates and avoid cases of single transactions
        if df.shape[0] > 1:
            duplicateTransactions.append(df.to_dict("records"))

    # return duplicate transactions
    return duplicateTransactions
