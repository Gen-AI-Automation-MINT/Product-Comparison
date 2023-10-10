import streamlit as st
import pandas as pd

# input_file = st.file_uploader('Upload your CSV file', type=['xlsx'])
st.set_page_config(page_title='Amazon Walmart URL Generator', page_icon=':smiley:', layout='wide')

input_file = "input_files/input_file_id.xlsx"

if input_file is not None:
    df = pd.read_excel(input_file)
    df.index = range(1, len(df) + 1)
    df['item_id'] = df['item_id'].astype(str)
    df['retailer_id'] = df['retailer_id'].astype(str)
    st.subheader('Input Data')
    st.dataframe(df)
    df['Walmart_Url'] = 'https://www.walmart.com/ip/' + df['item_id'] + '?selected=true'
    df['Comp_Url'] = 'https://www.amazon.com/dp/' + df['retailer_id'] + '?th=1&psc=1'
    st.subheader('Added Urls')
    st.dataframe(df)
    duplicate_WA_id = df[df.duplicated(['item_id'])]
    duplicate_AW_id = df[df.duplicated(['retailer_id'])]
    st.subheader('Duplicate Walmart item_id')
    st.dataframe(duplicate_WA_id)
    st.subheader('Duplicate Amazon retailer_id')
    st.dataframe(duplicate_AW_id)

    st.button('Download', df.to_csv('output_file_id.csv'))
