#from datat_retrival import *
#import seaborn as sns
#import matplotlib.pyplot as plt

import streamlit as st 
import pymongo
import streamlit as st
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from decimal import Decimal
from bson import Decimal128
import pandas as pd
import plotly.express as px
import geojson
import json
import plotly.graph_objects as go
import plotly.graph_objects as go
import plotly.figure_factory as ff


st.set_page_config(page_title="Airbn",layout="wide")
st.title("Airbn Data Analysis")
#st.markdown("<style>div.block-container {padding-top: 1rem;}</style>", unsafe_allow_html=True)
 

 #==================================== setting the connection  and getting the records =========================================================
database ="sample_airbnb"
collection ="listingsAndReviews"
uri = "mongodb+srv://mohan:mohan@cluster0.rochv2v.mongodb.net/?retryWrites=true&w=majority"

def connection_db(uri):
    client = MongoClient(uri, server_api=ServerApi('1'))
    try:
        client.admin.command('ping')
        print("Pinged your deployment. You successfully connected to MongoDB!")
    except Exception as e:
           print(e)
 


def retrive_records(uri,database,collection):
    client = MongoClient(uri)
    print("client successfull")
    db = client[database]
    print("database connection successfull")
    col = db[collection]
    print("database collection connection successfull")
    record = col.find()
    print("records collected")
    
    return record


def data_retrival(record):
    Total_entry =[]
    for a in record:
        ID = a.get("_id",None)
        Name = a.get("name",None)
        property_type =a.get("property_type",None)
        room_type = a.get("room_type",None)
        Red_type =a.get("bed_type",None)
        min_nights=a.get("minimum_nights",None)
        max_nights=a.get("maximum_nights",None)
        cancellation_policy =a.get("cancellation_policy",None)
        accommodate = a.get("accommodates",None)
        bedrooms = a.get("bedrooms",None)
        beds = a.get("beds",None)
        total_reviews = a.get("number_of_reviews",None)
        bathrooms = a.get("bathrooms",None)
        amenities = len(a.get("amenities",0))
        
        
        #1
        security_depo = a.get("security_deposit",None)
        if security_depo is None:
            security_deposit = None
        else:
            security_deposit =Decimal(str(security_depo))
        
        #2
        clean_fee =a.get("cleaning_fee",0)
        clean_fee  =int(Decimal(str(clean_fee )))
        
        #3
        extra_people=a.get("extra_people",None)
        if extra_people is None:
            extra_people =None
            
        else:
            extra_people =Decimal(str(extra_people))
        
        #4
        guests = a.get("guests_included",None)
        guests = int(Decimal(str(guests)))
        
        #5
        host = a.get("host",None)
        host_id = host.get("host_id",None)
        host_name = host.get ("host_name",None)
        host_response_rate =  host.get("host_response_rate",None)
        
        #6
        coun =a.get("address",None)
        country_code =coun.get("country_code",None)
        country=coun.get("country",None)
        location = coun.get("location",None)
        coordiantes = location.get("coordinates",None)
        if len(coordiantes) == 0:
            latitude = 0
            longitude = 0
        else:
            latitude = coordiantes[0]
            longitude = coordiantes[1]
        
        #7
        avail= a.get("availability",None)
        avail_30 = avail.get("availability_30",None)
        avail_60 = avail.get("availability_60",None)
        avail_90 = avail.get("availability_90",None)
        avail_365= avail.get("availability_365",None)
        
        #8
        review = a.get("review_scores",None)
        review_scores_accuracy =review.get("review_scores_accuracy",None)
        review_scores_cleanliness=review.get("review_scores_cleanliness",None)
        review_scores_checkin=review.get("review_scores_checkin",None)
        review_scores_communication=review.get("review_scores_communication",None)
        review_scores_location=review.get("review_scores_location",None)
        review_scores_value=review.get("review_scores_value",None)
        review_scores_rating=review.get("review_scores_rating",None)
        
        
        each_entry = each_entry = {
            "ID": ID,
            "Name": Name,
            "property_type": property_type,
            "room_type": room_type,
            "min_nights": min_nights,
            "max_nights": max_nights,
            "cancellation_policy": cancellation_policy,
            "accommodate": accommodate,
            "bedrooms": bedrooms,
            "beds": beds,
            "total_reviews": total_reviews,
            "bathrooms": bathrooms,
            "amenities": amenities,
            "security_deposit": security_deposit,
            "clean_fee": clean_fee,
            "extra_people": extra_people,
            "guests": guests,
            "host_id": host_id,
            "host_name": host_name,
            "host_response_rate": host_response_rate,
            "country_code": country_code,
            "country": country,
            "coordiantes":coordiantes,
            "latitude":latitude ,
            "longitude":longitude,
            "avail_30": avail_30,
            "avail_60": avail_60,
            "avail_90": avail_90,
            "avail_365": avail_365,
            "review_scores_accuracy": review_scores_accuracy,
            "review_scores_cleanliness": review_scores_cleanliness,
            "review_scores_checkin": review_scores_checkin,
            "review_scores_communication": review_scores_communication,
            "review_scores_location": review_scores_location,
            "review_scores_value": review_scores_value,
            "review_scores_rating": review_scores_rating
        }
        Total_entry.append(each_entry)   
        
    return Total_entry

