# Import python packages.
import streamlit as st
#from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col
import requests
import pandas as pd

# Write directly to the app.
st.title(f":cup_with_straw: Customize Your Smoothie:cup_with_straw:")
st.write(
  """**Choose the fruits you want in your smoothie!**
  """
)

name_on_order = st.text_input('Name on Smooothie:')
st.write('The name on your Smoothie will be: ',name_on_order)

#session = get_active_session()

conn =st.connection("snowflake")
session = conn.session()

my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'),col('SEARCH_ON'))
#st.dataframe(data=my_dataframe, use_container_width=True)    
#st.stop()

# Convert the snowpark Dataframe to Pandas Dataframe so we can use the LOC function
pd_df=my_dataframe.to_pandas()
st.dataframe(pd_df)
st.stop()

ingredients_list = st.multiselect(
    'Choose up to 5 Ingredients:',
    my_dataframe,
    max_selections = 5)
    

if ingredients_list:
    ingredients_string = ''

    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen + ' '

        #search_on=pd_df.loc[pd_df['FRUIT_NAME'] == fruit_chosen, 'SEARCH_ON'].iloc[0]
        #st.write('The search value for ', fruit_chosen,' is ', search_on, '.')

        st.subheader(fruit_chosen + ' Nutrition Information')
        url = "https://my.smoothiefroot.com/api/fruit/watermelon"
        response = requests.get(url + fruit_chosen)
        sf_df = st.dataframe(data=response.json(),use_container_width=True)
    
    #st.write(ingredients_list)

    my_insert_Stmt = """ insert into smoothies.public.orders (INGREDIENTS,NAME_ON_ORDER) 
    VALUES ('""" + ingredients_string + """','""" + name_on_order + """')"""

    #st.write (my_insert_Stmt)
    #st.stop
    
    time_to_insert = st.button('Submit Order')
    
    if time_to_insert:
        session.sql(my_insert_Stmt).collect()

        st.success('Your Smoothie Is Ordered!')