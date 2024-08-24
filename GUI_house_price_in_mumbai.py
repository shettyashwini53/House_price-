import pandas as pd
import streamlit as st
import plotly.express as px
import os
import warnings
import numpy as np
warnings.filterwarnings("ignore")

data= pd.read_csv(r"C:\Users\Ashwini Shetty\Desktop\PyGWalker - Python Data Visualization tool  Streamlit Integration\Mumbai House Prices.csv", delimiter=",", low_memory=True)
data.head(70)

data.shape
data.isnull().sum()

# Remove duplicate rows
data = data.drop_duplicates()

# Reset index after removing duplicates
data.reset_index(drop=True, inplace=True)

data.shape

#####
data["price_unit"].unique()
data["price_unit"]=data["price_unit"].replace({"Cr":10000000,"L":100000})
data["price_unit"].unique()

# Perform element-wise multiplication of the columns
data['price'] = data['price'] * data['price_unit']

# If you want to keep only the merged column and drop the original columns, you can do:
data.drop(['price_unit'], axis=1, inplace=True)
data.head(10)

data.to_excel("MHP.xlsx",index=False)


st.set_page_config(page_title="Home Sweet Home", page_icon="bar chart:", layout="wide")
st.title(" :bar_chart: Mumbai house price") # :bar_chart: side me icon ke liye aata hai
#just to take the title upwards or else by default woh thoda neeche aata hai
st.markdown('<style>div.block-container{padding-top:1rem;}</style>',unsafe_allow_html=True)

fl=st.file_uploader(":file folder: Upload a file",type=(['csv','xlsx']))#can upload a file 
#else if file not uploaded this loop would run
if fl is not None:   
    filename = fl.name
    st.write (filename)
    df= pd.read_csv(filename)
else:
    os.chdir(r"C:\Users\Ashwini Shetty\Desktop\PyGWalker - Python Data Visualization tool  Streamlit Integration")
    df= pd.read_csv("MHP.csv")
 
#########################################################################################################################################

# Sort the DataFrame by the 'cost' column
sorted_df = df.sort_values(by=['price'], ascending=True)

# Get top 10 costliest and least costliest areas
top_10_costliest = sorted_df.tail(5)
top_10_least_costliest = sorted_df.head(6)
# Create a color scale for regions
color_scale1 = px.colors.sequential.Greens

# Plotting for top 10 costliest areas
fig_top_costliest = px.bar(top_10_costliest, x='price', y='region', color='price',
                           color_discrete_sequence=color_scale1, orientation='h',
                           labels={'price': 'Price', 'region': 'Region'},
                           title='Top 10 Costliest Areas by Region')
fig_top_costliest.update_layout(showlegend=False)  # Hide legend

# Create a color scale for regions
color_scale2 = px.colors.sequential.Reds

# Plotting for top 10 least costliest areas
fig_top_least_costliest = px.bar(top_10_least_costliest, x='price', y='region', color='price',
                                 color_discrete_sequence=color_scale2, orientation='h',
                                 labels={'price': 'Price', 'region': 'Region'},
                                 title='Top 10 Least Costliest Areas by Region')
fig_top_least_costliest.update_layout(showlegend=False)  # Hide legend

# Display the plots using Streamlit
st.subheader("Top 5 Costliest Areas by Region")
st.plotly_chart(fig_top_costliest, use_container_width=True)

st.subheader("Top 5 Least Costliest Areas by Region")
st.plotly_chart(fig_top_least_costliest, use_container_width=True)    

#########################################################################################################################################
    
# Displaying two columns for minimum and maximum prices
min_price, max_price = st.columns((2))

# Min and Max price sliders
with min_price:
    min_price_value = st.slider("Minimum Price", float(df["price"].min()), float(df["price"].max()), float(df["price"].min()))

with max_price:
    max_price_value = st.slider("Maximum Price", float(df["price"].min()), float(df["price"].max()), float(df["price"].max()))

# Filtering DataFrame based on selected price range
df = df[(df["price"] >= min_price_value) & (df["price"] <= max_price_value)].copy()

#########################################################################################################################################

# Split the app layout into two columns
col1, col2 = st.columns(2)

st.sidebar.header("Choose your filter :-")

# Create for region 
region= st.sidebar.multiselect("Pick prferred region: ",df['region'].unique())
if not region:
    df2= df.copy()
else:
    df2= df[df["region"].isin(region)]
    
#  Create for  locality
locality= st.sidebar.multiselect("Pick locality:", df2['locality'].unique())
if not locality:
    df2= df.copy()
else:
    df2= df[df["locality"].isin(locality)]
 
 
#Filter based on region and locality
if not region and not locality:
    filtered_df= df
elif region and locality:
    filtered_df = df2[df["region"].isin(region) & df2["locality"].isin(locality)]
elif region:
    filtered_df = df2[df2["region"].isin(region)]
else:
    filtered_df=df2[df2["region"].isin(region) &df2["locality"].isin(locality)]
    
    
Type_df=filtered_df.groupby(by=['Type'], as_index= False)['price'].sum()
bhk_df=filtered_df.groupby(by=['bhk'], as_index= False)['price'].mean()
    
# Create a color scale for regions
color_scale = px.colors.qualitative.Set1
with col1:
    st.subheader("Average price wrt bhk")
    fig =px.bar(bhk_df, x="bhk", y="price", color_discrete_sequence=color_scale, text=['₹{:,.2f}'.format(x) for x in bhk_df["price"]],
                template="seaborn")
    st.plotly_chart(fig,use_container_width= True, height= 2000)
with col2:
    st.subheader("House type wise Price")
    fig= px.pie(Type_df, values= "price", names="Type", hole= 0.6)
    fig.update_traces(text= filtered_df["Type"], textposition= "outside")
    st.plotly_chart(fig, use_container_width= True)
    
    
#########################################################################################################################################
cl1, cl2 = st.columns((2))
with cl1:
    with st.expander("Type_ViewData"):
        Type_df=filtered_df.groupby(by=['Type'], as_index= False)['price'].mean()
        st.write(Type_df.style.background_gradient(cmap="Blues"))
        csv = Type_df.to_csv(index = False)
        st.download_button("Download Data", data = csv, file_name = "Type.csv", mime = "text/csv",
                            help = 'Click here to download the data as a CSV file')

#########################################################################################################################################
with cl2:
    with st.expander("bhk_ViewData"):
        region = filtered_df.groupby(by = "bhk", as_index = False)["price"].mean()
        st.write(bhk_df.style.background_gradient(cmap="Oranges"))
        csv = bhk_df.to_csv(index = False)
        st.download_button("Download Data", data = csv, file_name = "bhk.csv", mime = "text/csv",
                        help = 'Click here to download the data as a CSV file')
        
#########################################################################################################################################
# Create Sunburst chart
fig = px.sunburst(filtered_df, path=['bhk', 'Type'], values='bhk')

st.subheader("Creating a sunbust charts to understand how is the house type with respect to bhk")
# Display Sunburst chart
st.plotly_chart(fig, use_container_width=True)