
# connection to Mysql
import mysql.connector
mydb = mysql.connector.connect(host="localhost",user="root",password="lakshmiraj")

mycursor = mydb.cursor(buffered=True)

import streamlit as st
st.title("Youtube Data Harvesting Project")



# getting channel info through API

import googleapiclient.discovery
import googleapiclient.errors
from pprint import pprint
import json
import pandas as pd
import matplotlib.pyplot as plt

api_key="AIzaSyDDUQDM_d_wmmUvpPwpd0OK7KQoyxg8eUs"
api_service_name = "youtube"
api_version = "v3"
youtube = googleapiclient.discovery.build(api_service_name, api_version, developerKey=api_key)

# Use st.selectbox to select channel Id
options = ['UCxTFPM1NYtPVk1jBwUMJcnw', 'UCBq5xDFC4prrRQ8hOpBcrCQ', 'UCUUxBXYCt84q3QDx9_fB7IQ', 'UCE4N_MV7WDjoQ9mOcCpl7Vg']
selected_channel_id = st.selectbox('User input for Channel Id:', options)

Submit=st.button('SUBMIT')
if Submit:
    # User input for channel Id

    def get_channel_info(ChannelId):

        ChannelId=ChannelId
        channelresponse = youtube.channels().list(
            id=ChannelId,
            part='snippet,statistics,contentDetails,status'
        )
        channel_data = channelresponse.execute()

    

        channel_informations = {
        'channel_Name':channel_data['items'][0]['snippet']['title'],
        'channel_Id':channel_data['items'][0]['id'],
        'Description':channel_data['items'][0]['snippet']['description'],
        'Sub_count':channel_data['items'][0]['statistics']['subscriberCount'],
        'channel_views':channel_data['items'][0]['statistics']['viewCount'],
        'video_count':channel_data['items'][0]['statistics']['videoCount'],
        'channel_status':channel_data['items'][0]['status']['privacyStatus'],
        'playlist_Id':channel_data['items'][0]['contentDetails']['relatedPlaylists']['uploads']}
        return channel_informations
        
    if selected_channel_id== 'UCxTFPM1NYtPVk1jBwUMJcnw':
        channel_info = (get_channel_info(selected_channel_id))
        st.write(channel_info)

    elif selected_channel_id== 'UCBq5xDFC4prrRQ8hOpBcrCQ':
        channel_info = get_channel_info(selected_channel_id)
        st.write(channel_info)

    elif selected_channel_id== 'UCUUxBXYCt84q3QDx9_fB7IQ':
        channel_info = get_channel_info(selected_channel_id)
        st.write(channel_info)

    elif selected_channel_id== 'UCE4N_MV7WDjoQ9mOcCpl7Vg':
        channel_info = get_channel_info(selected_channel_id)
        st.write(channel_info)




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

with st.sidebar:
    # Add topics covered to the sidebar
    st.markdown('## Topics Covered')
    learnings = ['Python scripting', 'Youtube API', 'Connection-Youtube API, MongoDB & MySQL', 'Streamlit APP building']
    for learning in learnings:
        st.write(learning)

st.subheader('Video Count- Graph')
col1,col2=st.columns(2)
with col1:
    data=pd.read_csv(r"C:\Users\Antony\Documents\Data science\video_count.csv")
    st.dataframe(data.head())

with col2:
    df=pd.DataFrame(data)
    var_1 = st.selectbox('Select X-axis variable:', df.columns)
    var_2 = st.selectbox('Select Y-axis variable:', df.columns)

    # Bar chart
    fig, ax = plt.subplots()
    ax.bar(df[var_1], df[var_2])
    ax.set_xlabel(var_1)
    ax.set_ylabel(var_2)
    st.pyplot(fig)
