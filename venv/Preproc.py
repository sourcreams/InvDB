import openpyxl
import re
import pandas as pd
import numpy as np
from kiwipiepy import Kiwi, Option

file_Name = r"C:\Users\6408284\Desktop\투자비시스템개선\WBS표준화\2013 - 2019.xlsx"
file_Name = r"C:\Users\6408284\Desktop\투자비시스템개선\WBS표준화\2013 - 2019.XLSX"
kiwi=Kiwi(num_workers=0)


class ReaderExam:
    def __init__(self, filePath):
        self.file = open(filePath)

    def read(self, id):
        if id == 0: self.file.seek(0)
        return self.file.readline()


def dict_test():
    kiwi.load_user_dictionary('user_dic.txt')
    kiwi.prepare()
    data = np.loadtxt('test.txt', dtype=np.str, delimiter="\n")
    data_list = data.tolist()

    result_data = list()

    for result in kiwi.analyze(data_list, top_n=1):
        tokens, score = result[0]
        #print(tokens)
        result_string = ""

        for i in tokens:

            result_string = result_string + "," + i[0]

        result_string=result_string[1::]
        result_data.append(result_string)

    print(data.dtype)
    print(data)

    final_data = np.zeros((85919, 2), dtype="<U60")
    final_data[:, 0] = data
    final_data[:, 1] = result_data
    print(final_data)

    #final_data = np.c_( data, np.array(result_data).transpose())
    np.savetxt('final.txt', final_data, fmt="%s", delimiter="\t", encoding="UTF-8")

    #print(result_data)


def testfunc(file_Name):
    df = pd.read_excel(file_Name, sheet_name='PreProc', engine='openpyxl')
    #df['Fix_WBS_Name'] = df['WBS_Name'].str.replace('[A-Z][A-Z][i|c|a|e|r|b|0-9|A-Z]{0,1}','',regex=True)
    df['WBS_Name'] = df['WBS_Name'].str.replace('_',' ',regex=False)
    df['WBS_Name'] = df['WBS_Name'].str.replace('[', ' ', regex=False)
    df['WBS_Name'] = df['WBS_Name'].str.replace(']', ' ', regex=False)
    df['WBS_Name'] = df['WBS_Name'].str.replace('(', ' ', regex=False)
    df['WBS_Name'] = df['WBS_Name'].str.replace(')', ' ', regex=False)
    df['WBS_Name'] = df['WBS_Name'].str.replace('&', ' ', regex=False)
    df['WBS_Name'] = df['WBS_Name'].str.replace('>', ' ', regex=False)
    df['WBS_Name'] = df['WBS_Name'].str.replace(',', ' ', regex=False)
    df['new_WBS_name'] = df.apply(lambda x : replace_wbs(x['Project_Name'],x['WBS_Name']),axis=1)
    #reader = np.array2string(df['new_WBS_name'].to_numpy())
    np.savetxt('test.txt', df['new_WBS_name'].to_numpy(), fmt="%s", delimiter=",")
    reader = ReaderExam('test.txt')
    tuple_list = kiwi.extract_words(reader.read, min_cnt=10, max_word_len=10, min_score=0.25)

    for i in range(0,len(tuple_list)):

        tuple_list[i] = list(tuple_list[i])
        list.insert(tuple_list[i],1,"NNP")

    tuple_array = np.array(tuple_list)
    print(tuple_array)

    np.savetxt('output.txt', tuple_array[:,0:2], fmt="%s", delimiter="\t")


def replace_wbs(proj_name,wbs_name):

    reg_ex1 = re.compile('[A-Z][A-Z][i|c|a|e|r|b|0-9|A-Z]{0,1}')
    m = reg_ex1.match(proj_name)
    if m:
        return str.replace(wbs_name,m.group(),"")
    else :
        return wbs_name

def pre_proc_proj(file_Name):
    targetBk = openpyxl.load_workbook(file_Name)
    targetSht = targetBk["Proj"]

    reg_ex1 = re.compile('[A-Z][A-Z][i|c|a|e|r|b|0-9|A-Z]{0,1}')

    for i in range(2, targetSht.max_row + 1):
        str_val = targetSht.cell(row=i, column=1).value
        m = reg_ex1.match(str_val)
        if m:
            print('Match found: ', m.group())
            targetSht.cell(row=i, column=2).value = m.group()
        else:
            print('No match')

    targetBk.save(file_Name)
    targetBk.close()

#testfunc(file_Name)
dict_test()