import sys
sys.path.insert(0, r'C:\Users\mromankiewic\AppData\Local\Programs\Python\Python37\Lib\site-packages')
sys.path.insert(0, r'C:\Users\mromankiewic\AppData\Local\Programs\Python\Python37\Lib\site-packages\win32\lib')
sys.path.insert(0, r'C:\Users\mromankiewic\AppData\Local\Programs\Python\Python37\Lib\site-packages\win32')
import xlwings as xw
import pandas as pd
from datetime import date
from dateutil.relativedelta import relativedelta


# today = date.today()
# week= "CW"+ str(today.isocalendar()[1])
# monday = date.today() + relativedelta(days=-4)
monday = date.today() + relativedelta(days=-7)
year, week_num, day_of_week = monday.isocalendar()
thisweek = "CW"+ str(week_num)
a = " "


path1 = "N:/Region Management/00 Markets/CP&S/Forecast/Financial Forecast/Weekly Financial FC/2020/" +\
        "2020" + a + str(thisweek) + "/" +\
        str(monday.strftime("%Y%m%d")) + a + "Weekly Financial Forecast" + a +"CW" + a + str(week_num) + a

path0 = "N:/Region Management/00 Markets/CP&S/Forecast/Financial Forecast/Weekly Financial FC/2020/" + \
        "2020" + a + str(thisweek) + "/" + \
        "2020" + a + "Master Case" + a + str(thisweek) + ".xlsm"


app1 = xw.App(visible=False)
app1.screen_updating=False
app1.ignore_read_only_recommended=True
app1.display_alerts=False
app1.calculation = 'manual'

#Delete existing sheets
wb0 = app1.books.open(path0)
ws0 = wb0.sheets("II")
ws01 = wb0.sheets["DE", "AT", "CH", "BE", "NL", "PL", "ES", "FR", "IT", "SE", "FI", "DK", "NO", "UK", "IE", "CZ"]
ws01.delete()


#OPEN WORKBOOKS
wb1 = app1.books.open(path1 + "DE" + ".xlsx")
wb2 = app1.books.open(path1 + "AT" + ".xlsx")
wb3 = app1.books.open(path1 + "BE" + ".xlsx")
wb4 = app1.books.open(path1 + "PL" + ".xlsx")
wb5 = app1.books.open(path1 + "ES" + ".xlsx")
wb6 = app1.books.open(path1 + "FR" + ".xlsx")
wb7 = app1.books.open(path1 + "IT" + ".xlsx")
wb8 = app1.books.open(path1 + "SE" + ".xlsx")
wb9 = app1.books.open(path1 + "UK" + ".xlsx")
wb10 = app1.books.open(path1 + "CZ" + ".xlsx")


#COPY sheets
ws1 = wb1.sheets["DE"]
ws1.api.Copy(Before=ws0.api)
wb1.app.quit()

ws2 = wb2.sheets["AT", "CH"]
ws2.api.Copy(Before=ws0.api)
wb2.app.quit()

ws3 = wb3.sheets["BE", "NL"]
ws3.api.Copy(Before=ws0.api)
wb3.app.quit()

ws4 = wb4.sheets["PL"]
ws4.api.Copy(Before=ws0.api)
wb4.app.quit()

ws5 = wb5.sheets["ES"]
ws5.api.Copy(Before=ws0.api)
wb5.app.quit()

ws6 = wb6.sheets["FR"]
ws6.api.Copy(Before=ws0.api)
wb6.app.quit()

ws7 = wb7.sheets["IT"]
ws7.api.Copy(Before=ws0.api)
wb7.app.quit()

ws8 = wb8.sheets["SE", "FI", "DK", "NO"]
ws8.api.Copy(Before=ws0.api)
wb8.app.quit()

ws9 = wb9.sheets["UK", "IE"]
ws9.api.Copy(Before=ws0.api)
wb9.app.quit()

ws10 = wb10.sheets["CZ"]
ws10.api.Copy(Before=ws0.api)
wb10.app.quit()

#Close
app1.screen_updating=True
app1.display_alerts =True
app1.calculation = 'automatic'
wb0.save()
wb0.app.quit()
app1.quit()