@st.cache_data
def records(uri,database,collection):
    try:
        connection_db(uri)
       # having the collection of records
        try:
            records = retrive_records(uri,database,collection)
            #Getting the fileds of each records
            fileds = data_retrival(records)
            return fileds
        except Exception as e:
            print(e)
            st.warning("Collection is not available !!!")   
    except Exception as e:
        print(e)
        st.warning("Problem in Database connection !!!")
        
        
def data_type_conv(x):
    value  = int(Decimal(str(x)))
    return value




# =================================== Function to retrive data from database ==========================================================

data = records(uri,database,collection)


df_raw = pd.DataFrame(data)
#st.write(df_raw)

def data_type_conv(x):
    value  = int(Decimal(str(x)))
    return value

# =================================== Preprocessing the data ===============================================================================

def preprocess(df):
    df = df.dropna()
    df = df.reset_index(drop=True)
    convert_dict = {
    "security_deposit":int,
    "extra_people":int
    }
    df[["security_deposit","extra_people"]] = df[["security_deposit","extra_people"]].astype(convert_dict)
    df[["bedrooms","beds","bathrooms","host_response_rate","review_scores_accuracy","review_scores_cleanliness","review_scores_checkin","review_scores_communication","review_scores_location","review_scores_value","review_scores_rating"]]= df[["bedrooms","beds","bathrooms","host_response_rate","review_scores_accuracy","review_scores_cleanliness","review_scores_checkin","review_scores_communication","review_scores_location","review_scores_value","review_scores_rating"]].apply(lambda col: col.apply(data_type_conv))
    out1=pd.DataFrame(df[["country","property_type","room_type","cancellation_policy","accommodate","guests","extra_people","bedrooms","bathrooms","max_nights","min_nights","review_scores_accuracy","security_deposit","latitude","longitude","coordiantes","country_code"]])
    return out1

df_cleaned = preprocess(df_raw)
#st.write(df_cleaned)


# =================== Country ========================================

location_c = len(df_cleaned["country"].unique())
#st.sidebar.header("Filter Countries")
location = st.sidebar.multiselect(
    label=f" out of  {location_c}  Countries ",
    options=df_cleaned["country"].unique(),
    default=["Canada"],key="country_multiselect")

# =========================================== Query the dataframe ======================================================= 

try:
    
    location_selection = df_cleaned.query("country==@location")
    
    
    # ========================== Review =============================================
    review_c = len(location_selection["review_scores_accuracy"].unique())
    st.sidebar.header("Filter based on review")
    review = st.sidebar.multiselect(label=f" out of  {review_c} review",
                                    options=location_selection["review_scores_accuracy"].unique(),
                                    default=location_selection["review_scores_accuracy"].unique(),key="review_multiselect")
    
    review_selection =  location_selection.query("review_scores_accuracy==@review")
    
    
    
    # ========================== Property_type ==================================
    property_c = len(review_selection["property_type"].unique())
    st.sidebar.header("Filter based on property type")
   
    property = st.sidebar.multiselect(
        label=f" out of  {property_c} review",
        options=review_selection["property_type"].unique(),
        default=review_selection["property_type"].unique(),key="property_type")
    
    
    property_selection =  review_selection.query("property_type==@property")
    
    
    # ========================== Room_type ==================================
    Room_c = len(property_selection["room_type"].unique())
    st.sidebar.header("Filter based on room type")

    Room = st.sidebar.multiselect(
        label=f" out of  {Room_c} review",
        options=property_selection["room_type"].unique(),
        default=property_selection["room_type"].unique(),key="room_type")
    
    Room_selection = property_selection.query("room_type ==@Room")
    df_selection = Room_selection.reindex()
    


