import tkinter.filedialog
import pandas as pd
import os
import datetime
import re
import shutil

starttime=datetime.datetime.now()


path=os.getcwd()+'\\RNC_Result'
if os.path.exists(path):
    shutil.rmtree(path)
    os.makedirs('RNC_Result')
    os.chdir(path)
else:
    os.makedirs('RNC_Result')
    os.chdir(path)

def open_file():
    file_names = tkinter.filedialog.askopenfilenames(initialdir=r'D:')
    if file_names != '':
        string_filename=""
        for i in range(0, len(file_names)):
            string_filename += str(file_names[i]) + "\n"
        print("The file you choose to process is/are \n"+ string_filename)
    else:
        print("You didn't choose any files!")
    return file_names

def read_command(cfg_mml):
    mml_file=open(cfg_mml, 'r', encoding='utf-8')    # 打开文件，路径可通过其他设置
    mml_dic={}  #建立空字典
    command_filter_1=r'(SET.*?;)'   #只匹配Cell及NodeB命令行
    command_filter_2 = r'(SET.*?CELLID.*?;)'
    command_filter_3 = r'(.*?-.*?&)'
    try:
        for line in mml_file:        #直接for循环file对象
            if not re.match(command_filter_1,line):      #如果该行和filter不匹配，跳过读取下一行。
                continue
            if re.match(command_filter_2,line):
                continue
            line=line.strip()
            line = line.strip(';')      #清除结尾的分号
            if len(line):
                key=line.split(':')[0]
                if not key in mml_dic.keys():
                    mml_dic[key] = []
                    values=mml_dic.get(key)
                    temp_1=line.split(':')[1].strip()
                    x = [x for x in temp_1.split(',')]
                    sub_keys=[]
                    sub_values=[]
                    for every in x:
                        every = every.split('=')
                        temp_2=every[1].strip()
                        if re.match(command_filter_3,temp_2):
                            sub_x = [sub_x for sub_x in temp_2.split('&')]
                            for sub_every in sub_x:
                                sub_every=sub_every.split('-')
                                sub_key=every[0].strip()+'-'+sub_every[0].strip()
                                sub_keys.append(sub_key)
                                sub_values.append(sub_every[1].strip())
                        else:
                            sub_keys.append(every[0].strip())
                            sub_values.append(every[1].strip())
                    line_dic = dict(zip(sub_keys, sub_values))
                    values.append(line_dic)
                    mml_dic[key] = values
                else:
                    values=mml_dic.get(key)
                    temp=line.split(':')[1].strip()
                    x = [x for x in temp.split(',')]
                    sub_keys=[]
                    sub_values=[]
                    for every in x:
                        every = every.split("=")
                        temp_2=every[1].strip()
                        if re.match(command_filter_3,temp_2):
                            sub_x = [sub_x for sub_x in temp_2.split('&')]
                            for sub_every in sub_x:
                                sub_every=sub_every.split('-')
                                sub_key=every[0].strip()+'-'+sub_every[0].strip()
                                sub_keys.append(sub_key)
                                sub_values.append(sub_every[1].strip())
                        else:
                            sub_keys.append(every[0].strip())
                            sub_values.append(every[1].strip())
                    line_dic = dict(zip(sub_keys, sub_values))
                    values.append(line_dic)
                    mml_dic[key] = values
            else:
                continue
    finally:
        mml_file.close()
    return mml_dic


def get_folder_name(file_path):
    folder_name=file_path.split('/')
    folder_name=folder_name[len(folder_name)-1]
    folder_name=folder_name.split('.')
    folder_name=folder_name[0]
    return  folder_name

for file in open_file():
    print("Currently it is processing "+str(file))
    sub_start=datetime.datetime.now()
    os.chdir(path)
    sub_folder=get_folder_name(file)
    os.makedirs(sub_folder)
    sub_path=path+'\\'+sub_folder
    os.chdir(sub_path)
    for mml,val in read_command(file).items():
        file_name=mml+'.xlsx'
        df=pd.DataFrame(val)
        df=df.T
        df.to_excel(file_name,sheet_name=mml,header=True,index=True)
    sub_end=datetime.datetime.now()
    print(str((sub_end - sub_start).seconds) + " seconds consumed on processing "+sub_folder)

endtime=datetime.datetime.now()
print(str((endtime-starttime).seconds) + " seconds consumed in total")
