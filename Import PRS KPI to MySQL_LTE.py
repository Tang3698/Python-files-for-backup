import pymysql.cursors
import tkinter.filedialog
import os
import time

os.chdir(r'D:\Thailand-AIS\KPI\LTE')

def open_file():
    file_names = tkinter.filedialog.askopenfilenames(initialdir=r'D:\Thailand-AIS\KPI\LTE')
    if file_names != '':
        string_filename=""
        for i in range(0, len(file_names)):
            string_filename += str(file_names[i]) + "\n"
        print("The file you choose to process is/are \n"+ string_filename)
    else:
        print("You didn't choose any files!")
    return file_names

connection = pymysql.connect(host='localhost',
                             user='Test',
                             password='1234',
                             db='sts',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)

error_log='execute log_lte_ '+ str(time.time())+'.csv'
error_log_output=open(error_log,'w+')
for file in open_file():
    prs_kpi = open(file, 'r', encoding='utf-8')
    for line in prs_kpi:                  #for line in  f.readlines()[999:len(f.readlines())-1]: 从某一行开始读
        if '2018' in line:
            line=line.strip()
            temp=line.split(',')
            date=temp[0]
            date=date.split('/')
            date=date[2]+'-'+date[0]+'-'+date[1]
            temp[0]='\''+date+'\''
            temp[1] = '\'' + temp[1] + '\''
            temp[3] = '\'' + temp[3] + '\''
            temp[5] = '\'' + temp[5] + '\''
            temp[6] = '\'' + temp[6] + '\''
            temp[7] = '\'' + temp[7] + '\''
            for x in range(len(temp)):
                if temp[x]=='/0':
                    temp[x]='NULL'
                if temp[x]=='NIL':
                    temp[x]='NULL'
            new_line=','.join(temp)

            sql_line="INSERT INTO `daily_cell_lte_5.1` VALUES " + '('+new_line+')'+';'
            try:
                connection.cursor().execute(sql_line)
                connection.commit()
                print(sql_line)
            except:
                error_log_output.write(sql_line+'\n')
                continue
    prs_kpi.close()
connection.close()
error_log_output.close()