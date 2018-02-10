
# coding: utf-8

# In[ ]:


#按UMTS小区名称进行查询并显示KPI图形
import pymysql.cursors
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np
get_ipython().run_line_magic('matplotlib', 'inline')

connection = pymysql.connect(host='localhost',
                             user='Test',
                             password='1234',
                             db='sts',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)
if connection:
    print("connect to database successfully")
    
try:
    with connection.cursor() as cursor:
        # Read a single record
        CELLNAME=input("CellName=")
        CELLNAME=CELLNAME.strip().upper()
        StartDate=input("StartDate(\"YYYY-MM-DD\")=")
        StartDate=StartDate.strip()
        sql =("SELECT * FROM `daily_cell_sts_5.2` WHERE Time>= \'"+StartDate+"\'and CELLNAME=\'"+CELLNAME+"\' ORDER BY Time ASC")
        cursor.execute(sql)
        result = cursor.fetchall()
        if not result:
            print("Query result is empty")
except:
    print("Error occured when querying")
finally:
    connection.close()

KPI=['RRC Setup Success Rate (CS+PS)(%)',
     'RAB CS Assignment Success Rate(%)',
     'RAB PS Assignment Success Rate(%)',
     'RRC_Drop_Rate(%)',
     'RAB CS Drop Rate(%)',
     'RAB_PS_Drop_Rate(%)',
     'VS.MeanRTWP(dBm)']
  
PS_RAB_FAIL=['VS.RAB.FailEstabPS.Code.Cong',
              'VS.RAB.FailEstabPS.ULCE.Cong',
              'VS.RAB.FailEstabPS.DLCE.Cong',
              'VS.RAB.FailEstabPS.DLIUBBand.Cong',
              'VS.RAB.FailEstabPS.ULIUBBand.Cong',
              'VS.RAB.FailEstabPS.ULPower.Cong',
              'VS.RAB.FailEstabPS.DLPower.Cong',
              'VS.RAB.FailEstabPS.HSUPAUser.Cong',
              'VS.RAB.FailEstabPS.HSDPAUser.Cong',
              'VS.RAB.FailEstabPS.RBIncCfg',
              'VS.RAB.FailEstabPS.RBCfgUnsupp',
              'VS.RAB.FailEstabPS.PhyChFail',
              'VS.RAB.FailEstabPS.UuNoReply',
              'VS.RAB.FailEstabPS.IubFail',
              'VS.RAB.FailEstabPS.SRBReset',
              'VS.RAB.FailEstabPS.CellUpd',
              'VS.RAB.FailEstabPS.TNL']

CS_DROP_CAUSE=['VS.RAB.AbnormRel.CS.RF.SRBReset',
               'VS.RAB.AbnormRel.CS.RF.ULSync',
               'VS.RAB.AbnormRel.CS.RF.UuNoReply',
               'VS.RAB.AbnormRel.CS.OM',
               'VS.RAB.AbnormRel.CS.UTRANgen',
               'VS.RAB.AbnormRel.CS.OLC',
               'VS.RAB.AbnormRel.CS.Preempt',
               'VS.RAB.AbnormRel.CS.Security',
               'VS.RAB.AbnormRel.CS.IuAAL2']

