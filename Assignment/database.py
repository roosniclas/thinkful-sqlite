import pandas as pd
from sqlalchemy import create_engine
import os
import calendar
import numpy as np
import sys, getopt

engine = create_engine('sqlite:///getting_started.db')

input_folder = 'Input Files/'

for file in os.listdir(input_folder):
    if file.endswith('.csv'):
        df = pd.read_csv(input_folder+file)
        df.to_sql(file.replace('.csv', ''), engine, index = False, if_exists = 'replace')

sql_query = '''
    select city, state, warm_month, cold_month, average_high
    from weather as t1
    left join cities as t2 on t1.city = t2.name '''

df = pd.read_sql_query(sql_query, engine)

def warmest_month(month):
    month = month.capitalize()
    months = [month for month in calendar.month_name[1:]]
    warm_months = df['warm_month'].unique()
    if month in months and month in warm_months:
        filtered_df = df[df['warm_month'] == month]
        sorted_df = filtered_df.sort_values('average_high', ascending = False)
        print(str('The warmest city in '+month+' was '+sorted_df['city'].iloc[0]+', '+sorted_df['state'].iloc[0]+', with an average high of '+str(sorted_df['average_high'].iloc[0])+' degrees'))
        print('Try a different month with: database.py -m <month name>')
    elif month in months and month not in warm_months:
        print(month+' was not one of the warmest months anywhere, please try a different month!')
    elif month not in months:
        print(month+' is not a month! (At least not correctly spelled...)')

def main(argv):
    month = 'July'
    try:
      opts, args = getopt.getopt(argv,"hm:",["month="])
    except getopt.GetoptError:
      print('Usage: database.py -m <month name>')
      sys.exit(2)
    for opt, arg in opts:
      if opt == '-h':
         print('Usage: database.py -m <month name>')
         sys.exit()
      elif opt in ("-m", "--month"):
         month = arg
    warmest_month(month)

if __name__ == "__main__":
   main(sys.argv[1:])
