import openpyxl
import re
import pandas as pd
import numpy as np
import sys
import io
from common_module import resource_path, rmv_dupl

# 표준항목 별 WBS 정리

p_inv_filename = "MasterData.xlsx"
inv_data_filename = "inv_data.csv"

p_inv_df = pd.read_excel(resource_path(p_inv_filename), engine="openpyxl", sheet_name="P투자항목", encoding="utf-8")
inv_data_df = pd.read_csv(resource_path(inv_data_filename), encoding="utf-8", low_memory=False)

wbs_df = pd.concat([inv_data_df["프로젝트 정의"],inv_data_df["Project 명"],inv_data_df["WBS 요소"],inv_data_df["WBS 명"]
                ,inv_data_df["전체실적"],inv_data_df["레벨텍스트1"],inv_data_df["레벨텍스트2"],inv_data_df["레벨텍스트3"],inv_data_df["레벨텍스트4"]
                ,inv_data_df["책임 코스트센터"].str.slice(start=0, stop=4),inv_data_df["이름"]],axis=1, join="inner")

#print(wbs_df)

#teamName_df = (inv_data_df["이름"].to_frame()).drop_duplicates(["이름"])
teamCode_Series = inv_data_df["책임 코스트센터"].str.slice(start=0, stop=4)
teamName_df = inv_data_df["이름"].to_frame()
teamName_df['책임 코스트센터'] = teamCode_Series

teamName_df = rmv_dupl(teamName_df, "이름")
teamName_df.to_excel("team_result.xlsx")
teamCode_df = rmv_dupl(teamCode_Series.to_frame(), "책임 코스트센터")

#print(teamName_df)
#print(teamCode_df)
lvlTextCnt = []
projCnt = []
lvlStrList = []
wbsCnt = []

p_inv_df["lvl_index"] = p_inv_df["표준항목레벨4"]+" "+p_inv_df["레벨텍스트4"]
p_inv_df= p_inv_df.set_index("lvl_index")
#print(p_inv_df)

for teamCode in (teamCode_df.to_numpy()).tolist():
    #print(teamCode[0])
    temp_df = wbs_df.loc[wbs_df["책임 코스트센터"]==teamCode[0]]
    lvlText_df = rmv_dupl(temp_df["레벨텍스트4"].to_frame(), "레벨텍스트4")
    proj_df = rmv_dupl(temp_df["프로젝트 정의"].to_frame(), "프로젝트 정의")

    wbsCnt.append(len(temp_df.index))
    lvlTextCnt.append(len(lvlText_df.index))
    projCnt.append(len(proj_df.index))

    lvlText_String = '+'.join(str(e) for e in lvlText_df["레벨텍스트4"].to_numpy().tolist())
    lvlStrList.append(lvlText_String)

teamCode_df["WBS Cnt"] = pd.Series(lvlTextCnt)
teamCode_df["Lvl4 Cnt"] = pd.Series(lvlTextCnt)
teamCode_df["Proj Cnt"] = pd.Series(projCnt)
#teamCode_df["WBS list"] = pd.Series(lvlStrList)
teamCode_df=teamCode_df.set_index("책임 코스트센터")
print(teamCode_df)
teamCode_df.to_excel("wbs_break_result.xlsx")