if result:
    df=pd.DataFrame(result)
    fig_number=0
    Time_range=df['Time'].values.tolist()
    for x in KPI:
        fig_number=+1
        plt.figure(fig_number)
        plt.figure(figsize=(12,3.5),facecolor='whitesmoke')
        ax=plt.subplot(111)
        ax.plot(Time_range,df[x],'b-',label=CELLNAME)
        ax.set(title=x)
        ax.xaxis.set_major_locator(mdates.DayLocator(interval=1))  #设置日期间隔为1天
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
        ax.set_xticks(Time_range)   #设置X轴日期显示范围
        ax.spines['top'].set_visible(False)  
        ax.spines['right'].set_visible(False)
        ax.spines['bottom'].set_color('lightgrey')  
        ax.spines['left'].set_color('lightgrey')  
        ax.legend(bbox_to_anchor=(1,1.13),loc='upper right')       
        plt.xticks(rotation=90)

    #PS_RAB_ESTABLISHMENT FAILURE CAUSE   
    fig_number=+1
    plt.figure(fig_number)
    plt.figure(figsize=(12,3.5),facecolor='whitesmoke')
    ax_ps_rab=plt.subplot(111)
    for ps_cause in PS_RAB_FAIL:
        ax_ps_rab.plot(Time_range,df[ps_cause],'-',label=ps_cause)
    ax_ps_rab.set(title='PS RAB Fail Cause-All')
    ax_ps_rab.xaxis.set_major_locator(mdates.DayLocator(interval=1))  #设置日期间隔为1天
    ax_ps_rab.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
    ax_ps_rab.set_xticks(Time_range)   #设置X轴日期显示范围
    ax_ps_rab.spines['top'].set_visible(False)  
    ax_ps_rab.spines['right'].set_visible(False)
    ax_ps_rab.spines['bottom'].set_color('lightgrey')  
    ax_ps_rab.spines['left'].set_color('lightgrey')  
    ax_ps_rab.legend(bbox_to_anchor=(1.02, 1), loc=2, borderaxespad=0.)
    plt.xticks(rotation=90)
    
    #CS ABNORMAL RELEASE CAUSE   
    fig_number=+1
    plt.figure(fig_number)
    plt.figure(figsize=(12,3.5),facecolor='whitesmoke')
    ax_cs_drop=plt.subplot(111)
    for cs_drop_cause in CS_DROP_CAUSE:
        ax_cs_drop.plot(Time_range,df[cs_drop_cause],'-',label=cs_drop_cause)
    ax_cs_drop.set(title='CS Abnormal Release Cause-All')
    ax_cs_drop.xaxis.set_major_locator(mdates.DayLocator(interval=1))  #设置日期间隔为1天
    ax_cs_drop.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
    ax_cs_drop.set_xticks(Time_range)   #设置X轴日期显示范围
    ax_cs_drop.spines['top'].set_visible(False)  
    ax_cs_drop.spines['right'].set_visible(False)
    ax_cs_drop.spines['bottom'].set_color('lightgrey')  
    ax_cs_drop.spines['left'].set_color('lightgrey')  
    ax_cs_drop.legend(bbox_to_anchor=(1.02, 1), loc=2, borderaxespad=0.)
    plt.xticks(rotation=90)
plt.show()



# In[ ]:


#按基站名称进行查询并按扇区显示
import pymysql.cursors
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
get_ipython().run_line_magic('matplotlib', 'inline')

connection = pymysql.connect(host='localhost',
                             user='Test',
                             password='1234',
                             db='sts',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)
if connection:
    print("connect to database successfully")
    
try:
    with connection.cursor() as cursor:
        # Read a single record
        SITENAME=input("Sitename=")
        SITENAME=SITENAME.strip().upper()
        StartDate=input("StartDate(\"YYYY-MM-DD\")=")
        StartDate=StartDate.strip()
        sql =("SELECT * FROM `daily_cell_sts_5.2` WHERE Time>= \'"+StartDate+"\'and CELLNAME LIKE'"+SITENAME+"%\' ORDER BY Time ASC")
        cursor.execute(sql)
        result = cursor.fetchall()
        if not result:
            print("Query result is empty")
except:
    print("Error occured when querying")
finally:
    connection.close()

KPI=['RRC Setup Success Rate (CS+PS)(%)',
    'RAB CS Assignment Success Rate(%)',
    'RAB PS Assignment Success Rate(%)',
    'RRC_Drop_Rate(%)',
    'RAB CS Drop Rate(%)',
    'RAB_PS_Drop_Rate(%)']

if result:
#结果转成DataFrame后增加列Sector，Frequency
    df=pd.DataFrame(result)
    Time_range=df['Time'].values.tolist()
    cn=df.CELLNAME.values.tolist()
    SECTOR=[]
    FREQUENCY=[]
#生成SECTOR和FREQUENCY
    for cell in cn:
        cell=cell.strip()
        sectorname=cell[0:8]+"S"+cell[-1]
        SECTOR.append(sectorname)
        flayer="F"+cell[-2]
        FREQUENCY.append(flayer)
    
    df=df.assign(SECTOR=pd.Series(SECTOR),FREQUENCY=pd.Series(FREQUENCY))

