import os
from flask import Flask, flash, render_template, redirect, request
import sys 
import time
import datetime
import os
import uuid
import pandas as pd
import sys
import scrapetube
import csv
import grequests
import time
import pandas as pd
import csv

app = Flask(__name__)

@app.route('/')
def main():
    return {"hello": "hi"}


def store_data(part, server_num):
    time_init = time.time()
    channel_list = []
    total_video_data = []
    total_channel_data = []
    df  = pd.read_csv("output_csv/output_part_"+str(part)+".csv")
    for i,f in df.iterrows():
        channel_list.append(f['channel'])
        
    
    #urls = [f"http://0.0.0.0:5400/extract?{c}" for c in channel_list]#200
    #server path -1 to -9
    urls = [f"https://flask-single-chan-{server_num}.onrender.com/extract?{c}" for c in channel_list]#200
    print("got here 1")
    time_i = time.time()
    rs = (grequests.get(u) for u in urls)
    responses = grequests.map(rs)
    print(time.time()-time_i)
    print("got here 2")

    for response in responses:
        if hasattr(response, 'status_code'):
            if response.status_code == 200:
                for v in response.json()['data_videos']:
                    total_video_data.append([v['video_id'], v['created_at'], v['uploaded_on'], v['title'],
                                            v['thumbnail'], v['rich_thumbnail'], v['duration'], v['channel_name']])
                if response.json()['data_videos'] != []:
                    total_channel_data.append([response.json()['data_videos'][0]['channel_name'], len(response.json()['data_videos'])])
            else:
                print(f"Request failed with status code: {response.status_code}")
        else:
            
            print("no attribute, the response is ", response)
    #print(total_video_data)
    print("got here 3")

    with open('videos-folder/part_'+str(part)+'-data_videos.csv', 'w', newline='',  encoding='utf-8') as csvfile:
        fieldnames = ['video_id', 'created_at', 'uploaded_on', 'title', 'thumbnail', 'rich_thumbnail', 'duration', 'channel_name']
        write = csv.writer(csvfile)
        write.writerow(fieldnames)
        write.writerows(total_video_data)

    #print("got here 4")

    with open('channels-folder/part_'+str(part)+'-data_channels.csv', 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['channel_name', 'num_videos']
        write = csv.writer(csvfile)
        write.writerow(fieldnames)
        write.writerows(total_channel_data)

    #print(len(grequests.map(responses)))
    print(f'Time for part_{part} is {time.time()-time_init}')

@app.route('/launch', methods=['GET'])
def saver():
    time_init = time.time()
    start = int(request.url.split("?")[-1].split("-")[0])
    end = int(request.url.split("?")[-1].split("-")[1])
    server_num = int(request.url.split("?")[-1].split("-")[2])
    print(start, end, server_num)

    for part in range(start, end):
        try:
            store_data(part, server_num)
        except Exception as error:
            print("--An error occurred:", type(error).__name__, "–"+str(start)+"-"+str(server_num), error)
    return {"complete": "good" }