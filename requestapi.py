import grequests
import time
import pandas as pd
import csv
import sys

server = int(sys.argv[1])
range_start = int(sys.argv[2])
range_end = int(sys.argv[3])


def store_data(part):
    time_init = time.time()
    channel_list = []
    total_video_data = []
    total_channel_data = []
    df  = pd.read_csv("output_csv/output_part_"+str(part)+".csv")
    for i,f in df.iterrows():
        channel_list.append(f['channel'])
        
    
    #urls = [f"http://0.0.0.0:5400/extract?{c}" for c in channel_list]#200
    #server path -1 to -9
    urls = [f"https://flask-single-chan-{server}.onrender.com/extract?{c}" for c in channel_list]#200
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

for part in range(range_start, range_end):
    store_data(part)

#python r and hit tab
#erros encountered cntrl + C to stop the request api
#python .\requestapi.py 9 4 9 8 4