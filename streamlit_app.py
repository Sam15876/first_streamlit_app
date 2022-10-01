import streamlit as st
import pandas as pd
import requests
import snowflake.connector
from urllib.error import URLError

st.title('My Parents New Healthy Diner')

st.header('🥣 Breakfast Menu')
st.text('🥗 Omega 3 & Blueberry Oatmeal')
st.text('🐔 Kale, Spinarch & Rocket Smoothie')
st.text('🥑🍞 Hard-Boiled Free-Range Egg')

st.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')

# Load fruit list dataset
my_fruit_list = pd.read_csv('https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt')
my_fruit_list = my_fruit_list.set_index('Fruit')

# Let's put a pick list here so they can pick the fruit they want to include 
fruits_selected = st.multiselect('Pick some fruits:', list(my_fruit_list.index), ['Avocado', 'Strawberries'])
fruits_to_show = my_fruit_list.loc[fruits_selected]
# Display the table on the page.
st.dataframe(fruits_to_show)

def get_fruityvice_data(this_fruit_choice):
         fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + fruit_choice)
         fruityvice_normalized = pd.json_normalize(fruityvice_response.json())
         return fruityvice_normalized

# Display FruityVice API Response
st.header('Fruityvice Fruit Advice!')
try:
         fruit_choice = st.text_input('What fruit would you like information about?', 'Kiwi')
         if not fruit_choice:
                  st.error('Please select a fruit to get information.')
         else:
                  st.dataframe(get_fruityvice_data(fruit_choice))
                  
except URLError as e:
         st.error()

st.header("The fruit load list contains:")

def get_fruit_load_list():
         with my_cnx.cursor() as my_cur:
                  my_cur.execute("select * from fruit_load_list")
                  return my_cur.fetchall()

         
         my_data_rows = my_cur.fetchall()
         st.dataframe(my_data_rows)


def insert_row_snowflake(new_fruit):
         with my_cnx.cursor() as my_cur:
                  my_cur.execute("insert into fruit_load_list values('" + new_fruit + "')")
                  return 'Thanks for adding', add_my_fruit
         
add_my_fruit = st.text_input('View Our Fruit List - Add Your Favourites:')
if st.button('Get Fruit Load List'):
         my_cnx = snowflake.connector.connect(**st.secrets["snowflake"])
         st.text(insert_row_snowflake(add_my_fruit))
         my_cnx.close()
