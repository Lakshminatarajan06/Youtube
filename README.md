# Youtube
Data Science-Youtube Data Harvesting project.

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

mycursor.execute("CREATE DATABASE youtube1")
mycursor.execute("USE youtube1")
mycursor.execute("CREATE TABLE youtube1.channel (channel_id VARCHAR(256) PRIMARY KEY,channel_name VARCHAR(255),channel_views INT,\
                  channel_Description TEXT, channel_type VARCHAR (256), channel_status TEXT)")
mycursor.execute("USE youtube1")
mycursor.execute("CREATE TABLE youtube1.playlist (playlist_id VARCHAR(256) PRIMARY KEY,channel_id VARCHAR(256), channel_Name VARCHAR (255),FOREIGN KEY (channel_id) REFERENCES youtube.channel(channel_id))")
mycursor.execute("CREATE TABLE youtube1.video (video_id VARCHAR(256) PRIMARY KEY, playlist_id VARCHAR(256), video_name VARCHAR(255), video_Description TEXT,\
                  published_date DATETIME, view_count INT, like_count INT, favourite_count INT, comment_count INT, duration INT, \
                 thumbnail VARCHAR(255),FOREIGN KEY(playlist_id) REFERENCES youtube.playlist(playlist_id))")
mycursor.execute("CREATE TABLE youtube1.comment (comment_id VARCHAR(256) PRIMARY KEY, video_id VARCHAR(256),\
                   comment_text TEXT, comment_author VARCHAR(255), comment_published_date DATETIME,FOREIGN KEY(video_id) REFERENCES youtube.video(video_id))")


After collecting multiple channel information, you can migrate it to a SQL data warehouse in structured row and column format.

#Inserting Channel informations in MySQL table using for loop

mycursor.execute("USE youtube1")
cursor = records.find()
for document in cursor:
    channel_id = document['Channel_Name']['channel_Id']
    channel_name = document['Channel_Name']['channel_Name']
    channel_views = document['Channel_Name'].get('channel_views', None)
    channel_Description = document['Channel_Name'].get('Description', None)
    channel_type = document['Channel_Name']['channel_Name']
    channel_status = document['Channel_Name'].get('channel_status', None)

    sql = "INSERT INTO channel (channel_id, channel_name, channel_views, channel_Description, channel_type, channel_status) VALUES (%s, %s, %s, %s, %s, %s)"
    
    values = (channel_id, channel_name, channel_views, channel_Description, channel_type, channel_status)


    try:
        mycursor.execute(sql, values)
        mydb.commit()
        print("Channel inserted successfully")
    except Exception as e:
        print(f"Error: {e}")

# Insert datas in playlist table for mutiple channels using for loop:
cursor = records.find()
for document in cursor:
    channel_id = document['Channel_Name']['channel_Id']
    playlist_id= document['Channel_Name']['playlist_Id']
    playlist_name= document['Channel_Name']['channel_Name']

    sql = "INSERT INTO playlist (playlist_id, channel_id, channel_name) VALUES (%s, %s, %s)"
    
    values = (playlist_id, channel_id, playlist_name)


    try:
        mycursor.execute(sql, values)
        mydb.commit()
        print("playlist inserted successfully")
    except Exception as e:
        print(f"Error: {e}")

# Insert datas in videos table for multiple channels using for loop and using datetime and isodate libraries for time converstions.
cursor = records.find()
for document in cursor:

    total_video_count = document['Channel_Name']['video_count']
    playlist_id       = document['Channel_Name']['playlist_Id']
    
    for i in range(1, int(total_video_count) + 1):

        key = f"video_{i}"
        try:
            video_id     = document[key]['Video_Id']
            video_name   = document[key]['Video_Name']
            video_description     = document[key]['video_Desc']
            published_date   = datetime.strptime(document[key]['video_published'], "%Y-%m-%dT%H:%M:%SZ")
            view_count   = document[key]['video_viewCount']
            like_count   = document[key]['video_likeCount']
            favorite_count    = document[key]['video_likeCount']
            comment_count   = document[key]['video_commentCount']

            timeconversion  = parse_duration(document[key]['video_Duration'])
            duration     = int(timeconversion.total_seconds())

            thumbnail    = document[key]['video_Thumbnail']['default']['url']

            sql = "INSERT INTO video (video_id, playlist_id, video_name, video_Description, published_date, view_count, like_count, favourite_count, \
                comment_count, duration, thumbnail) VALUES (%s, %s, %s,%s, %s, %s, %s, %s,%s, %s, %s)"
            
            values = (video_id, playlist_id, video_name, video_description, published_date, view_count, like_count, favorite_count, comment_count, duration,                     thumbnail)
            #print(duration)

            try:
                mycursor.execute(sql, values)
                mydb.commit()
                print("Videos inserted successfully")
            except Exception as e:
                print(f"Error: {e}")
        except Exception as e:
            print(f"Key error: {e}")  

