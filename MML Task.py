# File: M (Python 3.4)

print('***********************************')
print('NPAmigo')
print('MML Task Result Parse')
print('   * Huawei Internal Use Only *')
print('Huawei MML Task Result Parse')
print('Internal version:  V2.6.1')
print('Author: hongjie@huawei.com')
print('***********************************')
print('\n')
configuration_file_name = 'MMLTaskResultParse_Config.txt'
import sys
import os
import re
import time
import configparser
##定义错误退出方式
def except_exit(print_content_1, print_content_2):
    print(print_content_1, print_content_2)
    print('Press ENTER key to exit!')
    input()
    exit()

config = configparser.ConfigParser()

##打开配置文件
try:
    config.read_file(open('MMLTaskResultParse_Config.ini'))
    print('Successfully open configuration file: MMLTaskResultParse_Config.ini')
except:
    except_exit('Fail to open configuration file:', 'MMLTaskResultParse_Config.ini')
##读取配置文件数据
mml_task_result_filename = config.get('CONFIG', 'mml_task_result_filename')
folder_output = config.get('CONFIG', 'folder_output')
time_filename = time.strftime('%Y%m%d%H%M%S')

##读取MML文件数据
try:
    mml_task_result_file = open(mml_task_result_filename, 'r', errors = 'ignore')
    print('Successfully open MML Task Result file!')
except:
    except_exit('Fail to open MML Task Result file:', mml_task_result_filename)
##获取MML文件名字和扩展名
mml_task_result_file_basename = os.path.basename(mml_task_result_filename)
mml_task_result_file_basename_splitext = os.path.splitext(mml_task_result_file_basename)[0]
##获取文件长度
lines = mml_task_result_file.readlines()
##判断打开文件是否正确
i = 0
while i < len(lines):
    line = lines[i]
    if '//****************MML script file****************' in line:
        print('This is CFGMML file, does not be parsed!')
        print('Press ENTER key to exit!')
        input()
        exit()
    if 'Script Task :' in line and '==========Summary==========' in lines[i + 1]:
        break
    i += 1
##判断完所有行，文件类型不匹配
if i == len(lines):
    print('This file is not a new format MML Task Result file!')
    print('Press ENTER key to exit!')
    input()
    exit()
fail_mml_command_output_file_filename = mml_task_result_file_basename_splitext + '_FailMmlCommand_' + time_filename + '.csv'

##创建输出文件夹
try:
    if not os.path.exists(folder_output):
        os.makedirs(folder_output)
    os.chdir(folder_output)
    print('Successfully change to the output directory:', folder_output)
except:
    except_exit('Can not change to the output directory:', folder_output)

os.chdir(folder_output)

##打开保存记录的excel
try:
    fail_mml_command_output_file = open(fail_mml_command_output_file_filename, 'w')
    print('Successfully open Fail MML Command parse output file', fail_mml_command_output_file_filename)
except:
    except_exit('Can not open Fail MML Command parse output file', fail_mml_command_output_file_filename)

fail_mml_command_output_file.write('MML Command,NE,Report\n')
mml_command = ''
mml_command_group_list = []
mml_command_grp = [
    []]
