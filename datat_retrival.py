import pymongo
import streamlit as st
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from decimal import Decimal
from bson import Decimal128
import pandas as pd

# ======================================== setting up the Mongodb atlas  connection ==============================================================
 

def connection_db(uri):
    client = MongoClient(uri, server_api=ServerApi('1'))
    try:
        client.admin.command('ping')
        print("Pinged your deployment. You successfully connected to MongoDB!")
    except Exception as e:
           print(e)
 
   
#==================================== getting up the records in the collection of the database ===================================================
 

def retrive_records(uri,database,collection):
    client = MongoClient(uri)
    db = client.database
    record = db.listingsAndReviews
    return record

# =========================================== iterate over  each fields in the records ==============================================================

from decimal import Decimal
from bson import Decimal128

Total_entry =[]

from decimal import Decimal
from bson import Decimal128

def data_retrival(a):
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
      
      
      

# ------------------------------------------------------------------------------------------------------------------------------------------------

        
#====================================================== Data preprocess ==========================================================================

def data_type_conv(x):
    value  = int(Decimal(str(x)))
    return value


def data_processing(data):
    dataframe = pd.DataFrame(data)
    df = dataframe.dropna()
    df = df.reset_index(drop=True)
    convert_dict = {
    "security_deposit":int,
    "extra_people":int}
    df[["security_deposit","extra_people"]] = df[["security_deposit","extra_people"]].astype(convert_dict)
    df[["bedrooms","beds","bathrooms","host_response_rate","review_scores_accuracy","review_scores_cleanliness","review_scores_checkin","review_scores_communication","review_scores_location","review_scores_value","review_scores_rating"]]= df[["bedrooms","beds","bathrooms","host_response_rate","review_scores_accuracy","review_scores_cleanliness","review_scores_checkin","review_scores_communication","review_scores_location","review_scores_value","review_scores_rating"]].apply(lambda col: col.apply(data_type_conv))
    
    df_processed = df[["country","property_type","Name","room_type","cancellation_policy","accommodate","guests","extra_people","bedrooms","bathrooms","max_nights","min_nights","review_scores_accuracy","latitude","security_deposit","latitude","longitude"]] 
    
    return df_processed
    
    