#按SECTOR生成KPI图
    sector_temp=df.SECTOR.values.tolist()
    sector_list=sorted(set(sector_temp),key=sector_temp.index)
    fig_number=0

    for sector in sector_list:
        print(sector)
        df_sector=df[df['SECTOR']==sector]
        cellname_temp=df_sector.CELLNAME.values.tolist()
        cellname_list=sorted(set(cellname_temp),key=cellname_temp.index)   
        for kpi in KPI:
            fig_number=+1
            plt.figure(fig_number)
            plt.figure(figsize=(12,3.5),facecolor='whitesmoke')
            ax=plt.subplot(111)
            for cell in cellname_list:
                df_cell=df_sector[df_sector['CELLNAME']==cell]
                ax.plot(Time_range,df_cell[kpi],'-',label=cell)
            ax.xaxis.set_major_locator(mdates.DayLocator(interval=1))  #设置日期间隔为1天
            ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
            ax.set_xticks(Time_range)
            ax.set(title=kpi)
            ax.spines['top'].set_visible(False)  
            ax.spines['right'].set_visible(False)
            ax.spines['bottom'].set_color('lightgrey')  
            ax.spines['left'].set_color('lightgrey')  
            ax.legend(bbox_to_anchor=(1.02, 1), loc=2, borderaxespad=0.)
            plt.xticks(rotation=90)
            
        plt.show()
    


# In[ ]:


#按LTE小区名称进行查询并显示KPI图形
import pymysql.cursors
import pandas as pd
import matplotlib.pyplot as plt
get_ipython().run_line_magic('matplotlib', 'inline')

connection = pymysql.connect(host='localhost',
                             user='Test',
                             password='1234',
                             db='sts',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)
if connection:
    print("connect to database successfully")
    
try:
    with connection.cursor() as cursor:
        # Read a single record
        CELLNAME=input("CellName=")
        CELLNAME=CELLNAME.strip().upper()
        StartDate=input("StartDate(\"YYYY-MM-DD\")=")
        StartDate=StartDate.strip()
        sql =("SELECT * FROM `daily_cell_lte_5.1` WHERE Time>= \'"+StartDate+"\'and CELLNAME=\'"+CELLNAME+"\' ORDER BY Time ASC")
        cursor.execute(sql)
        result = cursor.fetchall()
        if not result:
            print("Query result is empty")
except:
    print("Error occured when querying")
finally:
    connection.close()

KPI=['L-RRC Setup Success Rate (Service)',
     'L-eRAB Setup Success Rate_ALL',
     'L-RRC Drop Rate',
     'L-RRC Re-Estab Setup Success Rate',
     'L-eRAB Drop Rate_ALL',
     'L-Intra Freq HO_Succ Rate_Preparation_ALL (Intra+Inter eNB)',
     'L-Intra Freq HO_Succ Rate_ALL (Intra+Inter eNB)',
     'L-PRB Utilization DL',
     'L-Average UL Interference']

if result:
    df=pd.DataFrame(result)
    for x in KPI:
        n=KPI.index(x)
        plt.figure(n)
        plt.figure(figsize=(12,3.5),facecolor='whitesmoke')
        ax=plt.subplot(111)
        ax.plot(df['Time'],df[x],'b-',label=CELLNAME)
        ax.set(title=x)
        ax.xaxis.set_major_locator(mdates.DayLocator(interval=1))  #设置日期间隔为1天
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
        ax.set_xticks(Time_range)
        ax.spines['top'].set_visible(False)  
        ax.spines['right'].set_visible(False)
        ax.spines['bottom'].set_color('lightgrey')  
        ax.spines['left'].set_color('lightgrey')  
        ax.legend(loc='upper right')
        plt.xticks(rotation=90)    
    
plt.show()


# In[ ]:


#生成TA或者TP分布图
import pymysql.cursors
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick 
import numpy as np
get_ipython().run_line_magic('matplotlib', 'inline')

connection = pymysql.connect(host='localhost',
                             user='Test',
                             password='1234',
                             db='sts',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)
if connection:
    print("connect to database successfully")
    
try:
    with connection.cursor() as cursor:
        # Read a single record
        CELLNAME=input("CellName=")
        CELLNAME=CELLNAME.strip().upper()
        StartDate=input("StartDate(\"YYYY-MM-DD\")=")
        StartDate=StartDate.strip()
        sql1 =("SELECT * FROM `daily_cell_lte_5.1` WHERE Time>= \'"+StartDate+"\'and CELLNAME=\'"+CELLNAME+"\' ORDER BY Time ASC")
        cursor.execute(sql1)
        result1 = cursor.fetchall()
        sql2 =("SELECT * FROM `daily_cell_sts_5.2` WHERE Time>= \'"+StartDate+"\'and CELLNAME=\'"+CELLNAME+"\' ORDER BY Time ASC")
        cursor.execute(sql2)
        result2 = cursor.fetchall()
        if not result:
            print("Query result is empty")
