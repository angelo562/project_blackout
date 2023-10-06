import pandas as pd
from openpyxl import load_workbook
from openpyxl.styles import PatternFill
import os
import datetime as dt
from datetime import timedelta as td


"""Shift Admin Buddy.  Designed to give schedule stats

input: Group Shift stats in excel format
output: Excel format?

Shift Admin buddy as a Class()

Sheet with Holiday stats, for last 2 years starting fiscal 4th quarter, 10/1

Include Major holidays, minor holidays, weekends, nights

"""

class ShiftAdminBuddy:

    def __init__(self):
        self.holidays = True
        self.weekends = False
        self.path = self.return_path()
        self.datelist = self.get_datelist_asstring()
        self.df = self.get_and_clean_df()
        self.df = self.compile_df_to_analyze()
        self.fxn_list = self.collect_fxns()
        self.beg_date = self.df.Date.min().strftime('%Y-%m-%d')
        self.end_date = (self.df.Date.max()+ td(days=1)).strftime('%Y-%m-%d')

    def return_path(self):

        # inp1 = input(f"Please input location path of group shift stats: ")

        inp1 = r"C:\Users\Angel\Downloads\group_stats_detailed_164259_90sxeijc97.xlsx"

        path1 = os.path.abspath(inp1.strip(' \"'))
        return fr"{path1}"
    
        # GROUP OF FXNS returning dates

    def get_thanksgiving_date(self,year):
        # Start with November 1st of the given year
        date = dt.date(year, 11, 1)

        # Find the first Thursday
        while date.weekday() != 3:  # Thursday is represented by 3
            date += dt.timedelta(days=1)
        # Add three weeks to get to the fourth Thursday (Thanksgiving)
        date += dt.timedelta(weeks=3)

        return date

    def get_thanksgiving_eve_date(self,year):
        date = self.get_thanksgiving_date(year) 
        date -= dt.timedelta(days=1)
        return date

    def get_christmas_eve_date(self, year):
        # Add year to 12-24 
        return dt.date(year, 12, 24)

    def get_christmas_date(self, year):
        # Add year to 12-25
        return dt.date(year, 12,25)

    def get_new_years_eve_date(self,year):
        return dt.date(year, 12,31)

    def get_new_years_date(self,year):
        # returns the NEXT year 
        year += 1
        return dt.date(year, 1, 1)
        
    def get_mothers_day_date(self, year):

        date = dt.date(year, 5, 1)
        #first Sunday in may as 6
        while date.weekday() != 6:
            date += dt.timedelta(days=1)
        # add one week to get to 2nd sunday in may
        date += dt.timedelta(weeks=1)
        return date

    def get_halloween_date(self, year):
        return dt.date(year, 10, 31)

    minor_holiday_fxns = [
        get_mothers_day_date,
        get_halloween_date,
    ]

    major_holiday_fxns = [
        get_thanksgiving_date,
        get_thanksgiving_eve_date,
        get_christmas_eve_date,
        get_christmas_date,
        get_new_years_eve_date,
        get_new_years_date,
    ]

    # collect what fxns to run
    def collect_fxns(self):

        holiday_list_fxns = []
        major_h = True
        minor_h = True

        if major_h:
            holiday_list_fxns +=  self.major_holiday_fxns

        if minor_h:
            holiday_list_fxns +=  self.minor_holiday_fxns
        return holiday_list_fxns

    def get_and_clean_df(self):

        df = pd.read_excel(self.path , header=1)

        df = df.query('not Date.isna()').reset_index(drop=True)  

        df = df.rename(columns={
            'Work Hrs' : 'Work_hrs',
            'Sched Hrs': 'Scheduled_hrs',
            })

        #change Date to datetime dtype
        df.Date = pd.to_datetime(df.Date)       
        
        #Ensure df.Time is a str
        df['Time'] = df['Time'].astype(str)     
        #Format Provider names to be title()
        df.Provider = df.Provider.str.title().astype(str)    

        return df

    def compile_df_to_analyze(self):

        def concat_df(df_1, df_2):
            return  pd.concat([df_1, df_2], axis= 0)

        def query_df(date):
            date = date
            return self.df.query('Date == @date')

        df = query_df(self.datelist[0])
        for date in self.datelist[1:]:
            df = concat_df(df, query_df(date))
        return df
    
    def get_datelist_asstring(self, fxn_list= None, year= 2022):
        if self.holidays:
            if fxn_list is None:
                fxn_list = self.collect_fxns()

            date_list_asstring=[]
            for fxn in fxn_list:
                date_list_asstring.append(fxn(self,year).strftime('%Y-%m-%d'))
            return date_list_asstring

    def count_holidays(self):
        self.holidays = True
        self.weekends = False

        df_c = self.df.sort_values(by='Provider')\
        .reset_index(drop=True)\
        .Provider.value_counts()

        print(df_c)
        return df_c

    def count_weekends(self):
        self.holidays = False
        self.weekends = True

        

sab = ShiftAdminBuddy()

# "C:\Users\Angel\Downloads\group_stats_detailed_164259_90sxeijc97.xlsx"
# print(sab.path)
# sab.df.info()
# sab.count_holidays()
print(sab.end_date)
print(sab.beg_date)