import pymysql.cursors
import pandas as pd
import matplotlib.pyplot as plt

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
        CELLNAME = input("CellName=")
        CELLNAME = CELLNAME.strip().upper()
        StartDate = input("StartDate(\"YYYY-MM-DD\")=")
        StartDate = StartDate.strip()
        sql = (
        "SELECT * FROM `daily_cell_sts_5.2` WHERE Time>= \'" + StartDate + "\'and CELLNAME=\'" + CELLNAME + "\' GROUP BY Time ASC")
        cursor.execute(sql)
        result = cursor.fetchall()
        if not result:
            print("Query result is empty")
except:
    print("Error Occurs when querying")
finally:
    connection.close()

df = pd.DataFrame(result)

KPI = ['RRC Setup Success Rate (CS+PS)(%)', 'RAB CS Assignment Success Rate(%)', 'RAB PS Assignment Success Rate(%)',
       'RRC_Drop_Rate(%)', 'RAB CS Drop Rate(%)', 'RAB_PS_Drop_Rate(%)']

for x in KPI:
    n = KPI.index(x)
    plt.figure(n)
    plt.figure(figsize=(15.0, 5.0), facecolor='whitesmoke')
    ax = plt.subplot(111)
    ax.plot(df['Time'], df[x], 'b-', label=CELLNAME)
    ax.set(title=x)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_color('lightgrey')
    ax.spines['left'].set_color('lightgrey')
    ax.legend(loc='upper right')
    plt.xticks(rotation=90)
plt.show()
