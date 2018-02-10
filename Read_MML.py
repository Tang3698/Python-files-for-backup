import tkinter.filedialog
import pandas as pd
import itertools

#def open_file():
#    filename = tkinter.filedialog.askopenfilename(initialdir=r'D:\Reference Documents\Code\Python\WorkspaceforPython\PyCharmSpace')
#    if filename != '':
#        print("The file you choose to process is "+ filename)
#    else:
#        print("You didn't choose any files!")
#    return filename
def remove_duplicate(seq, idfun=None): # Alex Martelli ******* order preserving
    if idfun is None:
        def idfun(x): return x
    seen = {}
    result = []
    for item in seq:
        marker = idfun(item)
        # in old Python versions:
        # if seen.has_key(marker)
        # but in new ones:
        if marker in seen: continue
        seen[marker] = 1
        result.append(item)
    return result

def read_command():
    with open(r'Read_MML Sample.txt', 'r', encoding='utf-8') as f:  # 打开文件，路径可通过其他设置
        mml_file = f.readlines()
    mml_dic={}  #建立空字典
    for line in mml_file:
        line=line.strip()
        line=line.strip(';')
        if len(line):
            key=line.split(':')[0]
            if not key in mml_dic.keys():
                mml_dic[key] = []
                value=mml_dic.get(key)
                value.append(line.split(':')[1].strip())
                mml_dic[key] = value
            else:
                value=mml_dic.get(key)
                value.append(line.split(':')[1].strip())
                mml_dic[key] = value
        else:
            continue
    return mml_dic

#获取每个命令的参数列表
parameter_table={}
for command,parameter in read_command().items():
    parameter_list = []
    for line in parameter:
        x=[x for x in line.split(',')]
        for each in x:
            each=each.split("=")
            parameter_list.append(each[0])
        parameters=remove_duplicate(parameter_list)    #remove duplicate paramerters
    parameter_table[command]=parameters

#根据每个命令，生成字典
commands=read_command().keys()
mml_scripts={}
for command in commands:
    lines=read_command()[command]
    records=[]
    for line in lines:
        x=[x for x in line.split(',')]
        keys = []
        values = []
        for each in x:
            # 此处直接存储数值使用：each=each.split("="), values.append(each[1].strip())
            each=each.split("=")
            keys.append(each[0].strip())
            values.append(each[1].strip())
        line_dic=dict(zip(keys,values))    #每条数据生成字典
        records.append(line_dic)
    print(records)
    mml_scripts[command]=records

print(mml_scripts)
for mml,val in mml_scripts.items():
    print(mml)
    df=pd.DataFrame(val)
    print(df)