except:
    print("Error occured when querying")
finally:
    connection.close()
TA=['L-TA_0-156 m',
    'L-TA_156-234 m',
    'L-TA_234-546 m',
    'L-TA_546-1.014 km',
    'L-TA_1.014-1.950 km',
    'L-TA_1.950-3.510 km',
    'L-TA_3.510-6.630 km',
    'L-TA_6.630-14.430 km',
    'L-TA_14.430-30.030 km', 
    'L-TA_30.030-53.430 km',
    'L-TA_53.430-76.830 km', 
    'L-TA_more 76.830 km']
TP=['VS.TP.UE.0',
    'VS.TP.UE.1',
    'VS.TP.UE.2',
    'VS.TP.UE.3',
    'VS.TP.UE.4',
    'VS.TP.UE.5',
    'VS.TP.UE.6.9',
    'VS.TP.UE.10.15(times)',
    'VS.TP.UE.16.25',
    'VS.TP.UE.26.35',
    'VS.TP.UE.36.55',
    'VS.TP.UE.More55']
TP_dis=['0-234 m',
        '234-468 m',
        '468-702 m',
        '702-936 m',
        '0.936-1.17 km',
        '1.17-1.4 km',
        '1.4-2.1 km',
        '2.34-3.74 km',
        '3.74-6.084 km',
        '6.084-8.424 km',
        '8.424-13.1 km',
        '> 13.104 km']

if result1:
    df=pd.DataFrame(result1)
    #生成TA图    
    distance=[]
    bar_width=0.35
    #x轴序列
    km=[x+1 for x in range(12)]
    #值序列
    for ta in TA:
        distance.append(df[ta].values.sum())
    #生成CDF    
    total=sum(distance)
    cdf=np.cumsum([x*100/total for x in distance])
    
    fig_ta=plt.figure(figsize=(9,3.5))
    ax1=fig_ta.add_subplot(111)
    ax1.bar(km,distance,bar_width,color='b',label=CELLNAME+'-TA')
    
    #设置坐标轴间隔为1
    start, end = ax1.get_xlim()
    ax1.xaxis.set_ticks(np.arange(start, end, 1))
    plt.xticks(km,TA,rotation=90)
    
    #设置双坐标轴，右侧Y轴 
    ax2=ax1.twinx()
    ax2.plot(km,cdf,'m-',label=CELLNAME+'-CDF')
    #坐标轴设置为百分比显示
    fmt='%.2f%%' 
    yticks = mtick.FormatStrFormatter(fmt) 
    ax2.yaxis.set_major_formatter(yticks) 

    ax1.legend(loc=1,bbox_to_anchor=(0.98,0.95))
    ax2.legend(loc=1,bbox_to_anchor=(0.98,0.82))
    plt.subplots_adjust(bottom=0.15)
    plt.show()
    
if result2:
    df=pd.DataFrame(result2)
    #生成TA图    
    distance=[]
    bar_width=0.35
    #x轴序列
    km=[x+1 for x in range(12)]
    #值序列
    for tp in TP:
        distance.append(df[tp].values.sum())
    #生成CDF    
    total=sum(distance)
    cdf=np.cumsum([x*100/total for x in distance])
    
    fig_ta=plt.figure(figsize=(9,3.5))
    ax1=fig_ta.add_subplot(111)
    ax1.bar(km,distance,bar_width,color='b',label=CELLNAME+'-TP')
    
    #设置坐标轴间隔为1
    start, end = ax1.get_xlim()
    ax1.xaxis.set_ticks(np.arange(start, end, 1))
    plt.xticks(km,TP_dis,rotation=90)
    
    #设置双坐标轴，右侧Y轴 
    ax2=ax1.twinx()
    ax2.plot(km,cdf,'m-',label=CELLNAME+'-CDF')
    #坐标轴设置为百分比显示
    fmt='%.2f%%' 
    yticks = mtick.FormatStrFormatter(fmt) 
    ax2.yaxis.set_major_formatter(yticks) 

    ax1.legend(loc=1,bbox_to_anchor=(0.98,0.95))
    ax2.legend(loc=1,bbox_to_anchor=(0.98,0.82))
    plt.subplots_adjust(bottom=0.15)
    plt.show()

