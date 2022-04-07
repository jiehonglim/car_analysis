import pandas as pd
import streamlit as st
import altair as alt

st.title('Annual New Registration of Cars by Make')

#loading LTA's dataset
df_make_by_year = pd.read_csv('data/Yearly_New_Cars_by_make.csv')

#preparing my select input widget
car_list = df_make_by_year.groupby('make').sum().sort_values(by=['number'], ascending=False).reset_index().drop(['year', 'number'], axis=1)
year_df = df_make_by_year['year'].drop_duplicates()
pivot_chart_data = df_make_by_year.pivot(index='year', columns='make', values='number').fillna(0).diff()
second_last_year_df = pivot_chart_data.iloc[-2:-1]
last_year_df = pivot_chart_data.iloc[-1:]

#using slider bar
start_year, end_year = st.select_slider(
     'Select the year range',
     options=year_df,
     value=(2005,2021)
     )

column_data = df_make_by_year[(df_make_by_year['year'] >= start_year) & (df_make_by_year['year'] <= end_year)]

st.header('Comparing between ' + str(end_year-1) + ' and ' + str(end_year))

row1 = [0]*6
row1 = st.columns(6)

row2 = [0]*6
row2 = st.columns(6)

index_x = 0
for car in car_list['make'].head(12):
     last_two_row = column_data[column_data['make']==car].pivot(index='year', columns='make', values='number').fillna(0).iloc[-2:]

     diff = last_two_row.diff().iat[1,0]
     last_metric = last_two_row.iat[1,0]
     if index_x < 6:
          row1[index_x].metric(label=car, value=last_metric, delta=diff)
     else:
          row2[index_x-6].metric(label=car, value=last_metric, delta=diff)          

     index_x = index_x + 1

#using multi select
multiselect_option = st.multiselect(
     'Which car brand are you interested in ?', 
     car_list,
     key='multiselect_option'
     )

#filter by brand and year
filterbybrand_data = df_make_by_year[df_make_by_year['make'].isin(multiselect_option)]
chart2_data = filterbybrand_data[(filterbybrand_data['year'] >= start_year) & (filterbybrand_data['year'] <= end_year)]

#first chart
st.caption('Annual New Registration of Cars by Make 2005 - 2021')

c = alt.Chart(chart2_data).mark_line().encode(
     x='year:O', y='number:Q', color='make:N', strokeDash='make:N')

st.altair_chart(c, use_container_width=True)

st.write('You selected year between', start_year, 'and', end_year)




#st.dataframe(test_data[(test_data['year'] >= start_year) & (test_data['year'] <= end_year)])