# Insert datas in comment table for multiple channels using for loop
cursor = records.find()
for document in cursor:

    total_video_count = document['Channel_Name']['video_count']
    
    for i in range(1, int(total_video_count) + 1):

        key = f"video_{i}"

        video_id     = document[key]['Video_Id']
        total_comment_count = document[key]['video_commentCount']

        if(total_comment_count):
            for j in range(1, int(total_comment_count) + 1):

                commentkey = f"Comment_{j}"

                try:
                        comment_id     = document[key]['Comments'][commentkey]['Comment_Id']
                        comment_author = document[key]['Comments'][commentkey]['Comment_Author']
                        comment_text   = document[key]['Comments'][commentkey]['Comment_Text']
                        comment_published   = datetime.strptime(document[key]['Comments'][commentkey]['Comment_PublishedAt'], "%Y-%m-%dT%H:%M:%SZ")

                    
                        sql = "INSERT INTO comment (comment_id, video_id, comment_text, comment_author, comment_published_date) VALUES (%s, %s, %s,%s, %s)"
                
                        values = (comment_id, video_id, comment_text, comment_author, comment_published)
                        #print(duration)

                        try:
                            mycursor.execute(sql, values)
                            mydb.commit()
                            print("comments inserted successfully")
                        except Exception as e:
                            print(f"Error: {e}")
                except Exception as e:
                            print(f"Error: {e}")

And then using SQL query the answer for the questions is displayed in streamlit APP through various streamlit functions like buttons, dropdown box, checkbox, bar chart,et,.

import streamlit as st
st.title("Youtube Data Harvesting Project")

# Using Selectbox function the answer is displayed in streamlit application

selected_Question = st.selectbox('Select your Question:',
                                 ('1.What are the names of all the videos and their corresponding channels?',
                                  '2.Which channels have the most number of videos, and how many videos do they have?',
                                  '3.What are the top 10 most viewed videos and their respective channels?',
                                  '4.How many comments were made on each video, and what are their corresponding video names?',
                                  '5.Which videos have the highest number of likes, and what are their corresponding channel names?',
                                  '6.What is the total number of likes and dislikes for each video, and what are their corresponding video names?',
                                  '7.What is the total number of views for each channel, and what are their corresponding channel names?',
                                  '8.What are the names of all the channels that have published videos in the year 2023?',
                                  '9.What is the average duration of all videos in each channel, and what are their corresponding channel names?',
                                  '10.Which videos have the highest number of comments, and what are their corresponding channel names?'))