parameter_name_array = []
parameter_value_array = []
parameter_name_array_1 = []
parameter_value_array_1 = []
parameter_name_array_initial = []
parameter_name_value_array = []
parameter_name_value_array_initial = []
mml_command_sign = 0
first_return_sign = 0
mml_command_fail_succeed = ''
line_former = ''
while i < len(lines):
    line = lines[i]
    if '==========Fail MML Command==========' in line or '==========Failed MML Command==========' in line:
        mml_command_fail_succeed = 'fail'
        i += 1
        continue
    if '==========Succeed MML Command==========' in line or '==========Succeeded MML Command==========' in line:
        mml_command_fail_succeed = 'succeed'
        i += 1
        continue
    if 'MML Command-----' in line:
        if 'No matching result is found' in lines[i + 7] or 'Corresponding results not found.' in lines[i + 7]:
            i += 8
            continue
        if lines[i + 7] == '\n' and mml_command_fail_succeed == 'succeed':
            i += 8
            continue
        mml_command_former = mml_command
        line = line.strip()
        mml_command_array = line.split('-----')
        mml_command = mml_command_array[1]
        mml_command = mml_command.replace('"', '')
        if mml_command_fail_succeed == 'succeed':
            mml_command = re.sub(':.*;', '', mml_command)
        i += 1
        line = lines[i]
        line = line.strip()
        ne_name_array = line.split(' : ')
        ne_name = ne_name_array[1]
        if mml_command_fail_succeed == 'fail':
            i += 1
            line = lines[i]
            line = line.strip()
            if line == 'Report :':
                report = ''
            else:
                report_array = line.split(' : ')
                if '+++' in report_array[1]:
                    i += 3
                    line = lines[i]
                    report = line.strip()
                    report = report.lstrip('RETCODE = ')
                else:
                    report = report_array[1]
            fail_mml_command_output_file.write('"' + mml_command + '",')
            fail_mml_command_output_file.write(ne_name + ',')
            fail_mml_command_output_file.write(report)
            fail_mml_command_output_file.write('\n')
            continue
        if mml_command_fail_succeed == 'succeed':
            i += 1
            line = lines[i]
            line = line.strip()
            report_array = line.split(' : ')
            query_time = report_array[1].split('    ')[3]
            i += 2
            line = lines[i]
            line = line.strip()
            if mml_command == 'DSP BRD':
                if 'Display Board' or 'Board Status' in lines[i + 3]:
                    mml_command = 'DSP BRD_NodeB'
                if 'Board state' in lines[i + 3]:
                    mml_command = 'DSP BRD_RNC'
                
            if mml_command_group_list == []:
                mml_command_grp[0].append(mml_command)
                file_name_parse_output = mml_command + '_parse_' + time_filename + '.csv'
                mml_command_grp[0].append(file_name_parse_output)
                os.chdir(folder_output)
                
                try:
                    file_parse_output = open(file_name_parse_output, 'a')
                    print('Successfully open parse output file', file_name_parse_output)
                except_exit('Can not open parse output file', file_name_parse_output)

            else:
                mml_command_sign = 0
                for mml_command_group in mml_command_group_list:
                    if mml_command in mml_command_group:
                        file_name_parse_output = mml_command_group[1]
                        parameter_name_array = mml_command_group[2]
                        mml_command_sign = 1
                        break
                        continue
                if mml_command_sign == 0:
                    mml_command_grp[0].append(mml_command)
                    file_name_parse_output = mml_command + '_parse_' + time_filename + '.csv'
                    mml_command_grp[0].append(file_name_parse_output)
                    parameter_name_array = []
                if mml_command != mml_command_former:
                    file_parse_output.close()
                    os.chdir(folder_output)
                    
                    try:
                        file_parse_output = open(file_name_parse_output, 'a')
                        print('Successfully open parse output file', file_name_parse_output)
                    except_exit('Can not open parse output file', file_name_parse_output)

                
        
    if ('------' in line or 'ALARM' in line) and 'Fault' in line and 'eNodeB' in line:
        if '=' not in lines[i + 1]:
            if mml_command_sign == 0:
                i += 1
                line = lines[i]
                line = line.replace(',', ';')
                line = re.sub('  +', '  ', line)
                line = line.strip()
                parameter_name_array_initial = line.split('  ')
                if mml_command == 'LST DLGROUP':
                    parameter_name_array = [
                        'DL BB Resource Group No.',
                        'Cabinet No. of DL Process Unit',
                        'Subrack No. of DL Process Unit',
                        'Slot No. of DL Process Unit']
                elif mml_command == 'LST ULGROUP':
                    parameter_name_array = [
                        'UL BB Resource Group No.',
                        'Demodulation Work Mode',
                        'Cabinet No. of UL Process Unit',
                        'Subrack No. of UL Process Unit',
                        'Slot No. of UL Process Unit']
                elif '&' in lines[i + 2]:
                    line_value = lines[i + 2]
                    line_value = re.sub('  +', '  ', line_value)
                    line_value = line_value.strip()
                    parameter_value_array = line_value.split('  ')
                    for j in range(len(parameter_value_array)):
                        parameter_value = parameter_value_array[j]
                        if ':' in parameter_value:
                            parameter_name_array_1 = parameter_value.split('&')
                            for parameter_name_1 in parameter_name_array_1:
                                parameter_name_2 = parameter_name_1.split(':')[0]
                                parameter_name_array.append(parameter_name_2)
                            
                            parameter_name_array_1 = []
                            continue
                        parameter_name_array.append(parameter_name_array_initial[j])
                    
                    parameter_value_array = []
                    parameter_name_array_1 = []
                    j = 0
                else:
                    parameter_name_array = parameter_name_array_initial
                mml_command_grp[0].append(parameter_name_array)
                mml_command_group_list = mml_command_group_list + mml_command_grp
                mml_command_grp = [
                    []]
                file_parse_output.write('Query Time,NE Name,')
                for parameter_name in parameter_name_array:
                    file_parse_output.write(parameter_name + ',')
                
                file_parse_output.write('\n')
                parameter_name_array = []
                i += 2
                line = lines[i]
                line = line.replace(',', ';')
                if mml_command == 'LST DLGROUP':
                    line = line.strip()
                    dl_group_number = line
                    i += 7
                    line = lines[i]
                if mml_command == 'LST ULGROUP':
                    line = re.sub('  +', '  ', line)
                    line = line.strip()
                    ul_group_parameter_value_array = line.split('  ')
                    ul_group_number = ul_group_parameter_value_array[0]
                    demodulatoin_work_mode = ul_group_parameter_value_array[1]
                    i += 7
                    line = lines[i]
                
            else:
                i += 3
                line = lines[i]
                line = line.replace(',', ';')
                if mml_command == 'LST DLGROUP':
                    line = line.strip()
                    dl_group_number = line
                    i += 7
                    line = lines[i]
                if mml_command == 'LST ULGROUP':
                    line = re.sub('  +', '  ', line)
                    line = line.strip()
                    ul_group_parameter_value_array = line.split('  ')
                    ul_group_number = ul_group_parameter_value_array[0]
                    demodulatoin_work_mode = ul_group_parameter_value_array[1]
                    i += 7
                    line = lines[i]
            while 'reports in total' not in line:
                if line == '\n' or '(Number of results' in line:
                    i += 1
                    line = lines[i]
                    line = line.replace(',', ';')
                    continue
                if 'To be continued...' in line:
                    i += 12
                    line = lines[i]
                    line = line.replace(',', ';')
                    continue
                if '---    END' in line:
                    break
                if 'Prompt information' in line:
                    i += 3
                    line = lines[i]
                    line = line.replace(',', ';')
                    continue
                if 'List DLGROUP' in line:
                    i += 4
                    line = lines[i]
                    line = line.strip()
                    dl_group_number = line
                    i += 7
                    line = lines[i]
                if 'List ULGROUP' in line:
                    i += 4
                    line = lines[i]
                    line = re.sub('  +', '  ', line)
                    line = line.strip()
                    ul_group_parameter_value_array = line.split('  ')
                    ul_group_number = ul_group_parameter_value_array[0]
                    demodulatoin_work_mode = ul_group_parameter_value_array[1]
                    i += 7
                    line = lines[i]
                line = re.sub('  +', '  ', line)
                line = line.strip()
                parameter_value_array = line.split('  ')
                file_parse_output.write(query_time + ',' + ne_name + ',')
                if mml_command == 'LST DLGROUP':
                    file_parse_output.write(dl_group_number + ',')
                if mml_command == 'LST ULGROUP':
                    file_parse_output.write(ul_group_number + ',' + demodulatoin_work_mode + ',')
                for j in range(len(parameter_value_array)):
                    parameter_value = parameter_value_array[j]
                    if mml_command == 'DSP BRD_NodeB' or j <= 3:
                        file_parse_output.write(parameter_value + ',')
                    
                    if '::' in parameter_value:
                        parameter_value_array_1 = parameter_value.split('&')
                        for parameter_value_1 in parameter_value_array_1:
                            parameter_value_2 = parameter_value_1.split(':')[1]
                            file_parse_output.write(parameter_value_2 + ',')
                        
                        parameter_value_array_1 = []
                        continue
                    file_parse_output.write(parameter_value + ',')
                
                file_parse_output.write('\n')
                parameter_value_array = []
                i += 1
                line = lines[i]
                line = line.replace(',', ';')
        else:
            i += 1
            line = lines[i]
            line = line.replace(',', ';')
            while 'reports in total' not in line:
                if 'Prompt information' in line:
                    i += 4
                    line = lines[i]
                    line = line.replace(',', ';')
                    continue
                if line == '\n' and '=' not in lines[i + 1]:
                    i += 1
                    line = lines[i]
                    line = line.replace(',', ';')
                    continue
                if 'To be continued...' in line:
                    if mml_command == 'DSP ULOCELL':
                        i += 11
                    else:
                        i += 10
                    line = lines[i]
                    line = line.replace(',', ';')
                    continue
                if 'ALARM' in line and 'Fault' in line and 'eNodeB' in line:
                    i += 1
                    line = lines[i]
                    line = line.replace(',', ';')
                if 'Display Local Cell Status' in line:
                    i += 2
                    line = lines[i]
                if 'Inter-Freq Neighboring Cell Info' in line:
                    i += 3
                    line = lines[i]
                    continue
                if 'List Local Cell Sector Equipment Configuration' in line:
                    i += 5
                    line = lines[i]
                    continue
                if 'Information About the RF module and BBP Serving the Cell' in line:
                    while '(Number of results =' not in line:
                        i += 1
                        line = lines[i]
                    i += 2
                    line = lines[i]
                    continue
                if '---    END' in line:
                    break
                line = line.rstrip()
                parameter_name_value_array_initial = line.split('  =  ')
                parameter_name_value_array_initial[0] = parameter_name_value_array_initial[0].strip()
                if '::' in parameter_name_value_array_initial[1]:
                    parameter_name_value_array = parameter_name_value_array_initial[1].split('::')
                elif re.search('\\d\\d:\\d\\d:\\d\\d', parameter_name_value_array_initial[1]) != None:
                    parameter_name_value_array = parameter_name_value_array_initial
                elif ':' in parameter_name_value_array_initial[1]:
                    parameter_name_value_array = parameter_name_value_array_initial[1].split(':')
                else:
                    parameter_name_value_array = parameter_name_value_array_initial
                if mml_command_sign == 0 and first_return_sign == 0:
                    parameter_name_array.append(parameter_name_value_array[0])
                parameter_value_array.append(parameter_name_value_array[1])
                line_former = line
                i += 1
                line = lines[i]
                line = line.replace(',', ';')
                if 'Cell ID  =  NULL' in line_former:
                    while line != '\n' and '(Number of results' not in line:
                        i += 1
                        line = lines[i]
                line_former = ''
                if not line == '\n':
                    if ('(Number of results' in line or mml_command_sign == 0) and first_return_sign == 0:
                        mml_command_grp[0].append(parameter_name_array)
                        mml_command_group_list = mml_command_group_list + mml_command_grp
                        mml_command_grp = [
                            []]
                        file_parse_output.write('Query Time,NE Name,')
                        for parameter_name in parameter_name_array:
                            file_parse_output.write(parameter_name + ',')
                        
                        file_parse_output.write('\n')
                        parameter_name_array = []
                        first_return_sign = 1
                    file_parse_output.write(query_time + ',' + ne_name + ',')
                    for parameter_value in parameter_value_array:
                        file_parse_output.write(parameter_value + ',')
                    
                file_parse_output.write('\n')
                parameter_value_array = []
                i += 1
                line = lines[i]
                line = line.replace(',', ';')
                continue
            first_return_sign = 0
    i += 1
mml_task_result_file.close()

try:
    fail_mml_command_output_file.close()
except:
    pass


try:
    file_parse_output.close()
except:
    pass

os.chdir(sys.path[0])
print('All Done! Press ENTER key to exit!')
input()
