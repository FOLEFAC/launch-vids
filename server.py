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

app = Flask(__name__)

@app.route('/')
def main():
    return {"hello": "hi"}

@app.route('/extract', methods=['GET'])
def saver():
    time_init = time.time()
    channel_number = request.url.split("-")[-1] 
    channel_name = request.url.split("?")[-1].split("-")[0]
    #print("the channel is ", channel_name)
    data_videos = []
    videos = scrapetube.get_channel(channel_username = channel_name)
    try:
        for v, video in enumerate(videos):
            try:

                data_videos.append({'video_id':video['videoId'], 'created_at':str(datetime.datetime.utcnow()), 'uploaded_on':'unknown',
                    'title':video['title']['runs'][0]['text'], 'thumbnail':video['thumbnail']['thumbnails'][-1]['url'],
                    'rich_thumbnail':video['thumbnail']['thumbnails'][-1]['url'], 'duration':video['lengthText']['simpleText'],
                    'channel_name':channel_name})

            except Exception as error:
                pass
                #print("An error occurred:", type(error).__name__, "–", error)
            if v%1000==0 and v>0:
                print(v)
            num_videos = v
    
            if v>1998:
                break
            #print(video['videoId'])
            #print("timing_3.x", time.time()-time_init)
        #print("timing_4", time.time()-time_init)
    except Exception as error:
        print("--An error occurred:", type(error).__name__, "–"+channel_name+"-"+str(channel_number), error)
        return {"data_videos": data_videos}
    print("the number of videos is ", len(data_videos))
    return {"data_videos": data_videos}