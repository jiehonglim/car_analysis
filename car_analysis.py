import pandas as pd
import streamlit as st
import altair as alt

st.title('Annual New Registration of Cars by Make')

#loading LTA's dataset
df_make_by_year = pd.read_csv('Yearly_New_Cars_by_make.csv')

#preparing my select input widget
car_list = df_make_by_year.groupby('make').sum().sort_values(by=['number'], ascending=False).reset_index().drop(['year', 'number'], axis=1)

option = st.selectbox(
     'Which car brand are you interested in ?', car_list)

st.write('You selected:', option)

#refinements and filtering by inputs
chart_data = df_make_by_year[df_make_by_year['make']==option].drop(['make'], axis=1).set_index('year')

#chart it for the win !
st.bar_chart(chart_data)
st.caption('Annual New Registration of Cars by Make 2005 - 2021')

#day 5 using multi select
option2 = st.multiselect(
     'Which car brand are you interested in ?', 
     car_list,
     key='option2'
     )

test_data = df_make_by_year[df_make_by_year['make'].isin(option2)]


c = alt.Chart(test_data).mark_line().encode(
     x='year:Q', y='number:Q', color='make:N', strokeDash='make:N')

st.altair_chart(c, use_container_width=True)
st.caption('Annual New Registration of Cars by Make 2005 - 2021')
