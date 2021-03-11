import openpyxl
import re
import pandas as pd
import numpy as np
import sys
import io
from common_module import resource_path

# CN7 VS AD 표준항목 단위 실적 비교

p_inv_filename = "MasterData.xlsx"
ad_filename = "AD.xlsx"
cn7_filename= "CN7.xlsx"


p_inv_df = pd.read_excel(resource_path(p_inv_filename), engine="openpyxl", sheet_name="P투자항목", encoding="utf-8")
ad_df = pd.read_excel(resource_path(ad_filename), engine="openpyxl", sheet_name="WBS", encoding="utf-8")
cn7_df = pd.read_excel(resource_path(cn7_filename), engine="openpyxl", sheet_name="WBS", encoding="utf-8")

p_inv_df["lvl_index"] = p_inv_df["표준항목레벨4"]+" "+p_inv_df["레벨텍스트4"]
p_inv_df= p_inv_df.set_index("lvl_index")
print(p_inv_df)

exe_sum = ad_df.groupby("레벨텍스트4")["전체실적"].sum()
df_exe_sum = exe_sum.to_frame()
df_exe_sum.rename(columns={"전체실적":"AD_실적"},inplace=True)

meg_1 = pd.merge(p_inv_df,df_exe_sum,left_index=True,right_index=True,how="left")
print(meg_1.columns)


exe_sum = cn7_df.groupby("레벨텍스트4")["전체실적"].sum()
df_exe_sum = exe_sum.to_frame()
df_exe_sum.rename(columns={"전체실적":"CN7_실적"},inplace=True)

meg_2 = pd.merge(meg_1,df_exe_sum,left_index=True,right_index=True,how="left")
print(meg_2)

meg_2.to_excel("compare.xlsx",sheet_name="compare")