import pandas as pd

header = ['city','year', 'warm_month','cold_month','average_high']

df = pd.read_csv('weather_data', sep = ' {2,}', engine = 'python')

df.to_csv('../Assignment/Input Files/weather.csv', index = False)
