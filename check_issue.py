import pandas as pd
import csv

df1 = pd.read_csv("./channels-folder/part_10-data_channels.csv")
output_list = []
for i,d in df1.iterrows():
    output_list.append(d['channel_name'])

df2 = pd.read_csv("./output_csv/output_part_10.csv")
input_list = []
for i,d in df2.iterrows():
    input_list.append(d['channel'])
c=0
for i in input_list:
    if i not in output_list:
        print(i)
        c+=1
print(c)
