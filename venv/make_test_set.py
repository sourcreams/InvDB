import openpyxl
import re
import pandas as pd
import numpy as np
import sys
import io
from common_module import resource_path, rmv_dupl

# 표준항목 별 WBS 정리

inv_data_filename = "inv_data.csv"
train_set_filename = "train_set.csv"

inv_data_df = pd.read_csv(resource_path(inv_data_filename), encoding="utf-8", low_memory=False)
train_df = pd.read_csv(resource_path(train_set_filename), encoding="utf-8", low_memory=False)

inv_data_df = inv_data_df.append(train_df, ignore_index=True)

test_df = inv_data_df.drop_duplicates(subset= "WBS 요소", keep= False)

test_df.to_csv("test_set.csv", encoding="euc-kr", index=False)

def opt_set(df):

    opt_df = df[["WBS 요소","WBS 명","통제팀","책임 코스트센터","레벨텍스트4"]].copy()
    opt_df["레벨텍스트4"] = (opt_df["레벨텍스트4"].str.slice(start=0, stop=5))
    opt_df["책임 코스트센터"]= opt_df["책임 코스트센터"].str.slice(start=0, stop=4)

    return opt_df


opt_set(train_df).to_csv("train_set_opt.csv", encoding="euc-kr", index=False)

opt_set(test_df).drop("레벨텍스트4", axis=1).to_csv("test_set_opt.csv", encoding="euc-kr", index=False)