# ================================== Ploting the Graphs  ==========================================================

    df = df_selection[(df_selection["extra_people"] != 0) & (df_selection["accommodate"] != 0) &(df_selection["bedrooms"] != 0)&(df_selection["bathrooms"] != 0)&(df_selection["max_nights"] != 0)&(df_selection["max_nights"] != 2147483647)&(df_selection["max_nights"] != "2147483647")&(df_selection["min_nights"] != 1234567890)&(df_selection["security_deposit"] != 0)]
    df['max_nights'] = pd.to_numeric(df['max_nights'], errors='coerce')

    with st.expander("Tabular"):
                st.write(df)
#------------------------------------- property plot ----------------------------------------------------------------- 
    col1,col2 = st.columns(2)
    with col1: 
        
        fig = px.histogram(df_selection, x='property_type',color="country",barmode="group",title="Count of Property Types in Each Country")
        fig.update_layout(xaxis_title="Property Type")
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:    
        # plotly plot for room types
        fig = px.histogram(df_selection, x='room_type',color="country",barmode="group",title="Count of Room Types in Each Country")
        fig.update_layout(xaxis_title="Room Type")
        st.plotly_chart(fig, use_container_width=True)   
        
                
# ------------------------------------------------------------- Accomodation  and Extra people ----------------------------------------------------          

   
    col7,col8 = st.columns(2)
    with col7:
        
        fig = px.sunburst(df, path=['property_type', 'room_type'], values='review_scores_accuracy',color='review_scores_accuracy',color_continuous_scale='inferno')
        fig.update_layout(title_text="Relation of Room Types based in each Property  on Review Scores Accuracy")
        st.plotly_chart(fig)
        
        
        
        fig = px.histogram(df, x='room_type',y ="accommodate" ,color="property_type",title="Total Accommodation in the Each Room Types based on Property types")
        fig.update_layout(xaxis_title="Room Type", yaxis_title="Accommodate")
        st.plotly_chart(fig, use_container_width=True) 
    
   
        
        
        
        fig = px.scatter(df, x="accommodate", y="extra_people", color="property_type",
                size='extra_people', hover_data=['room_type'])
        fig.update_layout(title_text="Relation Between Accommodation vs.  Extra People")
        fig.update_layout(xaxis_title="Accommodate", yaxis_title="Extra People")
        st.plotly_chart(fig)
        
    
        
        # --------------------------------------------------------------------- Accommodation vs Guests ---------------------------------------------------------------------------------------------
        
        fig = px.scatter(df, x="accommodate", y="guests", color="property_type",
                size='guests', hover_data=['room_type'])
        fig.update_layout(title_text="Relation Between Accommodation vs. Guests",xaxis_title="Accommodate", yaxis_title="Guests")
        st.plotly_chart(fig)
    
        
        
        
        # -------------------------------------------------------------------------------- Accommodation vs Bedrooms -------------------------------------------------------------------------------
        fig = px.scatter(df, x="accommodate", y="bedrooms", color="property_type",
                size='bedrooms', hover_data=['room_type'])
        fig.update_layout(title_text="Relation Between Accommodation vs. Bedrooms",xaxis_title="Accommodate", yaxis_title="Bedrooms")
        st.plotly_chart(fig)
        
    
        
        # ------------------------------------------------------------------------ Accommodation vs Bathrooms ----------------------------------------------------------------------------------
        
        fig = px.scatter(df, x="accommodate", y="bathrooms", color="property_type",
                size='bathrooms', hover_data=['room_type'])
        fig.update_layout(title_text="Relation Between Accommodation vs. Bathrooms",xaxis_title="Accommodate", yaxis_title="Bathrooms")
        st.plotly_chart(fig)
        
        
        # ------------------------------------------------------------------- Extra People  ------------------------------------------------------------------------------
        
        fig = px.scatter(df, x="extra_people", y="security_deposit", color="property_type",
                size='security_deposit', hover_data=['room_type'])
        fig.update_layout(title_text="Relation Between  Extra People vs. Security_deposit",xaxis_title="Extra People", yaxis_title="Security Deposit")
        st.plotly_chart(fig)
        
        fig = px.scatter(df, x="extra_people", y="max_nights", color="property_type",
                size='max_nights', hover_data=['room_type'])
        fig.update_layout(title_text="Relation Between  Extra People vs. max_nights",xaxis_title="Extra People", yaxis_title="Max Nights")
        st.plotly_chart(fig)
        
        
        fig = px.scatter(df, x="extra_people", y="bedrooms", color="property_type",
                size='max_nights', hover_data=['room_type'])
        fig.update_layout(title_text="Relation Between  Extra People vs. Bedrooms",xaxis_title="Extra People", yaxis_title="Bedrooms")
        st.plotly_chart(fig)
        
        fig = px.scatter(df, x="extra_people", y="bathrooms", color="property_type",
                size='max_nights', hover_data=['room_type'])
        fig.update_layout(title_text="Relation Between  Extra People vs. bathrooms",xaxis_title="Extra People", yaxis_title="Bathrooms")
        st.plotly_chart(fig)
        # ------------------------------------------------------------------- Nights --------------------------------------------------------------------------------------

        fig = px.histogram(df, x='property_type',y ="min_nights" ,color="min_nights",barmode="group",title="Total no.of. Minimum nights based on  Property",hover_data=["room_type"])
        fig.update_layout(xaxis_title="Property Type", yaxis_title="Minimum Nights")
        st.plotly_chart(fig, use_container_width=True)
        
        fig = px.histogram(df, x='property_type',y ="max_nights" ,color="max_nights",barmode="group",title="Total no.of. Maximum nights in the Property",hover_data=["room_type"])
        fig.update_layout(xaxis_title="Property Type", yaxis_title="Maximum Nights")
        st.plotly_chart(fig, use_container_width=True)
        
        fig = px.histogram(df, x='property_type',y ="security_deposit" ,color="property_type",barmode="group",title=" Total Deposit amount for each  Property")
        fig.update_layout(xaxis_title="Property Type", yaxis_title="Security Deposit")
        st.plotly_chart(fig, use_container_width=True)
        
    #================================================================================ Heat map ===============================================================================================================      
        df2 = df.groupby(['property_type', 'room_type']).size().reset_index(name='count')
        heatmap_data =  df2.pivot(index='room_type', columns='property_type', values='count')
        fig = px.imshow(heatmap_data, text_auto=True,color_continuous_scale='RdBu_r')
        fig.update_layout(title='Heatmap Map for Property Types vs. Room Types')
        st.plotly_chart(fig, use_container_width=True)
        
        df2 = df.groupby(['property_type', 'cancellation_policy']).size().reset_index(name='count')
        heatmap_data =  df2.pivot(index='cancellation_policy', columns='property_type', values='count')
        fig = px.imshow(heatmap_data, text_auto=True,color_continuous_scale='RdBu_r')
        fig.update_layout(
            title='Heatmap Map for Property Types vs. cancellation_policy')
        st.plotly_chart(fig, use_container_width=True)
        
            
        
        df3 = df.groupby(['property_type', 'room_type', 'cancellation_policy']).size().reset_index(name='count')
        df1 = df3.drop_duplicates(subset=['room_type', 'property_type', 'cancellation_policy'], keep='first')
        fig = px.scatter(df1, x='room_type', y='count', color='cancellation_policy', facet_col='property_type',
                 category_orders={'room_type': df1['room_type'].unique()})
        fig.update_layout( xaxis=dict(tickangle=45), showlegend=True,title="Cancellation Policy in Property type and Room type")
        st.plotly_chart(fig, use_container_width=True)
        
        df3 = df.groupby(['property_type', 'room_type', 'security_deposit']).size().reset_index(name='count')
        df1 = df3.drop_duplicates(subset=['room_type', 'property_type', 'security_deposit'], keep='first')
        fig = px.scatter(df1, x='room_type', y='count', color='security_deposit', facet_col='property_type',
                 category_orders={'room_type': df1['room_type'].unique()},color_continuous_scale="rdylbu")
        fig.update_layout( xaxis=dict(tickangle=45), showlegend=True,title="Security Deposit  in Property type and Room type")
        st.plotly_chart(fig, use_container_width=True)
        
        
        df3 = df.groupby(['property_type', 'room_type', 'security_deposit',"review_scores_accuracy"]).size().reset_index(name='count')
        df1 = df3.drop_duplicates(subset=['room_type', 'property_type', 'security_deposit',"review_scores_accuracy"], keep='first')
        fig = px.scatter(df1, x='room_type', y='count', color='security_deposit', facet_col='property_type',
                 category_orders={'room_type': df1['room_type'].unique()},color_continuous_scale="rdylbu",hover_data="review_scores_accuracy")
        fig.update_layout( xaxis=dict(tickangle=45), showlegend=True,title="Security Deposit  in Property type and Room type")
        st.plotly_chart(fig, use_container_width=True)
        

    with col8:
        # ----------------------------------------------------------  Extra People vs Security_deposit --------------------------------------------------------------------------------------------
        
        fig = px.sunburst(df, path=['room_type','property_type'], values='review_scores_accuracy',color='review_scores_accuracy',color_continuous_scale="armyrose")
        fig.update_layout(title_text="Relation of Property Types in each Room Types  based on Review Scores Accuracy")
        st.plotly_chart(fig)
        
        fig = px.histogram(df, x='room_type',y ="extra_people" ,color="property_type",title=" Extra people in each Rooms Types")
        fig.update_layout(xaxis_title="Room Type")
        st.plotly_chart(fig, use_container_width=True)
        
        
        #+c------------------------------------------------------------------  Grouping  based on Accommodation-----------------------------------------------------------
        fig = px.histogram(df, x='accommodate',y ="extra_people" ,color="property_type",barmode="group",title=" Grouping Accommodation based on  Extra People in each Property")
        fig.update_layout(xaxis_title="Accimmodate", yaxis_title="Extra People")
        st.plotly_chart(fig)
        
        fig = px.histogram(df, x='accommodate',y ="guests" ,color="property_type",barmode="group",title=" Grouping Accommodation based on  Guests in each Property")
        fig.update_layout(xaxis_title="Accomadate", yaxis_title="Extra People")
        st.plotly_chart(fig)
        
        
        fig = px.histogram(df, x='accommodate',y ="bedrooms" ,color="property_type",barmode="group",title=" Grouping Accommodation based on  Bedrooms in each Property")
        fig.update_layout(xaxis_title="Accomadate", yaxis_title="Bedrooms")
        st.plotly_chart(fig)
        
        fig = px.histogram(df, x='accommodate',y ="bathrooms" ,color="property_type",barmode="group",title=" Grouping Accommodation based on  Bathrooms in each Property")
        fig.update_layout(xaxis_title="Accomadate", yaxis_title="Bathrooms")
        st.plotly_chart(fig)
        
            
        
        # ------------------------------------------------------------------- Extra People vs max_nights ------------------------------------------------------------------------------
        fig = px.histogram(df, x='security_deposit',y ="extra_people" ,color="property_type",barmode="group",title="Grouping Security Deposit based on Extra people in each Property")
        fig.update_layout(xaxis_title="Security Deposit", yaxis_title="Extra People")
        st.plotly_chart(fig)
    
        fig = px.histogram(df, x='max_nights',y ="extra_people" ,color="property_type",barmode="group",title="Grouping Maximim Nights based on Extra people in each Property")
        fig.update_layout(xaxis_title="MAximum nights", yaxis_title="Extra People")
        st.plotly_chart(fig)
        
        fig = px.histogram(df, x='bedrooms',y ="extra_people" ,color="property_type",barmode="group",title="Grouping Bedrooms based on Extra people in each Property")
        fig.update_layout(xaxis_title="Bedrooms", yaxis_title="Extra People")
        st.plotly_chart(fig)
        
        fig = px.histogram(df, x='bathrooms',y ="extra_people" ,color="property_type",barmode="group",title="Grouping Bathrooms based on Extra people in each Property")
        fig.update_layout(xaxis_title="Bathrooms", yaxis_title="Extra People")
        st.plotly_chart(fig)
        
        
        
        #----------------------------------------------------------------------------- Nights -----------------------------------------------------------
        fig = px.histogram(df, x='room_type',y ="min_nights" ,color="min_nights",barmode="group",title=" Total Minimum nights in each Rooms")
        fig.update_layout(xaxis_title="Room Type", yaxis_title="Minimum Nights")
        st.plotly_chart(fig, use_container_width=True)
        
        fig = px.histogram(df, x='room_type',y ="max_nights" ,color="max_nights",barmode="group",title="Total Maximum nights in each Rooms")
        fig.update_layout(xaxis_title="Room Type", yaxis_title="Maximum Nights")
        st.plotly_chart(fig, use_container_width=True)
        
    
        
        corr_df = df[['accommodate', 'guests', 'extra_people', 'bedrooms', 'bathrooms', 'max_nights', 'min_nights', 'review_scores_accuracy', 'security_deposit']]
        corr_matrix = corr_df.corr()
        
        
        
        fig = px.histogram(df, x='room_type',y ="security_deposit" ,color="property_type",barmode="group",title="Total Deposit amount for each  Rooms")
        fig.update_layout(xaxis_title="Room Type", yaxis_title="Security Deposit")
        st.plotly_chart(fig, use_container_width=True)
        
        
        
        # ---------------------------------------------------------------- Correlations  ------------------------------------------------------------------------------
        fig = ff.create_annotated_heatmap(
            z=corr_matrix.values,
            x=list(corr_matrix.columns),
            y=list(corr_matrix.index),
            colorscale='RdYlGn',
            annotation_text=corr_matrix.round(2).values,
            showscale=True)
        fig.update_layout(title_text="Correlation Heatmap")
        st.plotly_chart(fig)
        
        
        df2 = df.groupby(['room_type', 'cancellation_policy']).size().reset_index(name='count')
        heatmap_data =  df2.pivot(index='cancellation_policy', columns='room_type', values='count')
        fig = px.imshow(heatmap_data, text_auto=True,color_continuous_scale='RdBu_r')
        fig.update_layout(
            title='Heatmap Map for Room Types vs. cancellation_policy')
        st.plotly_chart(fig, use_container_width=True)
        
        
        df3 = df.groupby(['property_type', 'room_type', 'cancellation_policy',"security_deposit"]).size().reset_index(name='count')
        df1 = df3.drop_duplicates(subset=['room_type', 'property_type', 'cancellation_policy',"security_deposit"], keep='first')
        fig = px.scatter(df3, x='room_type', y='count', color='cancellation_policy', facet_col='property_type',
                 category_orders={'room_type': df1['room_type'].unique()},hover_data="security_deposit",color_continuous_scale="spectral")
        fig.update_layout( xaxis=dict(tickangle=45), showlegend=True,title="Cancellation Policy impact in security Deposit")
        st.plotly_chart(fig, use_container_width=True)
        
        
        df3 = df.groupby(['property_type', 'room_type', 'review_scores_accuracy']).size().reset_index(name='count')
        df1 = df3.drop_duplicates(subset=['room_type', 'property_type' ,'review_scores_accuracy'], keep='first')
        fig = px.scatter(df1, x='room_type', y='count', color='review_scores_accuracy', facet_col='property_type',
                 category_orders={'room_type': df1['room_type'].unique()},color_continuous_scale="rdylbu")
        fig.update_layout( xaxis=dict(tickangle=45), showlegend=True,title="Reviews on Property type and Room type")
        st.plotly_chart(fig, use_container_width=True)
        
        
        df3 = df.groupby(['property_type', 'room_type', "cancellation_policy",'review_scores_accuracy']).size().reset_index(name='count')
        df1 = df3.drop_duplicates(subset=['room_type', 'property_type' ,'review_scores_accuracy'], keep='first')
        fig = px.scatter(df1, x='room_type', y='count', color='review_scores_accuracy', facet_col='property_type',
                 category_orders={'room_type': df1['room_type'].unique()},color_continuous_scale="rdylbu",hover_data="cancellation_policy")
        fig.update_layout( xaxis=dict(tickangle=45), showlegend=True,title="cancellation policy impact in reviews")
        st.plotly_chart(fig, use_container_width=True)
        
    
# ================================================== Ploting the map ===============================================================================================
    
    new_df = df.groupby(["country","property_type","room_type","latitude", "longitude","review_scores_accuracy"]).size().to_frame(name="total").reset_index()
    

    fig = px.density_mapbox(new_df,lat="longitude",lon="latitude",radius=13,
                            mapbox_style="carto-positron",zoom=1, #carto-positron stamen-terrain
                            color_continuous_scale="portland",hover_data=["property_type","room_type","review_scores_accuracy"]
                            )
    
    fig.update_layout(title='Density Map of Properties',
                mapbox=dict(center=dict(lat=new_df['longitude'].mean(),
                                        lon=new_df['latitude'].mean()),
                            zoom=15))
    st.plotly_chart(fig)
    
    
    new_df = df.groupby(["country","property_type","room_type","latitude", "longitude"]).size().to_frame(name="total").reset_index()
 
    st.map(new_df,latitude='longitude',longitude='latitude',size='review_scores_accuracy')
    
 
except Exception as e:
    st.warning("Check the options ")
    





  
    
    
    
    
    
 
 
