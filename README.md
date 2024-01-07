# Youtube
Data Science Youtube Harvesting project file

The Aim of this Project is to create Streamlit application that allows user to access and analyze data from multiple channels.
The project is to understand the basics step to coonect Youtube API with Python coding flatform through Python scripting. Google Youtube API is used to extract channel details.

**#Storing API key in a Variable and importing the required libraries.**

import googleapiclient.discovery
import googleapiclient.errors
from pprint import pprint

api_key="AIzaSyDDUQDM_d_wmmUvpPwpd0OK7KQoyxg8eUs"
api_service_name = "youtube"
api_version = "v3"
youtube = googleapiclient.discovery.build(api_service_name, api_version, developerKey=api_key)

**#Python function to extract data for user input (Channel_id) youtube channels.**

def get_channel_info(ChannelId):

    channel_id = ChannelId
    videos = {}
    channelresponse = youtube.channels().list(
        id=channel_id,
        part='snippet,statistics,contentDetails,status'
    )

    channel_data = channelresponse.execute()

    #pprint(channel_data['items'])
    #print(channel_data.keys())

    channel_informations = {
      'channel_Name':channel_data['items'][0]['snippet']['title'],
      'channel_Id':channel_data['items'][0]['id'],
      'Description':channel_data['items'][0]['snippet']['description'],
      'Sub_count':channel_data['items'][0]['statistics']['subscriberCount'],
      'channel_views':channel_data['items'][0]['statistics']['viewCount'],
      'video_count':channel_data['items'][0]['statistics']['videoCount'],
      'channel_status':channel_data['items'][0]['status']['privacyStatus'],
      'playlist_Id':channel_data['items'][0]['contentDetails']['relatedPlaylists']['uploads']}

      # you have to fetch respectively more informative data's and create an dictionary for easy access

    videos['Channel_Name'] = channel_informations
    #pprint(channel_informations)
    #pprint(videos)
    ########################################################################################################### End channel info

    ##### get videos
    playlistId       = channel_data['items'][0]['contentDetails']['relatedPlaylists']['uploads']
    playlistresponse = youtube.playlistItems().list(part="snippet,contentDetails",maxResults=500,playlistId=playlistId)
    playlist_data    = playlistresponse.execute()

    playlistId = channel_data['items'][0]['contentDetails']['relatedPlaylists']['uploads']
    playlist_items = []


    #pprint(playlist_data['items'])
    i = 1

    for item in playlist_data['items']:

                video_id = item['snippet']['resourceId']['videoId']

                video_response = youtube.videos().list(
                    part='snippet,statistics,contentDetails',
                    id=video_id
                ).execute()

                #pprint(video_response['items'])
                comments_count = video_response['items'][0]['statistics']['commentCount']
                if video_response['items']:
                    video_information  = {
                        "Video_Id": video_id,
                        "Video_Name": video_response['items'][0]['snippet']['title'] if 'title' in video_response['items'][0]['snippet'] else "Not Available",
                        "video_Desc":video_response['items'][0]['snippet']['description'],
                        "video_published":video_response['items'][0]['snippet']['publishedAt'],
                        "video_viewCount":video_response['items'][0]['statistics']['viewCount'],
                        "video_likeCount":video_response['items'][0]['statistics'].get('likeCount', 0),
                        "video_fauriteCount":video_response['items'][0]['statistics']['favoriteCount'],
                        "video_commentCount":video_response['items'][0]['statistics']['commentCount'],
                        "video_Duration":video_response['items'][0]['contentDetails']['duration'],
                        "video_Thumbnail":video_response['items'][0]['snippet']['thumbnails'],
                        "Comments": {},
                    }



                ###### get video comment
                try:
                    if(comments_count):
                        commentsresponse = youtube.commentThreads().list(part="snippet,replies",videoId=video_id)
                        comments_data    = commentsresponse.execute()
                        #pprint(comments_data['items'])
                        j = 1

                        for comment in comments_data['items']:
                                    comment_information = {
                                        "Comment_Id": comment['snippet']['topLevelComment']['id'],
                                        "Comment_Text": comment['snippet']['topLevelComment']['snippet']['textDisplay'],
                                        "Comment_Author": comment['snippet']['topLevelComment']['snippet']['authorDisplayName'],
                                        "Comment_PublishedAt": comment['snippet']['topLevelComment']['snippet']['publishedAt']
                                    }

                                    #pprint(comment_information)
                                    video_information['Comments'][f'Comment_{j}'] = comment_information
                                    j += 1

                        videos[f'video_{i}'] = video_information

                        #print(i)
                        i += 1
                except Exception as e:
                       print(f"Error fetching comments")

    #pprint(videos)
    return(videos)


#user to enter channel id
channel_Id=input('Enter the channel Id: ')

channel_1=get_channel_info(channel_Id)
pprint(channel_1)

The extracted data is in Json format and this unstructured data is stored in MongoDB in local host. 

#Making connection with MongoDB, Creating Database and collection - Inserting the data for multiple channels.

!pip install pymongo
!pip install isodate
import pymongo

from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

from datetime import datetime
from isodate import parse_duration
client = pymongo.MongoClient("mongodb://localhost:27017/")

db = client.get_database('natarajan')
records = db.dt2223

Youtube multiple channels information is stored MongoDB collection and this datas are migrated to MySQL in table format (Structured data).

# Making connection with MySQL and creating the Database and Tables to migrgrate data from MongoDB to MySQL.

!pip install mysql-connector-python
import mysql.connector
mydb = mysql.connector.connect(host="localhost",user="root",password="lakshmiraj")
#print(mydb)
mycursor = mydb.cursor(buffered=True)







