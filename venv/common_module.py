import sys
import os

def resource_path(relative_path):

    if hasattr(sys, '_MEIPASS'):

        return os.path.join(sys._MEIPASS, relative_path)

    return os.path.join(os.path.abspath("."), relative_path)

def rmv_dupl(df, col_name):

    df = df.drop_duplicates([col_name])
    df = df.reset_index().drop(columns="index")

    return df