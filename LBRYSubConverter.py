import os
import requests
import json
import soupsieve
import pkgutil

from bs4 import BeautifulSoup

fileToOpen = 'subscriptions.json'
saveFileName = 'LBRY_Subscriptions.txt'

# Opening the subscription_manager file
if os.path.exists(fileToOpen):
    youtube_subscriptions = open(fileToOpen,'r')
else:
    print("Please provide subscriptions.json")
    exit()

if os.path.exists(saveFileName):
    append_write = 'a'
else:
    append_write = 'w'
writeLbrySubs = open(saveFileName,append_write)

# Loading parser
jsonparser = json.loads(youtube_subscriptions.read())

# Close youtube json
youtube_subscriptions.close()

youtube_subsciption_ids_list = []

# Extract youtube channel Ids
for channel in jsonparser:
        youtube_subsciption_ids_list.append(channel["snippet"]["resourceId"]["channelId"])

# Convert list to string
youtube_subsciption_ids = ','.join(youtube_subsciption_ids_list)

# Create API Call based on list of extracted channel_ids
resp = requests.get("https://api.lbry.com/yt/resolve?channel_ids={"+youtube_subsciption_ids+"}")

# extract lbry channel fields from json
channels = (json.loads(resp.text))["data"]["channels"]

# loop over channels, and write if key is not 'None'. I.e it exists on lbry
count = 0
for channel in channels:
    if not channels[channel] is None :
        print ("lbry://%s" % channels[channel])
        writeLbrySubs.write("lbry://"+channels[channel] + '\n')
        count += 1

writeLbrySubs.close()


print ("Total number of YouTube channels are availible on LBRY: %s" % count)