show=st.checkbox('SHOW ANSWER')
if show:
    def answer_question(selected_Question):
        if selected_Question == '1.What are the names of all the videos and their corresponding channels?':
            query = "SELECT vi.video_name, ch.channel_name FROM youtube1.video vi \
                    JOIN youtube1.playlist pl ON vi.playlist_id = pl.playlist_id \
                    JOIN youtube1.channel ch ON pl.channel_id = ch.channel_id"
            
            # Execute the query
            mycursor.execute(query)

            # Fetch the result
            result = mycursor.fetchall()

            # Display the result using st.write
            for i in result:
                video_name, channel_name = i
                st.write(f"Video Name: {video_name}, Channel Name: {channel_name}")

        elif selected_Question == '2.Which channels have the most number of videos, and how many videos do they have?':
            query = "SELECT ch.channel_name, COUNT(vi.video_id) AS video_count FROM youtube1.channel ch \
                    JOIN youtube1.playlist pl ON ch.channel_id = pl.channel_id \
                    JOIN youtube1.video vi ON vi.playlist_id = pl.playlist_id \
                    GROUP BY ch.channel_id \
                    ORDER BY video_count DESC"

            # Execute the query
            mycursor.execute(query)

            # Fetch the result
            result = mycursor.fetchall()

            # Display the result using st.write
            for i in result:
                channel_name, video_count = i
                st.write(f"Channel Name: {channel_name}, Video Count: {video_count}")

        elif selected_Question == '3.What are the top 10 most viewed videos and their respective channels?':

            mycursor.execute('SELECT vi.view_count, ch.channel_name FROM youtube1.video vi\
                            JOIN youtube1.playlist pl ON vi.playlist_id = pl.playlist_id\
                            JOIN youtube1.channel ch ON ch.channel_id = pl.channel_id\
                            ORDER BY vi.VIEW_COUNT DESC\
                            LIMIT 10;')

            result=mycursor.fetchall()


            # Print the result
            for i in result:
                view_count, channel_name = i
                st.write(f"view count: {view_count}, channel name: {channel_name}")

        elif selected_Question == '4.How many comments were made on each video, and what are their corresponding video names?':

            mycursor.execute("SELECT vi.comment_count, vi.video_name FROM youtube.video vi")

            result = mycursor.fetchall()

            for i in result:
                comment_count, video_name = i
                st.write(f"Comment count: {comment_count}, video name: {video_name}")

        elif selected_Question == '5.Which videos have the highest number of likes, and what are their corresponding channel names?':

            mycursor.execute('SELECT vi.video_name, vi.like_count, ch.channel_name FROM youtube1.video vi \
                    JOIN youtube1.playlist pl ON vi.playlist_id = pl.playlist_id \
                    JOIN youtube1.channel ch ON pl.channel_id = ch.channel_id \
                    ORDER BY vi.like_count DESC;')

            result = mycursor.fetchall()

            for i in result:
                video_name, like_count, channel_name = i
                st.write(f"Video name: {video_name}, Like count: {like_count}, Channel name: {channel_name}")

        elif selected_Question == '6.What is the total number of likes and dislikes for each video, and what are their corresponding video names?':

            mycursor.execute("SELECT (vi.like_count) as total_likes, vi.video_name FROM youtube1.video vi \
                    ORDER BY total_likes DESC;")

            result = mycursor.fetchall()

            for i in result:
                total_likes, video_name = i
                st.write(f"Total Likes: {total_likes}, Video name: {video_name}")

        elif selected_Question == '7.What is the total number of views for each channel, and what are their corresponding channel names?':

            mycursor.execute("SELECT ch.channel_views, ch.channel_name FROM youtube1.channel ch\
                            order by ch.channel_views desc;")
            
            result=mycursor.fetchall()

            for i in result:
                channel_views, channel_name=i
                st.write(f"channel views: {channel_views}, channel name: {channel_name}")
        
        elif selected_Question == '8.What are the names of all the channels that have published videos in the year 2023?':

            mycursor.execute("SELECT ch.channel_name, vi.video_name, vi.published_date FROM youtube1.channel ch\
                            join youtube1.playlist pl on pl.channel_id=pl.channel_id\
                            join youtube1.video vi on pl.playlist_id=vi.playlist_id\
                            where year(vi.published_date)=2023;")
            
            result = mycursor.fetchall()

            for i in result:
                channel_name, video_name, published_date = i
                st.write(f"channel name: {channel_name}, video name: {video_name}, published date: {published_date}")

        elif selected_Question == '9.What is the average duration of all videos in each channel, and what are their corresponding channel names?':

            mycursor.execute("SELECT AVG(vi.duration) as average_duration, ch.channel_name from youtube1.video vi\
                            join youtube1.playlist pl on vi.playlist_id=pl.playlist_id\
                            join youtube1.channel ch on pl.channel_id=ch.channel_id\
                            group by ch.channel_name")
            
            result = mycursor.fetchall()

            for i in result:
                average_duration, channel_name = i
                st.write(f"Average Duration: {average_duration}, channel name: {channel_name}")

        elif selected_Question == '10.Which videos have the highest number of comments, and what are their corresponding channel names?':

            mycursor.execute("SELECT vi.comment_count, ch.channel_name from youtube1.video vi\
                            join youtube1.playlist pl on vi.playlist_id=pl.playlist_id\
                            join youtube1.channel ch on pl.channel_id=ch.channel_id\
                            order by vi.comment_count desc;")
            
            result=mycursor.fetchall()

            for i in result:
                comment_count, channel_name = i
                st.write(f"comment count: {comment_count}, channel name: {channel_name}")

            
    # Use st.selectbox to get the user's question choice

    st.write('You Question:', selected_Question)

    # Call the answer_question function
    answer_question(selected_Question)
    
Finally, you can display the retrieved data in the Streamlit app. You can use Streamlit's data visualization features to create charts and graphs to help users analyze the data.


