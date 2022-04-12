from ast import Div
from numpy import sort
import pandas as pd
import plotly.express as px
import dash
from dash import Input, Output,html,dcc
from dash.exceptions import PreventUpdate

#importing csv into pandas dataframe
#data2 is a file after processing, that was produced by the file "dataProcessing"
#data2 is smaller in size and will make the app run faster.
df= pd.read_csv('data2.csv')


# Initialize the dash app "app"
app = dash.Dash(__name__)

# assign the server variable to the app.server attribute
server = app.server
#the name that will appear in the browser tab 
# app.title= 'Cohort Analysis'

#app layout
app.layout= html.Div([
     #main part of the app
    html.Div([
      #title
        html.Div([
           html.P('Cohort Analysis') 
       ],id= 'title'),
       #deopdown section
    html.Div([
        html.P('Select Country'),
        #Country filter:contires dropdown
        dcc.Dropdown(id= 'countries-Dropdown',
            #Dropdpwn options: All the countries in the dataset
            options= df.sort_values('Country')['Country'].unique(),
            #allow multiple values 
            multi= True,
            #the values selected by default is all the countries
            value= list(df.sort_values('Country')['Country'].unique()),
            #enable search feature in the search bar
            searchable= True,
        )
        ], id= 'dropdown_container',className= 'dropdown_container'),
        #chart section of the app
        html.Div([
            #dcc.Graph component contains the figure
            dcc.Graph(id= 'cohort-chart')], id= 'chartcontainer')
            ], id= 'layout')
]) #End of the layout

#The callback that will connect the dropdown to the chart 
@app.callback(
    Output('cohort-chart', 'figure'),
    Input('countries-Dropdown','value')
)
#Argument refer to the value of component_property in the input,  number of arguments depends on number of inputes
def update_cohort_chart(countries):
        # check if the length of the input is 0 (there is no country selected) there will not be a chart.
    if len(countries) == 0:
        raise PreventUpdate
        # assign the variable df to the data table where the country is in (countries) which is the input from the dropdown
    dff = df[df["Country"].isin(countries) == True]
    grouping = dff.groupby(['CohortMonth', 'CohortIndex'])

    cohort_data = grouping['CustomerID'].apply(pd.Series.nunique)
    cohort_data = cohort_data.reset_index()

    cohort_counts = cohort_data.pivot(index='CohortMonth',
                                    columns ='CohortIndex',
                                    values = 'CustomerID')
    cohort_sizes = cohort_counts.iloc[:,0]

    retention = cohort_counts.divide(cohort_sizes, axis=0)
    retention = retention.round(3)*100
    # make the figure
    fig = px.imshow(retention, 
                    # allow text to appear in the chart
                    text_auto= True, 
                    # set the color scale of the chart
                    color_continuous_scale = ['white', 'cyan', 'darkblue'])
                    # update the layout of the figure

                    # make the x axis appear at the top
    fig.update_layout(xaxis = dict(side = 'top'),
                    # set the color of the background to be white
                    paper_bgcolor = 'white',
                    plot_bgcolor = 'white',
                    # hide the color scale
                    coloraxis_showscale=False)
    # return the fugure, whatever you return from this function is the output of the callback
    return fig

if __name__ == '__main__':
    app.run_server(debug=True)