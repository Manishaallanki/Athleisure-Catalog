# Import python packages
import streamlit as st
from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col;
import pandas as pd

# Write directly to the app
st.title("Athleisure Catalog")
# Get the current credentials
session = get_active_session()
color_data_frame = session.table("ZENAS_ATHLEISURE_DB.products.sweatsuits").select(col('COLOR_OR_STYLE'));
selected_color=st.selectbox('pick a sweatsuit color or style:', color_data_frame);

table_prod_data = session.sql("""select file_name,price,size_list,upsell_product_desc,file_url from catalog_for_website where color_or_style ='"""+selected_color+"""'""")
pd_prod_data = table_prod_data.to_pandas()
file_name = pd_prod_data['FILE_NAME'].iloc[0]
file_url = pd_prod_data['FILE_URL'].iloc[0]
price = '$' + str(pd_prod_data['PRICE'].iloc[0])+'0'
size_list = pd_prod_data['SIZE_LIST'].iloc[0]
upsell = pd_prod_data['UPSELL_PRODUCT_DESC'].iloc[0]
if selected_color:
    st.write(session.sql("""select file_url, from catalog_for_website where color_or_style ='"""+selected_color+"""'"""));
    st.image(image=file_url,width=400,caption='Our warm, comfortable, ' + selected_color + ' sweatsuit!')

    st.markdown('**Price:** '+ price)
    st.markdown('**Sizes Available:** ' + size_list)
    st.markdown('**Also Consider:** ' + upsell)
