import sys
sys.path.insert(0, r'C:\Users\mromankiewic\AppData\Local\Programs\Python\Python37\Lib\site-packages')
import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials

#Directory and credentials
scope = ["https://spreadsheets.google.com/feeds",'https://www.googleapis.com/auth/spreadsheets',"https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name(r'N:\Region Management\00 Markets\NORTHERN EUROPE\CP&S\14) Minh\Google drive API\creds.json', scope)
client = gspread.authorize(creds)

from datetime import date

from dateutil.relativedelta import relativedelta

# today = date.today()
# week= "CW"+ str(today.isocalendar()[1])
# monday = date.today() + relativedelta(days=-4)
monday = date.today() + relativedelta(days=+3)
year, week_num, day_of_week = monday.isocalendar()
nextweek = "CW"+ str(week_num)
thisweek = "CW"+ str(week_num-1)
lastweek = "CW"+ str(week_num-2)

path1 = "N:/Region Management/00 Markets/CP&S/Forecast/Logistic Forecast/Forecast tools/Forecasting 2.0/OUTPUT/Temporary/" +\
       str(monday.strftime("%Y%m%d")) + "_Forecasting_FridayInput_"
path2 = "_"+ str(nextweek) + ".xlsx"


#Freeze last week's Tab
worksheet = client.open_by_key("14gYc3XF0SebKq1jD_NKcqjqj5okaBMwjdgZ54NoaP6I").worksheet(lastweek)

cell_list = worksheet.range('A45:CD66')

for cell in cell_list:
    try:
        a = float(str(cell.value).replace(",", ""))
        cell.value = a
    except:
        pass

worksheet.update_cells(cell_list)

#Scrape data
country = ['BE', 'NL', 'DK', 'CH', 'SE', 'NO', 'IE','UK', 'ES', 'FR', 'IT', 'AT', 'DE', 'PL', 'CZ','FI']

data = pd.read_excel(open(path1 + country[0] + path2, "rb"), sheet_name="Input", na_values="NA")

daily = data[4:116]
daily = daily.drop(daily.columns[:13], axis=1)
daily.iloc[:, 0] = country[0]
daily.iloc[0, 0:4] = ["Country", "Year", "Week", "WeekDay"]

# case = data[4:9]
# case = case.drop(case.columns[:22], axis=1)
# case.iloc[:, 0] = country[0]
# case.iloc[0:2, 1] = ["Year", "Month"]

data = data[4:21]
data = data.drop(data.columns[10:], axis=1)
data.iloc[:, 0] = country[0]
data.iloc[0, 0] = "Country"

country = ['BE','NL', 'DK', 'CH', 'SE', 'NO', 'IE','UK', 'ES', 'FR', 'IT', 'AT', 'DE', 'PL', 'CZ', 'FI']

for i in country:
    try:
        df = pd.read_excel(open(path1 + i + path2, "rb"), sheet_name="Input", na_values="NA")
        dai = df[5:116]
        dai = dai.drop(dai.columns[:13], axis=1)
        dai.iloc[:, 0] = i.upper()
        daily = daily.append(dai)
        df = df[5:21]
        df = df.drop(df.columns[10:], axis=1)
        df.iloc[:, 0] = i.upper()
        df = df.fillna(" ")
        data = data.append(df)
    except:
        pass


# Update Forecast and Daily Tabs

data = data.fillna(" ")
daily = daily.fillna(" ")
case = client.open_by_key("14gYc3XF0SebKq1jD_NKcqjqj5okaBMwjdgZ54NoaP6I").worksheet("Forecast")
dailyTab = client.open_by_key("14gYc3XF0SebKq1jD_NKcqjqj5okaBMwjdgZ54NoaP6I").worksheet("DailyFC")
case.update(data.values.tolist())
dailyTab.update(daily.values.tolist())
