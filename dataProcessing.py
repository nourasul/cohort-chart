from calendar import month
import pandas as pd
import datetime as dt
import plotly.express as px

#read the dataset 
df = pd.read_csv('data.csv') 
# we only want to consider the last 4 columns(InvoiceDate, UnitPrice,CustomerID,Country)no need for the rest 
df = df[df.columns[4:]]
print(df.columns)

#print("Type of date: ",df['InvoiceDate'].dtype)

#convert date type to date& get rid of time 
df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'])
def remove_time(x):
    return dt.datetime(x.year, x.month,1)
df['TransactionMonth'] = df['InvoiceDate'].apply(remove_time)

#group by customerID, because the goal is to measure the retention of each customer throughout the different months.
grouping = df.groupby('CustomerID')['TransactionMonth']
df['CohortMonth']= grouping.transform('min')
print(df)

#extract year,month, and day
def get_date(df,date):
    year= df[date].dt.year 
    month= df[date].dt.month
    day= df[date].dt.day
    return year, month, day

transcation_year, transaction_month, transaction_day= get_date(df,'TransactionMonth')
cohort_year, cohort_month, cohort_day= get_date(df, 'CohortMonth')

year_diff= transcation_year - cohort_year
month_diff= transaction_month - cohort_month

df['CohortIndex']= year_diff * 12 + month_diff + 1 
#after procecing create new csv file
df.to_csv('data2.csv', index = False)

#f=df.dropna(subset=['CustomerID'])
grouping = df.groupby(['CohortMonth', 'CohortIndex'])

#Excludes Null values
cohort_data = grouping['CustomerID'].apply(pd.Series.nunique)
cohort_data = cohort_data.reset_index()
#print('cohort_data= ', cohort_data)


cohort_counts = cohort_data.pivot(index='CohortMonth',columns ='CohortIndex',values = 'CustomerID')
cohort_sizes= cohort_counts.iloc[:,0]
retention = cohort_counts.divide(cohort_sizes, axis=0)
retention = retention.round(3)*100
#print(retention) 
retention.index = retention.index.strftime('%Y-%m')
#print('retention.index:', retention.index)


fig = px.imshow(retention, height = 700, width = 950, text_auto= True, color_continuous_scale = ['white', 'cyan', 'darkblue'])
fig.update_layout(xaxis = dict(side = 'top'),paper_bgcolor = 'white', plot_bgcolor = 'white', coloraxis_showscale=False)

fig.show()