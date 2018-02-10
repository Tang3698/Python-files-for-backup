#  读入数据模型,生成字典列表{{命令名称1：['第一行'{{参数1:值1},{参数2:值2}....},...'第N行'{{参数1:值1},{参数2:值2}....}....]},{命令名称2：[{[{},{}....},{{},{}...},{{},{}....}....]}}
#  输出方法，list of dict生成DataFrame
# V1.1 引入pyexcelerate输出xlsx文件，提高输出速度

import tkinter.filedialog
import pandas as pd
import os
import datetime
import re
import shutil
from pyexcelerate import Workbook


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


def create_dir(path):
    if os.path.exists(path):
        shutil.rmtree(path)
        os.makedirs('Result')
        os.chdir(path)
    else:
        os.makedirs('Result')
        os.chdir(path)

def read_command(cfg_mml):
    mml_file=open(cfg_mml, 'r')    # 打开文件，路径可通过其他设置
    mml_dic={}  #建立空字典
    command_filter_1=['ADD UCELLSETUP','ADD UINTRAFREQNCELL']
    command_filter_2=r'(.*?-.*?&)'   #用于匹配含有多个子参数项的命令
    try:
        for line in mml_file:        #直接for循环file对象
            if not line.split(':')[0] in command_filter_1:      #如果该行和filter不匹配，跳过读取下一行。
                continue
            line=line.strip()    #清楚首尾空格
            line = line.strip(';')      #清除结尾的分号
            if len(line):
                key=line.split(':')[0]       #以分号分割每一行，提取前面的命令名称作为 键
                if not key in mml_dic.keys(): #处理第一次出现的命令
                    mml_dic[key] = []          # 给mml_dic装入该键对应的值-空列表
                    values=mml_dic.get(key)       #提取该键对应的值，赋给values
                    temp=line.split(':')[1].strip()  #读入命令中的参数内容，即分号后的内容，进行处理
                    x = [x for x in temp.split(',')]  #逗号分割，生成list
                    sub_keys=[]  #建立空list，用于存储每个参数及对应的值
                    sub_values=[]
                    for every in x:    #对逗号分割后的每个参数进行循环处理
                        every = every.split("=")
                        temp_2=every[1].strip()
                        if re.match(command_filter_2,temp_2):   #判断参数中是否包含子参数项
                            sub_x = [sub_x for sub_x in temp_2.split('&')]
                            for sub_every in sub_x:
                                sub_every=sub_every.split('-')
                                sub_key=every[0].strip()+'-'+sub_every[0].strip()
                                sub_keys.append(sub_key)
                                sub_values.append(sub_every[1].strip())
                        else:
                            sub_keys.append(every[0].strip())
                            sub_values.append(every[1].strip())
                    line_dic = dict(zip(sub_keys, sub_values))  #每一行数据生成一个字典
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
                        if re.match(command_filter_2,temp_2):
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
                    values.append(line_dic)  #添加多行数据
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

def export(path):
    for file in open_file():
        print("Currently it is processing "+str(file))
        sub_start=datetime.datetime.now()
        os.chdir(path)
        sub_folder=get_folder_name(file)
        output_file=sub_folder+'CFGMML_output.xlsx'
        wb=Workbook()
        for mml,val in read_command(file).items():
            df=pd.DataFrame(val)
            data = [df.columns.tolist(), ] + df.values.tolist()
            try:
                wb.new_sheet(mml, data=data)
                print(mml)
            except:
                continue
        wb.save(output_file)
        sub_end=datetime.datetime.now()
        print(str((sub_end - sub_start).seconds) + " seconds consumed on processing "+str(file))

def save_all():
     starttime=datetime.datetime.now()
     path = os.getcwd() + '\\Result'
     create_dir(path)
     export(path)
     endtime=datetime.datetime.now()
     print((endtime-starttime).seconds)


if __name__ == '__main__':
    save_all()