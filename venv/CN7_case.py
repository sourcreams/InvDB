import openpyxl
import re
import pandas as pd
import numpy as np
import sys
import io
from common_module import resource_path

procurement_file_Name = r"C:\Users\6408284\Desktop\투자비시스템개선\WBS표준화\청구내역\2016.xlsx"
wbs_file_Name = r"C:\Users\6408284\Desktop\투자비시스템개선\CN7_SP2.XLSX"
wbs_file_Name_csv = r"C:\Users\6408284\Desktop\투자비시스템개선\CN7_SP2.csv"


def test():
    conn_String = r'DRIVER={Microsoft Excel Driver (*.xls, *.xlsx, *.xlsm, *.xlsb)};' \
                  r'DBQ=' + resource_path("MasterData.xlsx") + ';' \
                                                               r'ReadOnly=1'

    conn = pyodbc.connect(conn_String, autocommit=True)
    cursor = conn.cursor()

print(sys.stdin.encoding)
print(sys.stdout.encoding)

#df_cn7 = pd.read_csv(wbs_file_Name, engine="openpyxl", sheet_name="LvlText", encoding="utf-8")
df_cn7 = pd.read_csv(wbs_file_Name_csv)
print(df_cn7)

print(df_cn7.filter(like="○", axis=0))




